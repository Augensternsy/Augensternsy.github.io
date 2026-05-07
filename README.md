# AI-Driven SDET Toolkit

> 基于 RAG 与 Agent 的自动化测试助手

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-green.svg)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 项目背景

在软件测试领域，测试工程师和 SDET 面临两大核心痛点：

1. **测试用例编写效率低**：手工编写测试用例耗时耗力，需要反复查阅测试规范文档
2. **长对话上下文管理难**：多轮对话中 LLM 的 Token 容易撑爆，导致上下文丢失或请求失败

本项目通过 **RAG（检索增强生成）** 和 **Agent 智能体** 技术，构建了一套完整的 AI 测试工具链，实现：

- 从规范文档到测试用例的自动生成
- 多轮对话的滑动窗口记忆管理
- 从 HTML DOM 到 Selenium 脚本的一键生成

---

## 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                    AI-Driven SDET Toolkit                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Stage 1     │  │  Stage 2     │  │  Stage 3         │  │
│  │  RAG 知识库  │─▶│  JSON 用例   │  │  对话记忆管理    │  │
│  │  构建        │  │  生成        │  │  (滑动窗口)      │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
│         │                  │                  │             │
│         ▼                  ▼                  ▼             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Core Technologies                       │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Python 3.10+  │  LangChain  │  ChromaDB            │  │
│  │  BGE Embedding │  OpenAI API │  tiktoken            │  │
│  │  BeautifulSoup │  Selenium   │  Recursive Splitter  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Stage 4: DOM → Selenium                 │  │
│  │  HTML 结构 ─▶ 元素分析 ─▶ Prompt ─▶ LLM ─▶ 脚本     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 核心技术栈

| 技术 | 用途 | 说明 |
|------|------|------|
| **Python 3.10+** | 开发语言 | 主要编程语言 |
| **LangChain** | 框架 | 文档加载、文本分割、向量存储 |
| **ChromaDB** | 向量数据库 | 本地持久化存储向量数据 |
| **BGE Embedding** | 向量化模型 | `BAAI/bge-base-zh-v1.5` 中文优化 |
| **OpenAI API** | LLM 调用 | 兼容 DeepSeek 等第三方 API |
| **tiktoken** | Token 计数 | 精确计算对话 Token 消耗 |
| **BeautifulSoup** | HTML 解析 | 提取 DOM 元素信息 |
| **Selenium** | 自动化测试 | 生成的目标测试框架 |

---

## 核心功能

### 第一阶段：RAG 向量检索基础

**功能描述**：将本地测试规范文档（Markdown/TXT）转换为可检索的向量知识库。

**核心流程**：
1. 读取 `./docs` 目录下所有 `.md` 和 `.txt` 文件
2. 使用 `RecursiveCharacterTextSplitter` 进行文档切片（`chunk_size=500`, `chunk_overlap=50`）
3. 使用 `HuggingFaceBgeEmbeddings` 将文本向量化
4. 持久化保存到本地 `ChromaDB` 向量数据库

**关键代码**：
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma

# 文档切片
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

# 向量化
embeddings = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-base-zh-v1.5",
    model_kwargs={'device': 'cpu'}
)

# 持久化存储
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
```

---

### 第二阶段：结构化 Prompt 生成 JSON 用例

**功能描述**：结合向量库检索和结构化 Prompt，自动生成标准 JSON 格式的测试用例。

**核心流程**：
1. 接收用户需求（如"登录接口，包含用户名和密码"）
2. 从 ChromaDB 检索 Top-3 相关测试规范
3. 构建包含 Few-Shot 示例的结构化 Prompt
4. 调用 LLM 生成 JSON 格式测试用例
5. JSON Schema 验证并保存到文件

**输出格式**：
```json
{
  "test_cases": [
    {
      "case_id": "TC001",
      "test_point": "正常登录 - 正确的用户名和密码",
      "precondition": "用户已注册，账号存在且状态正常",
      "steps": ["调用登录接口", "传入正确的用户名", "传入正确的密码"],
      "expected_result": "返回200状态码和有效的token",
      "priority": "P0",
      "test_type": "功能测试"
    }
  ]
}
```

---

### 第三阶段：对话记忆管理（滑动窗口截断）

**功能描述**：解决多轮对话中 Token 撑爆问题，实现动态滑动窗口截断策略。

**核心逻辑**：
- 维护对话历史消息列表
- 实时统计对话轮数和 Token 消耗
- 超过阈值（10 轮 或 3000 tokens）时，自动丢弃最老的 4 轮对话
- 始终保留 System Prompt

**关键代码**：
```python
class ConversationMemory:
    def __init__(self, max_rounds=10, max_tokens=3000, truncate_rounds=4):
        self.max_rounds = max_rounds
        self.max_tokens = max_tokens
        self.truncate_rounds = truncate_rounds
        self.messages = []
    
    def should_truncate(self):
        return self.count_rounds() > self.max_rounds or \
               self.count_tokens() > self.max_tokens
    
    def truncate(self):
        # 保留 System Prompt
        system_messages = [m for m in self.messages if m["role"] == "system"]
        other_messages = [m for m in self.messages if m["role"] != "system"]
        
        # 丢弃最老的 N 轮
        messages_to_remove = self.truncate_rounds * 2
        retained = other_messages[messages_to_remove:]
        
        self.messages = system_messages + retained
```

**运行效果**：
```
模拟 7 轮对话...
  轮数:  5 | Token:  168 | 消息: 11 | 截断: 0
  [触发截断条件] 当前轮数: 6 / 5
  [执行截断] 丢弃最老的 2 轮对话...
    截断后轮数: 4 | 截断后 Token: 115
```

---

### 第四阶段：HTML → Selenium 脚本生成

**功能描述**：输入 HTML DOM 结构，自动生成带显式等待的 Python+Selenium 测试脚本。

**核心流程**：
1. 使用 BeautifulSoup 解析 HTML，提取元素信息（id/name/class）
2. 构建结构化 Prompt，包含元素定位策略和代码规范
3. 调用 LLM 生成完整的 Selenium 测试脚本
4. 自动提取 Python 代码块并保存为 `.py` 文件

**生成脚本示例**：
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class TestLoginPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
    
    def test_login_functionality(self):
        self.driver.get("http://example.com/login")
        
        username_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_input.send_keys("testuser")
        
        login_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "loginBtn"))
        )
        login_button.click()
        
        self.wait.until(EC.url_changes(self.login_url))
    
    def tearDown(self):
        self.driver.quit()
```

---

## 快速开始

### 环境要求

- Python 3.10+
- pip 包管理器

### 安装依赖

```bash
pip install -r requirements.txt
```

或手动安装：

```bash
pip install langchain langchain-community langchain-text-splisters chromadb \
            sentence-transformers openai tiktoken beautifulsoup4
```

### 配置环境变量

```powershell
# Windows PowerShell
$env:OPENAI_API_KEY="your-api-key"
$env:OPENAI_BASE_URL="https://api.qnaigc.com/v1"
$env:MODEL_NAME="deepseek-v3"
```

```bash
# Linux/Mac
export OPENAI_API_KEY="your-api-key"
export OPENAI_BASE_URL="https://api.qnaigc.com/v1"
export MODEL_NAME="deepseek-v3"
```

### 运行全部阶段

```bash
python run_all_stages.py
```

### 运行单个阶段

```bash
# 第一阶段：构建 RAG 知识库
python run_all_stages.py --stage 1

# 第二阶段：生成 JSON 测试用例
python run_all_stages.py --stage 2

# 第三阶段：对话记忆管理演示
python run_all_stages.py --stage 3

# 第四阶段：HTML → Selenium 脚本生成
python run_all_stages.py --stage 4
```

---

## 项目结构

```
.
├── docs/                          # 测试规范文档目录
│   └── 软件测试规范.md
├── chroma_db/                     # 向量数据库存储
├── rag_knowledge_base.py          # 第一阶段：RAG 知识库构建
├── test_case_generator.py         # 第二阶段：JSON 用例生成
├── conversation_memory.py         # 第三阶段：对话记忆管理
├── html_to_selenium.py            # 第四阶段：Selenium 脚本生成
├── run_all_stages.py              # 统一运行入口
├── requirements.txt               # Python 依赖
└── README.md                      # 项目说明
```

---

## 使用示例

### 示例 1：构建知识库并检索

```python
# 构建知识库
python rag_knowledge_base.py

# 在代码中使用
from rag_knowledge_base import build_vectorstore, search_similar

vectorstore = build_vectorstore("./docs")
results = search_similar(vectorstore, "如何进行性能测试？", top_k=3)
```

### 示例 2：生成测试用例

```python
# 直接运行
python test_case_generator.py

# 在代码中使用
from test_case_generator import generate_test_cases

result = generate_test_cases("登录接口，包含用户名和密码")
print(result)
```

### 示例 3：多轮对话管理

```python
from conversation_memory import ConversationMemory

memory = ConversationMemory(
    system_prompt="你是一个测试专家助手。",
    max_rounds=10,
    max_tokens=3000,
    truncate_rounds=4
)

memory.add_message("user", "什么是等价类划分？")
memory.add_message("assistant", "等价类划分是一种黑盒测试方法...")

# 检查是否需要截断
if memory.should_truncate():
    memory.truncate()
```

### 示例 4：HTML → Selenium 脚本

```python
from html_to_selenium import SeleniumScriptGenerator

generator = SeleniumScriptGenerator(
    api_key="your-api-key",
    base_url="https://api.qnaigc.com/v1",
    model="deepseek-v3"
)

html = """
<div class="login-container">
    <input type="text" id="username" name="username" placeholder="用户名">
    <input type="password" id="password" name="password" placeholder="密码">
    <button type="submit" id="loginBtn">登录</button>
</div>
"""

script = generator.generate_script(html)
generator.save_script(script, "test_login.py")
```

---

## 技术亮点

| 亮点 | 说明 |
|------|------|
| **RAG 向量检索** | 使用 BGE 中文模型 + ChromaDB，实现规范文档的精准检索 |
| **结构化 Prompt** | Few-Shot + JSON Schema 验证，保证 LLM 输出格式稳定 |
| **滑动窗口管理** | 动态截断策略，解决多轮对话 Token 撑爆问题 |
| **DOM → 脚本生成** | BeautifulSoup 预处理 + 显式等待，生成高质量 Selenium 代码 |
| **统一运行入口** | `run_all_stages.py` 一键运行全部阶段 |

---

## 面试亮点

本项目可用于面试中展示以下能力：

- **RAG 技术落地**：从文档切片到向量检索的完整流程
- **Prompt Engineering**：结构化 Prompt + Few-Shot + JSON Schema 约束
- **上下文工程**：滑动窗口截断策略，解决 Token 限制问题
- **自动化测试**：从 HTML DOM 到 Selenium 脚本的代码生成
- **工程化能力**：模块化设计、统一运行入口、完整文档注释

---

## License

MIT License
