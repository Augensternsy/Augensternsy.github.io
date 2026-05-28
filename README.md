# 个人技术博客与 AI 工具链

> 基于 Hexo + GitHub Actions CI/CD + AI 测试用例生成器 + Coze Agent 的一站式技术平台

[![Hexo](https://img.shields.io/badge/Hexo-6.3+-blue.svg)](https://hexo.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.13+-orange.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-purple.svg)](https://www.langchain.com/)
[![Coze](https://img.shields.io/badge/Coze-Agent-blueviolet.svg)](https://www.coze.cn/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 项目概览

本项目是一个综合性的技术平台，包含四大核心模块：

| 模块 | 技术栈 | 功能描述 |
|------|--------|----------|
| **个人博客** | Node.js + Hexo + GitHub Actions | 具备 CI/CD 流水线的个人网站，实现自动化发布闭环 |
| **AI 测试用例生成器** | FastAPI + DeepSeek + LangChain RAG | 基于大语言模型的智能测试用例生成工具，部署于 Vercel Serverless |
| **AI 算法题解生成器** | FastAPI + DeepSeek + LangChain RAG | 算法题解与复杂度分析生成器，支持多语言代码生成 |
| **个人数字分身** | Coze 框架 + Prompt 工程 + RAG | 专属智能体，支持联网检索与简历知识库的高精准问答 |

---

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        个人技术博客与 AI 工具链                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────┐  ┌─────────────────────────────────┐  │
│  │      模块一：Hexo 博客       │  │      模块二：AI 测试用例生成器    │  │
│  │  • Node.js + Hexo           │  │  • FastAPI + Mangum            │  │
│  │  • GitHub Actions CI/CD     │  │  • DeepSeek-V3 LLM             │  │
│  │  • Matery 主题              │  │  • LangChain RAG               │  │
│  │  • 自动化发布闭环           │  │  • 纯内存向量检索               │  │
│  │                             │  │  • Vercel Serverless 部署       │  │
│  │  访问: https://augensternsy.github.io                            │  │
│  │                             │  │  访问: https://xxx.vercel.app/api/generate_cases │
│  └─────────────────────────────┘  └─────────────────────────────────┘  │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                  模块三：个人数字分身 (Agent)                    │    │
│  │  • Coze 框架                                                   │    │
│  │  • Prompt 工程逻辑约束                                         │    │
│  │  • 联网检索 Skill                                              │    │
│  │  • RAG 简历知识库                                              │    │
│  │  • 个人技术栈与履历的高精准问答                                  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📦 核心功能

### 模块一：个人博客（CI/CD 自动化发布闭环）

**功能描述**：基于 Node.js+Hexo 与 GitHub Actions 构建具备 CI/CD 流水线的个人网站，实现自动化发布闭环。

**核心特性**：
- ✅ **自动化构建**：GitHub Actions 自动触发构建
- ✅ **自动部署**：构建产物自动部署到 `gh-pages` 分支
- ✅ **主题美化**：Matery 主题，响应式设计
- ✅ **SEO 优化**：支持搜索索引生成
- ✅ **发布闭环**：代码推送即完成发布

**CI/CD 流程**：
```
代码推送 → GitHub Actions 触发 → Hexo 构建 → 部署到 gh-pages → 网站更新
```

**快速启动**：
```bash
# 安装依赖
npm install

# 本地开发
npm run server

# 构建生产版本
npm run build

# 手动部署
npm run deploy
```

---

### 模块二：AI 测试用例生成器

**功能描述**：基于 FastAPI + DeepSeek 开发 AI 测试用例生成器，部署于 Vercel Serverless 环境并集成前端交互插件；同步编写 Python 自动化脚本完成核心接口验证，保障工具可靠性。

**核心特性**：
- ✅ **RAG 检索增强**：从测试规范文档中检索相关知识
- ✅ **纯内存向量检索**：无需 FAISS，纯 Python 余弦相似度计算
- ✅ **结构化输出**：标准 JSON 格式测试用例
- ✅ **前端集成**：博客内嵌交互插件
- ✅ **接口验证**：Python 自动化脚本保障可靠性
- ✅ **Vercel Serverless**：无服务器架构部署

**技术架构**：
```
用户输入 → 向量检索 → RAG 增强 Prompt → DeepSeek LLM → JSON 测试用例
```

**API 接口**：
```
POST /api/generate_cases
Content-Type: application/json

{
"requirement": "登录接口，包含用户名和密码",
"top_k": 3
}
```

**输出示例**：
```json
{
"success": true,
"data": [
    {
    "case_id": "TC001",
    "test_point": "正常登录",
    "precondition": "用户已注册",
    "steps": ["打开登录页面", "输入用户名", "输入密码", "点击登录"],
    "expected_result": "登录成功，跳转到首页",
    "priority": "P0",
    "test_type": "功能测试"
    }
],
"total_cases": 5,
"rag_enabled": true
}
```

---

### 模块三：AI 算法题解与复杂度分析生成器

**功能描述**：基于 FastAPI + DeepSeek + 轻量级向量检索 RAG 开发的 AI 算法题解生成器，支持根据算法题描述生成解题思路、数据结构选择、参考代码、复杂度分析与边界样例。

**核心特性**：
- ✅ **轻量级向量检索 RAG**：OpenAI Embedding + 余弦相似度，无需外部向量数据库
- ✅ **关键词检索兜底**：双层召回策略，确保系统稳定性
- ✅ **RAG 算法知识库**：包含 13 种常见算法题型模板
- ✅ **结构化输出**：标准 JSON 格式，包含完整题解字段
- ✅ **多语言支持**：Python/Java/C++/JavaScript
- ✅ **复杂度分析**：自动生成时间/空间复杂度分析
- ✅ **优化版题解**：支持点击按钮生成优化版题解
- ✅ **边界样例**：至少 3 个测试用例覆盖
- ✅ **前端集成**：独立交互页面 `/algorithm-solver`

**技术架构**：
```
算法题描述 → 文档切分 → Embedding 向量化 → Top-K 相似度检索 → 结构化 Prompt → DeepSeek LLM → 标准化题解
                              ↓
                         关键词检索兜底
```

**API 接口**：
```
POST /api/algorithm-solver
Content-Type: application/json

{
"problem": "给定一个整数数组 nums 和一个目标值 target，请返回和为 target 的两个整数下标",
"language": "Python",
"mode": "standard"  // standard 或 optimized
}
```

**响应字段**（标准模式）：
| 字段 | 说明 |
|------|------|
| problem_type | 题目类型列表 |
| estimated_difficulty | 估算难度 |
| difficulty_reason | 难度判断理由 |
| core_idea | 解题核心思路 |
| data_structure | 数据结构选择 |
| step_by_step_solution | 步骤解析 |
| reference_code | 参考代码 |
| time_complexity | 时间复杂度 |
| space_complexity | 空间复杂度 |
| edge_cases | 边界样例（≥3个） |
| common_mistakes | 易错点列表 |
| optimization | 优化方案 |
| rag_context | RAG 检索到的算法模板 |

**响应字段**（优化模式）：
| 字段 | 说明 |
|------|------|
| optimized_core_idea | 优化版核心思路 |
| comparison | 优化前后对比（before/after/improvement） |
| optimized_code | 优化后代码 |
| optimized_time_complexity | 优化后时间复杂度 |
| optimized_space_complexity | 优化后空间复杂度 |
| correctness_explanation | 正确性说明 |
| applicable_conditions | 适用条件 |
| optimized_common_mistakes | 优化版易错点 |
| optimization_summary | 优化总结 |

---

### 模块四：个人数字分身（Coze Agent）

**功能描述**：研发个人数字分身（基于 Coze 框架的专属 Agent），运用 Prompt 工程进行逻辑约束；集成联网检索 Skill 与 RAG 简历知识库，实现针对个人技术栈与履历的高精准问答。

**核心特性**：
- ✅ **Prompt 工程约束**：精准的逻辑约束与角色定义
- ✅ **联网检索 Skill**：实时获取最新信息
- ✅ **RAG 简历知识库**：基于个人简历的精准问答
- ✅ **前端集成**：博客页面内嵌聊天窗口

**实现方式**：
- 集成 Coze Web SDK
- 通过 `bot_id` 连接到 Coze 平台的智能体
- 支持实时对话交互

**应用场景**：
- 🎯 技术栈介绍与问答
- 🎯 项目经验讲解
- 🎯 面试问题模拟
- 🎯 个人成就展示

**访问方式**：博客页面右下角的聊天按钮

---

## 🛠️ 技术栈

| 分类 | 技术 | 版本 | 用途 |
|------|------|------|------|
| **前端** | Hexo | 6.3+ | 静态博客框架 |
| **前端** | Matery | - | 博客主题 |
| **后端** | FastAPI | 0.115+ | API 服务框架 |
| **后端** | Mangum | 0.18+ | Vercel 适配 |
| **AI** | LangChain | 0.3+ | RAG 框架 |
| **AI** | DeepSeek | - | 大语言模型 |
| **AI** | Coze | - | Agent 框架 |
| **CI/CD** | GitHub Actions | - | 自动化部署 |
| **部署** | Vercel | - | Serverless 部署 |

---

## 📁 项目结构

```
.
├── source/                        # Hexo 博客源码
│   ├── _posts/                   # 博客文章
│   │   ├── AI测试用例生成器.md    # AI 测试用例生成器介绍
│   │   └── AI算法题解与复杂度分析生成器.md  # 算法题解生成器介绍
│   ├── about/                    # 关于页面
│   ├── algorithm-solver/         # 算法题解生成器前端页面
│   │   └── index.md              # 交互页面
│   └── ...
├── themes/                       # Hexo 主题
│   └── matery/                   # Matery 主题
│       └── layout/
│           └── layout.ejs        # Coze Agent 集成
├── api-deploy/                   # AI API 服务
│   ├── api/
│   │   └── index.py              # FastAPI 主应用
│   ├── docs/
│   │   ├── 软件测试规范.md        # 测试用例生成器知识库
│   │   └── 算法题型知识库.md      # 算法题解生成器知识库
│   ├── algorithm_solution_generator.py  # 算法题解生成器核心逻辑
│   ├── requirements.txt          # Python 依赖
│   └── vercel.json              # Vercel 配置
├── .github/
│   └── workflows/
│       └── deploy.yml            # GitHub Actions CI/CD
├── _config.yml                   # Hexo 配置
├── package.json                  # Node.js 依赖
├── test_algorithm_solver.py      # 算法题解生成器测试脚本
└── README.md                     # 项目说明
```

---

## 🚀 快速开始

### 环境要求

| 模块 | 要求 |
|------|------|
| 博客 | Node.js 18+ |
| API | Python 3.13+ |

### 博客开发

```bash
# 安装依赖
npm install

# 本地预览
npm run server

# 构建生产版本
npm run build
```

### API 开发

```bash
# 进入 API 目录
cd api-deploy

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn api.index:app --host 0.0.0.0 --port 8000 --reload
```

### 环境变量配置

在 `api-deploy/.env` 中配置：

```env
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.qnaigc.com/v1
MODEL_NAME=deepseek-v3
EMBEDDING_MODEL=text-embedding-3-small
```

---

## 🔄 CI/CD 流水线

### GitHub Actions 配置

`.github/workflows/deploy.yml` 实现了自动化发布闭环：

1. **触发条件**：`main` 分支有新推送
2. **运行环境**：Ubuntu 最新版本
3. **执行步骤**：
   - 安装 Node.js
   - 安装依赖
   - 构建 Hexo 博客
   - 部署到 `gh-pages` 分支

### Vercel 自动部署

API 服务部署到 Vercel Serverless：
- 推送代码自动触发部署
- 支持 Serverless Function 运行
- 自动 SSL 证书配置

---

## ✨ 技术亮点

| 亮点 | 说明 |
|------|------|
| **CI/CD 闭环** | GitHub Actions 实现代码推送即发布 |
| **RAG 检索增强** | 测试规范文档驱动的精准用例生成 |
| **纯内存向量检索** | 无需重型向量库，适合 Serverless 环境 |
| **前端集成** | 博客内嵌 AI 工具，用户体验无缝 |
| **Coze Agent** | 个人数字分身，精准问答能力 |

---

## 🎯 面试亮点

本项目可展示以下工程能力：

1. **CI/CD 实践**：GitHub Actions 自动化流水线配置
2. **RAG 技术落地**：从文档加载到向量检索的完整流程
3. **Prompt Engineering**：结构化 Prompt 约束 LLM 输出
4. **Serverless 部署**：Vercel Serverless 环境适配
5. **全栈开发**：前端博客 + 后端 API + AI 能力集成
6. **Agent 开发**：Coze 框架智能体集成

---

## 📄 License

MIT License
