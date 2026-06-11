#!/usr/bin/env python3
"""
AI Java Coder - AI驱动的Java代码生成器
基于自然语言描述自动生成Spring Boot CRUD代码

用法:
  python ai_java_coder.py "用户管理系统，包含用户ID、用户名、密码、邮箱、手机号、创建时间"
  python ai_java_coder.py --output ./generated "订单系统，包含订单ID、用户ID、商品名称、数量、单价、总价、状态、创建时间"
  python ai_java_coder.py --framework mybatis "商品分类，包含分类ID、分类名称、父分类ID、排序号、状态"
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Load environment
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "https://api.deepseek.com/anthropic")
MODEL = os.getenv("MODEL_ID", "deepseek-v4-flash")

if not ANTHROPIC_API_KEY:
    print("Error: ANTHROPIC_API_KEY not set. Create a .env file or set environment variable.")
    sys.exit(1)

from anthropic import Anthropic
client = Anthropic(base_url=ANTHROPIC_BASE_URL)

SYSTEM_PROMPT = """你是一个专业的Java代码生成器。你擅长根据自然语言描述生成高质量的Spring Boot代码。

你需要生成以下文件（每个文件用 ``` 代码块包围，并在第一行注明文件名）:

1. Entity.java - JPA实体类或MyBatis实体
2. Repository.java - 数据访问层
3. Service.java - 业务逻辑层  
4. ServiceImpl.java - 业务逻辑实现
5. Controller.java - REST控制器
6. DTO.java - 数据传输对象（如有需要）

要求:
- 所有注释使用中文
- 遵循阿里巴巴Java开发规范
- 使用Lombok简化代码
- 包含基本的CRUD操作
- 代码完整、可直接编译运行
- 包名使用 com.example.demo
- 考虑Swagger/SpringDoc注解

输出格式:
每个文件用 ``` 包围，第一行是文件名，如:
```java:UserEntity.java
package com.example.demo.entity;
...
```"""

def generate_code(description: str, framework: str = "jpa", output_dir: str = None):
    """Generate Java CRUD code from natural language description."""
    
    framework_prompt = ""
    if framework == "mybatis":
        framework_prompt = "使用MyBatis-Plus框架，生成Mapper XML文件和实体类"
    elif framework == "jpa":
        framework_prompt = "使用Spring Data JPA框架"
    
    user_prompt = f"""请根据以下需求生成完整的Java CRUD代码：

需求描述: {description}

框架要求: {framework_prompt}

请生成实体类、Repository/Mapper、Service、ServiceImpl、Controller等完整代码文件。"""

    print(f"\n{'='*60}")
    print(f"🤖 AI正在分析需求: {description}")
    print(f"📦 框架: {framework}")
    print(f"{'='*60}\n")
    
    response = client.messages.create(
        model=MODEL,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
        max_tokens=8000
    )
    
    result = ""
    for block in response.content:
        if block.type == "text":
            result += block.text
    
    # Parse and save files
    files_saved = parse_and_save(result, output_dir)
    
    return result, files_saved

def parse_and_save(content: str, output_dir: str = None) -> list:
    """Parse AI response and save individual files."""
    import re
    
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    files_saved = []
    
    # Match code blocks with filenames
    pattern = r'```(?:java)?:?([^\n]+?)\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    if not matches:
        # Try alternate pattern
        pattern = r'```(?:java)?\n(.*?)```'
        matches = re.findall(pattern, content, re.DOTALL)
        if matches:
            # Try to extract filenames from comments
            for i, code in enumerate(matches):
                filename_match = re.search(r'(?:package|//|/*)\s*(.+?\.java)', code[:200])
                if filename_match:
                    filename = filename_match.group(1).strip()
                else:
                    filename = f"File{i+1}.java"
                
                save_path = save_file(filename, code, output_dir)
                if save_path:
                    files_saved.append(save_path)
    else:
        for filename, code in matches:
            filename = filename.strip()
            save_path = save_file(filename, code, output_dir)
            if save_path:
                files_saved.append(save_path)
    
    return files_saved

def save_file(filename: str, content: str, output_dir: str = None) -> str:
    """Save a file to the specified directory."""
    # Clean filename
    filename = filename.replace("\\", "/").split("/")[-1]
    if not filename.endswith(".java") and not filename.endswith(".xml"):
        filename += ".java"
    
    if output_dir:
        filepath = os.path.join(output_dir, filename)
    else:
        # Auto-detect package structure
        pkg_match = re.search(r'package\s+([^;]+);', content)
        if pkg_match:
            pkg_path = pkg_match.group(1).replace('.', '/')
            filepath = os.path.join(pkg_path, filename)
        else:
            filepath = filename
    
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    size = len(content)
    print(f"  ✅ 已保存: {filepath} ({size} 字节)")
    return filepath

def main():
    parser = argparse.ArgumentParser(description="AI Java Coder - AI驱动的Java代码生成器")
    parser.add_argument("description", nargs="?", help="需求描述，如：用户管理系统，包含用户ID、用户名、密码")
    parser.add_argument("--output", "-o", default="./generated", help="输出目录")
    parser.add_argument("--framework", "-f", choices=["jpa", "mybatis"], default="jpa", help="框架选择")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--list-models", action="store_true", help="列出支持的AI模型")
    
    args = parser.parse_args()
    
    print("""
╔═══════════════════════════════════════════╗
║        AI Java Coder v1.0                ║
║     AI驱动的Java代码生成器               ║
╚═══════════════════════════════════════════╝
    """)
    
    if args.list_models:
        print("支持的模型配置（通过环境变量 MODEL_ID 设置）:")
        print("  deepseek-v4-flash (默认)")
        print("  claude-sonnet-4-6")
        print("  glm-5")
        print("  kimi-k2.5")
        print("  MiniMax-M2.5")
        return
    
    if not args.description and not args.interactive:
        parser.print_help()
        print("\n示例: python ai_java_coder.py \"用户管理系统，包含用户ID、用户名、密码、邮箱\"")
        return
    
    if args.interactive:
        print("📝 请输入您的需求（输入 q 退出）:")
        while True:
            try:
                desc = input("\n需求描述 > ").strip()
                if desc.lower() in ('q', 'quit', 'exit'):
                    break
                if not desc:
                    continue
                result, files = generate_code(desc, args.framework, args.output)
                print(f"\n📊 生成了 {len(files)} 个文件，保存在 {args.output}/")
            except KeyboardInterrupt:
                break
    else:
        result, files = generate_code(args.description, args.framework, args.output)
        print(f"\n📊 生成了 {len(files)} 个文件，保存在 {args.output}/")
        print(f"\n💡 提示: 使用 -i 参数进入交互模式，-f 选择框架")

if __name__ == "__main__":
    import re  # used in save_file
    main()
