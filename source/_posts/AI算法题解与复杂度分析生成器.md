---
title: 基于 FastAPI + DeepSeek + 轻量级向量检索 RAG 的 AI 算法题解与复杂度分析生成器
date: 2026-05-29 10:00:00
top: true
categories:
  - 技术分享
tags:
  - Python
  - FastAPI
  - AI
  - RAG
  - 算法
---

## 项目背景

作为一个经常刷 LeetCode 的开发者，我一直在思考如何提高算法学习效率。面对一道新题时，往往需要：
1. 判断题目类型
2. 回忆相关解题模板
3. 设计数据结构和算法
4. 编写代码并分析复杂度
5. 考虑边界情况和易错点

这个过程对于初学者来说门槛很高，即使是有经验的开发者也需要花费不少时间。于是我想到，能不能用 AI 来辅助完成这些工作？

## 为什么要做算法题解生成器

1. **提高学习效率**：快速获取专业的题解分析，节省思考时间
2. **标准化输出**：确保题解包含完整的复杂度分析、边界样例和易错点
3. **知识沉淀**：通过 RAG 技术整合常见算法模板，形成知识库
4. **辅助面试准备**：帮助开发者快速复习算法知识，应对技术面试

## 技术栈

- **FastAPI**：高性能 Python Web 框架，用于构建 API 服务
- **DeepSeek**：开源大语言模型，提供代码生成能力
- **轻量级向量检索 RAG**：OpenAI Embedding + 余弦相似度，无需外部向量数据库
- **Mangum**：AWS Lambda/API Gateway 适配器，支持 Vercel Serverless 部署
- **Pydantic**：数据验证和序列化

## 系统架构

```
用户请求 → FastAPI → 算法题解生成器 → DeepSeek API
                                 ↓
                          轻量级 RAG 检索
                              ↓
                ┌──────────────┴───────────────┐
                ↓                              ↓
         Embedding 向量化检索          关键词检索兜底
                ↓                              ↓
         余弦相似度 Top-K               模板匹配
```

### 核心流程

1. **输入处理**：接收算法题描述、语言选择和生成模式
2. **RAG 检索**：根据题目描述从知识库中检索相关算法模板（优先向量检索，失败则关键词兜底）
3. **Prompt 构建**：结合检索结果构建结构化提示词
4. **模型调用**：调用 DeepSeek API 生成题解
5. **结果解析**：解析 JSON 响应，确保字段完整
6. **结果返回**：返回标准化的题解数据

## 轻量级向量检索 RAG 设计

我选择了纯 Python 实现的轻量级向量检索方案，无需引入 FAISS、Chroma 等重型依赖，非常适合 Vercel Serverless 环境。

### RAG 架构特点

1. **文档切分**：按 Markdown 标题切分知识库文档
2. **Embedding 向量化**：使用 OpenAI Embedding API
3. **余弦相似度**：纯 Python 实现相似度计算
4. **双层召回策略**：
   - 优先：Embedding 语义检索
   - 兜底：关键词匹配检索
5. **内存缓存**：向量缓存在内存中，首次加载后快速检索

## RAG 知识库设计

我整理了 13 种常见算法题型的详细模板，包括：

| 题型 | 典型题目 | 核心思路 |
|------|----------|----------|
| 数组与哈希表 | 两数之和 | O(1) 查找 |
| 双指针与排序 | 三数之和 | 两端向中间移动 |
| 滑动窗口 | 最长无重复子串 | 动态维护窗口边界 |
| 栈与单调栈 | 接雨水 | 维护单调序列 |
| 链表操作 | 反转链表 | 指针操作 |
| 树与二叉树 | 前中后序遍历 | 递归/迭代 |
| 二分查找 | 搜索旋转数组 | 对数时间查找 |
| 动态规划 - 背包问题 | 01背包 | 状态转移方程 |
| 动态规划 - 其他问题 | 最长递增子序列 | 状态转移 |
| 图论 - DFS与BFS | 岛屿数量 | 图遍历 |
| 贪心算法 | 跳跃游戏 | 局部最优选择 |

每个模板包含：题型特点、典型题目、解题思路、数据结构选择。

## Prompt 设计

我设计了严格的结构化 Prompt，确保输出格式稳定：

```
你是一名资深算法工程师和 LeetCode 题解专家。

## 参考知识（从知识库检索）
{rag_context}

## Few-shot 示例
示例输入：{"problem": "...", "language": "Python", "mode": "standard"}
示例输出：{"problem_type": [...], "core_idea": "...", ...}

## 用户输入
{"problem": "...", "language": "...", "mode": "..."}

## 输出要求
1. 只输出 JSON，不要输出任何其他文字
2. 必须包含所有要求的字段
3. edge_cases 至少包含 3 个样例
```

## API 接口说明

### 请求接口

**POST** `/api/algorithm-solver`

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| problem | string | 是 | 算法题描述 |
| language | string | 否 | 编程语言（默认 Python） |
| mode | string | 否 | 生成模式（standard/optimized，默认 standard） |

### 响应字段（标准模式）

| 字段 | 类型 | 说明 |
|------|------|------|
| problem_type | array | 题目类型列表 |
| estimated_difficulty | string | 估算难度 |
| difficulty_reason | string | 难度判断理由 |
| core_idea | string | 解题核心思路 |
| data_structure | string | 数据结构选择 |
| step_by_step_solution | array | 步骤解析 |
| reference_code | string | 参考代码 |
| time_complexity | string | 时间复杂度 |
| space_complexity | string | 空间复杂度 |
| edge_cases | array | 边界样例（至少3个） |
| common_mistakes | array | 易错点列表 |
| optimization | string | 优化方案 |
| rag_context | string | RAG 检索到的算法模板 |

### 响应字段（优化模式）

| 字段 | 类型 | 说明 |
|------|------|------|
| optimized_core_idea | string | 优化版核心思路 |
| comparison | object | 优化前后对比（before/after/improvement） |
| optimized_code | string | 优化后代码 |
| optimized_time_complexity | string | 优化后时间复杂度 |
| optimized_space_complexity | string | 优化后空间复杂度 |
| correctness_explanation | string | 正确性说明 |
| applicable_conditions | string | 适用条件 |
| optimized_common_mistakes | array | 优化版易错点 |
| optimization_summary | string | 优化总结 |

## 示例输入输出

### 标准模式输入

```json
{
  "problem": "给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的两个整数，并返回它们的数组下标。",
  "language": "Python",
  "mode": "standard"
}
```

### 标准模式输出

```json
{
  "problem_type": ["数组", "哈希表"],
  "estimated_difficulty": "easy",
  "difficulty_reason": "只需一次遍历和简单哈希表操作",
  "core_idea": "使用哈希表记录已经遍历过的元素及其下标...",
  "data_structure": "使用哈希表（字典）...",
  "step_by_step_solution": ["1. 初始化空哈希表...", "..."],
  "reference_code": "class Solution:\n    def twoSum(self, nums, target):\n        ...",
  "time_complexity": "O(n)",
  "space_complexity": "O(n)",
  "edge_cases": [
    {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "..."},
    ...
  ],
  "common_mistakes": ["先放入哈希表再查找...", "..."],
  "optimization": "暴力解法 O(n²) → 哈希表 O(n)",
  "rag_context": "数组与哈希表"
}
```

### 优化模式输入

```json
{
  "problem": "给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的两个整数，并返回它们的数组下标。",
  "language": "Python",
  "mode": "optimized"
}
```

### 优化模式输出

```json
{
  "optimized_core_idea": "本题已经是最优解法，无需进一步优化",
  "comparison": {
    "before": "O(n²) 时间复杂度的暴力解法，双重循环遍历所有可能",
    "after": "O(n) 时间复杂度的哈希表解法，只需要一次遍历",
    "improvement": "时间复杂度从 O(n²) 优化到 O(n)，空间复杂度从 O(1) 变为 O(n)"
  },
  "optimized_code": "class Solution:\n    def twoSum(self, nums, target):\n        ...",
  "optimized_time_complexity": "O(n)",
  "optimized_space_complexity": "O(n)",
  "correctness_explanation": "由于每个元素只访问一次，且通过哈希表在 O(1) 时间内查找补数，算法正确且高效",
  "applicable_conditions": "适用于需要在数组中找两数之和的问题",
  "optimized_common_mistakes": ["先放入哈希表再查找...", "..."],
  "optimization_summary": "本题当前解法已经是时间最优，无需进一步优化"
}
```

## 异常处理与 JSON 稳定性设计

### 异常处理策略

1. **空输入处理**：检测空题目描述，返回友好错误信息
2. **API Key 缺失**：检查环境变量，返回明确错误
3. **认证失败**：捕获 AuthenticationError，提示 Key 无效
4. **请求超限**：捕获 RateLimitError，提示稍后重试
5. **JSON 解析失败**：多层解析策略，从 Markdown 代码块中提取
6. **RAG 检索失败**：自动降级到关键词检索，确保系统稳定

### JSON 稳定性保障

1. **强制 JSON 格式**：使用 `response_format={"type": "json_object"}`
2. **代码块提取**：支持提取 ```json ... ``` 格式的内容
3. **自动修复**：处理末尾多余逗号等常见问题
4. **字段补全**：确保所有必需字段存在，缺失时填充默认值
5. **格式验证**：验证数组类型字段，确保格式正确

## 项目亮点

1. **轻量级向量检索 RAG**：OpenAI Embedding + 余弦相似度，无需外部向量数据库
2. **双层召回策略**：优先语义检索，失败则关键词兜底，确保系统稳定性
3. **优化版题解**：支持点击按钮生成优化版题解，包含前后对比
4. **标准化输出**：严格的字段验证和格式规范
5. **可扩展性**：支持多语言代码生成，易于添加新题型模板
6. **Serverless 友好**：适配 Vercel Serverless 部署环境

## 后续可扩展方向

1. **代码执行验证**：集成代码沙箱，验证生成代码的正确性
2. **多语言支持**：扩展支持 C++、Go、Rust 等语言
3. **进阶算法模板**：添加更多高级算法题型（图论、数论等）
4. **用户反馈机制**：收集用户反馈，持续优化知识库
5. **题目相似度匹配**：根据输入自动推荐相似题目

## 总结

这个项目让我对 RAG 技术和 Prompt 工程有了更深入的理解。通过将算法知识结构化存储，并结合大语言模型的生成能力，可以大大提高算法学习的效率。后续我会继续完善这个工具，希望能帮助更多开发者提升算法能力。

---

**项目地址**：[GitHub](https://github.com/augensternsy/blog)

**在线体验**：访问 `/algorithm-solver` 页面即可使用