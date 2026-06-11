# AI Java Coder 🚀

> AI驱动的Java代码生成器 - 输入中文描述，自动生成完整Spring Boot CRUD代码

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Donate Bitcoin](https://img.shields.io/badge/Donate-Bitcoin-orange.svg)](#支持我们)

## 📋 简介

**AI Java Coder** 是一个基于AI大模型的Java代码生成工具。你只需要用自然语言描述你的需求，它就能自动生成完整的、可直接编译运行的Spring Boot CRUD代码。

### ✨ 特性

- 🎯 **中文输入** - 用中文描述需求，AI理解并生成代码
- 📦 **完整CRUD** - 生成 Entity、Repository、Service、Controller、DTO 全套代码
- 📝 **中文注释** - 所有代码注释均为中文，便于团队理解
- 🏗️ **最佳实践** - 遵循阿里巴巴Java开发规范
- 🚀 **一键生成** - 秒级生成完整项目代码
- 🔧 **框架选择** - 支持 JPA 和 MyBatis-Plus
- 📊 **Swagger支持** - 自动添加 OpenAPI 注解

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/zyggood/ai-java-coder.git
cd ai-java-coder

# 安装依赖
pip install -r requirements.txt

# 配置API密钥
cp .env.example .env
# 编辑 .env 文件，填入你的 API Key
```

### 使用

```bash
# 一行命令生成代码
python ai_java_coder.py "用户管理系统，包含用户ID、用户名、密码、邮箱、手机号、创建时间"

# 指定输出目录
python ai_java_coder.py "订单系统，包含订单ID、用户ID、商品名称、数量、单价、总价、状态" --output ./my-project

# 使用MyBatis框架
python ai_java_coder.py "商品分类，包含分类ID、分类名称、父分类ID、排序号" --framework mybatis

# 交互模式
python ai_java_coder.py --interactive
```

## 📖 示例

输入：
```bash
python ai_java_coder.py "用户管理系统，包含用户ID、用户名、密码、邮箱、手机号、创建时间"
```

输出 (8个文件)：
| 文件 | 说明 |
|------|------|
| `User.java` | JPA实体类，带Swagger注解和中文注释 |
| `UserRepository.java` | 数据访问层 |
| `UserService.java` | 业务逻辑接口 |
| `UserServiceImpl.java` | 业务逻辑实现，完整CRUD逻辑 |
| `UserController.java` | REST控制器，RESTful API |
| `UserCreateDTO.java` | 创建请求DTO |
| `UserUpdateDTO.java` | 更新请求DTO |
| `UserResponseDTO.java` | 响应DTO |

### 生成的API接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/users` | 创建用户 |
| GET | `/api/users/{id}` | 查询用户详情 |
| GET | `/api/users` | 分页查询用户列表 |
| PUT | `/api/users/{id}` | 更新用户 |
| DELETE | `/api/users/{id}` | 删除用户 |

## 🛠️ 高级用法

### 框架选择

```bash
# Spring Data JPA (默认)
python ai_java_coder.py "..." --framework jpa

# MyBatis-Plus
python ai_java_coder.py "..." --framework mybatis
```

### 批量生成（交互模式）

```bash
python ai_java_coder.py -i
```

进入交互模式后，可以连续输入多个需求，每次输入都会生成一套代码。

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 许可证

[MIT License](LICENSE)

## 💖 支持我们

如果您觉得这个工具对您有帮助，欢迎赞助支持我们继续开发！

**比特币 (BTC) 捐赠:**

- **SegWit (推荐，费率低):** `bc1q5s8srtuuqvl25fax3ylqscrjvfyes89akmwq0h`
- **Legacy:** `1FxTo8tgQJHuvpG5rpw3UP31ca3Q5RWPnc`

您的支持是我们前进的动力！🚀

---

**关键词:** Java代码生成, Spring Boot, CRUD, AI编程, 代码自动生成, Java, MyBatis, JPA
