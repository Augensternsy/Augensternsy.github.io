# RAG 向量知识库使用指南

## 项目结构

```
blog/
├── docs/                          # 文档目录
│   └── 软件测试规范.md             # 示例文档
├── chroma_db/                     # 向量数据库存储目录（运行后生成）
├── rag_knowledge_base.py          # RAG 知识库构建脚本
└── requirements.txt               # Python 依赖列表
```

## 环境准备

### 1. 安装 Python

确保已安装 Python 3.8 或更高版本：

```bash
python --version
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

或者手动安装：

```bash
pip install langchain langchain-community langchain-text-splitters chromadb sentence-transformers
```

## 使用方法

### 构建向量知识库

运行主脚本：

```bash
python rag_knowledge_base.py
```

脚本将执行以下步骤：

1. **加载文档** - 从 `./docs` 目录读取所有 `.md` 和 `.txt` 文件
2. **文档切片** - 使用 RecursiveCharacterTextSplitter 进行切片（chunk_size=500, chunk_overlap=50）
3. **加载 Embedding 模型** - 使用 BAAI/bge-base-zh-v1.5 中文 Embedding 模型
4. **构建向量数据库** - 将向量数据保存到 `./chroma_db` 目录

### 使用已构建的知识库

在你的 Python 代码中加载并使用知识库：

```python
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

# 加载 Embedding 模型
embeddings = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-base-zh-v1.5",
    model_kwargs={'device': 'cpu'}
)

# 加载已保存的向量数据库
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# 执行相似度检索
query = "软件测试的基本要求是什么？"
results = vectorstore.similarity_search(query, k=3)

for i, result in enumerate(results, 1):
    print(f"结果 {i}:")
    print(f"来源: {result.metadata['source_file']}")
    print(f"内容: {result.page_content}")
    print()
```

## 自定义配置

### 修改切片参数

在 `rag_knowledge_base.py` 中修改：

```python
chunk_size = 500      # 每个文本块的大小（字符数）
chunk_overlap = 50    # 文本块之间的重叠字符数
```

### 更换 Embedding 模型

支持的模型：

- `BAAI/bge-base-zh-v1.5` - 中文优化（推荐）
- `BAAI/bge-large-zh-v1.5` - 更大的中文模型
- `sentence-transformers/all-MiniLM-L6-v2` - 英文轻量级模型

### 添加更多文档

将 `.md` 或 `.txt` 文件放入 `./docs` 目录即可，支持子目录。

## 常见问题

### Q: 首次运行很慢怎么办？

A: 首次运行需要下载 Embedding 模型（约 400MB），请耐心等待。后续运行会直接使用缓存。

### Q: 如何清理向量数据库？

A: 删除 `./chroma_db` 目录后重新运行脚本即可。

### Q: 支持 GPU 加速吗？

A: 支持。将 `model_kwargs={'device': 'cpu'}` 改为 `model_kwargs={'device': 'cuda'}`。

## 下一步

构建好向量知识库后，你可以：

1. **接入 LLM** - 结合 OpenAI、通义千问等大语言模型实现 RAG 问答
2. **构建 Web 应用** - 使用 Streamlit 或 FastAPI 创建问答界面
3. **集成到现有系统** - 将检索功能集成到你的面试助手中
