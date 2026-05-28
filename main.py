# -*- coding: utf-8 -*-
"""
FastAPI 主应用 - AI 测试用例生成 API + 算法题解生成器 (Vercel 简化版)

功能说明：
1. 提供 RESTful API 接口，供前端调用生成测试用例
2. 提供算法题解生成器接口
3. 支持跨域请求（CORS）
4. 环境变量配置，不硬编码敏感信息

环境变量：
- OPENAI_API_KEY: API 密钥
- OPENAI_BASE_URL: API 基础 URL（可选）
- MODEL_NAME: 模型名称（可选，默认 deepseek-v3）
"""

import os
import json
import re
from dotenv import load_dotenv
from typing import List, Optional, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ValidationError
from openai import OpenAI, APIError, AuthenticationError, RateLimitError

load_dotenv()

# 创建 FastAPI 应用
app = FastAPI(
    title="AI-Driven SDET Toolkit API",
    description="基于 RAG 与 Agent 的自动化测试助手 API",
    version="1.0.0"
)

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 请求体模型
class GenerateCasesRequest(BaseModel):
    requirement: str = Field(..., min_length=1, max_length=2000)
    top_k: int = Field(default=3, ge=1, le=10)


# 初始化 OpenAI 客户端
def get_client():
    return OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.qnaigc.com/v1")
    )


@app.get("/")
async def root():
    return {
        "name": "AI-Driven SDET Toolkit API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/generate_cases")
async def generate_cases(request: GenerateCasesRequest):
    try:
        system_prompt = """你是一个专业的软件测试工程师。请根据用户的需求生成标准化的测试用例。

要求：
1. 生成 5 个测试用例
2. 每个用例包含：case_id, test_point, precondition, steps, expected_result, priority, test_type
3. 返回纯 JSON 格式，不要包含其他文字
4. priority 使用 P0/P1/P2
5. test_type 使用：功能测试/异常测试/边界测试/性能测试/安全测试

JSON 格式示例：
{
  "test_cases": [
    {
      "case_id": "TC001",
      "test_point": "正常登录",
      "precondition": "用户已注册",
      "steps": ["打开登录页面", "输入用户名", "输入密码", "点击登录"],
      "expected_result": "登录成功，跳转到首页",
      "priority": "P0",
      "test_type": "功能测试"
    }
  ]
}"""

        user_prompt = f"请为以下需求生成测试用例：{request.requirement}"

        client = get_client()
        model_name = os.getenv("MODEL_NAME", "deepseek-v3")

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        response_text = response.choices[0].message.content

        # 解析 JSON
        json_start = response_text.find("{")
        json_end = response_text.rfind("}") + 1
        if json_start != -1 and json_end != -1:
            json_str = response_text[json_start:json_end]
            json_data = json.loads(json_str)
        else:
            json_data = json.loads(response_text)

        test_cases = json_data.get("test_cases", [])

        return {
            "success": True,
            "message": "测试用例生成成功",
            "data": test_cases,
            "total_cases": len(test_cases)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"生成测试用例失败: {str(e)}"
        )


# ========== 算法题解生成器 ==========

class AlgorithmRequest(BaseModel):
    """算法题解请求模型"""
    problem: str
    language: str = "Python"


def extract_json_from_markdown(text: str) -> str:
    """从 Markdown 代码块中提取 JSON"""
    pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    
    pattern = r'```\s*([\s\S]*?)\s*```'
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    
    return text


def parse_json_safely(text: str) -> Optional[dict]:
    """安全解析 JSON，处理各种异常情况"""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    extracted = extract_json_from_markdown(text)
    try:
        return json.loads(extracted)
    except json.JSONDecodeError:
        pass
    
    try:
        fixed = re.sub(r',\s*([}\]])', r'\1', extracted)
        return json.loads(fixed)
    except json.JSONDecodeError:
        pass
    
    return None


@app.post("/api/algorithm-solver")
async def algorithm_solver(request: AlgorithmRequest):
    """
    AI 算法题解与复杂度分析生成器
    
    根据算法题描述生成：
    - 题目类型识别
    - 解题思路
    - 数据结构选择
    - 参考代码
    - 复杂度分析
    - 边界样例
    - 易错点总结
    - 优化方案
    """
    if not request.problem or not request.problem.strip():
        return {
            "success": False,
            "message": "题目描述不能为空",
            "data": None
        }
    
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_BASE_URL", "https://api.qnaigc.com/v1")
    model_name = os.getenv("MODEL_NAME", "deepseek-v3")
    
    if not api_key:
        return {
            "success": False,
            "message": "未配置 OPENAI_API_KEY 环境变量",
            "data": None
        }
    
    system_prompt = f"""你是一名资深算法工程师和 LeetCode 题解专家。
你的任务是根据用户输入的算法题描述，生成结构化的算法题解。

## 难度判断规则
你需要根据算法题描述自动判断题目难度，难度分为：简单、中等、困难。

判断标准：

简单：
- 通常只需要一次遍历、简单条件判断、基础哈希表、简单数组操作。
- 状态设计较少，不涉及复杂递归或多阶段决策。
- 例如：两数之和、有效括号、合并两个有序数组。

中等：
- 需要明确的数据结构选择或算法模式。
- 可能涉及动态规划、滑动窗口、双指针、DFS/BFS、二分查找、回溯等。
- 需要分析状态转移、搜索过程或边界条件。
- 例如：最长无重复子串、01背包、岛屿数量、三数之和。

困难：
- 需要多个算法思想组合。
- 需要复杂状态设计、优化技巧、剪枝、单调队列、线段树、图论高级算法等。
- 暴力解和最优解差距较大，复杂度优化难度高。
- 例如：编辑距离进阶优化、最小覆盖子串、接雨水、困难图论问题。

## Few-shot 示例（严格参考此格式生成）
示例输入：
{{
  "problem": "给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的两个整数，并返回它们的数组下标。",
  "language": "Python"
}}

示例输出：
{{
  "problem_type": ["数组", "哈希表"],
  "estimated_difficulty": "简单",
  "difficulty_reason": "只需要一次遍历和哈希表即可解决，属于经典的数组+哈希表问题。",
  "core_idea": "使用哈希表记录已经遍历过的元素及其下标，在遍历当前元素时判断 target - nums[i] 是否已经出现。",
  "data_structure": "使用哈希表（字典），因为需要在 O(1) 平均时间内判断补数是否存在。",
  "step_by_step_solution": [
    "1. 初始化一个空哈希表，用于存储元素值到下标的映射。",
    "2. 遍历数组 nums。",
    "3. 对每个元素 nums[i]，计算 complement = target - nums[i]。",
    "4. 如果 complement 已经在哈希表中，返回对应下标和当前下标。",
    "5. 否则将当前元素和下标存入哈希表。"
  ],
  "reference_code": "class Solution:\\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\\n        seen = {{}}\\n        for i, num in enumerate(nums):\\n            need = target - num\\n            if need in seen:\\n                return [seen[need], i]\\n            seen[num] = i\\n        return []",
  "time_complexity": "O(n)，其中 n 是数组 nums 的长度，需要遍历数组一次。",
  "space_complexity": "O(n)，最坏情况下需要将 n 个元素存入哈希表。",
  "edge_cases": [
    {{"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "nums[0] + nums[1] = 2 + 7 = 9"}},
    {{"input": "nums = [3,2,4], target = 6", "output": "[1,2]", "explanation": "nums[1] + nums[2] = 2 + 4 = 6"}},
    {{"input": "nums = [3,3], target = 6", "output": "[0,1]", "explanation": "nums[0] + nums[1] = 3 + 3 = 6"}}
  ],
  "common_mistakes": ["先把当前元素放入哈希表再查找，可能导致同一个元素被使用两次。", "没有考虑数组中存在重复元素的情况。"],
  "optimization": "暴力解法需要 O(n²) 时间复杂度，使用哈希表可以将时间复杂度优化到 O(n)，空间复杂度为 O(n)。",
  "rag_context": "数组与哈希表"
}}

## 用户输入
{{
  "problem": "{request.problem}",
  "language": "{request.language}"
}}

## 输出要求（必须严格遵守）
1. 只输出 JSON，不要输出任何其他文字。
2. 必须包含以下字段：problem_type, estimated_difficulty, difficulty_reason, core_idea, data_structure, step_by_step_solution, reference_code, time_complexity, space_complexity, edge_cases, common_mistakes, optimization, rag_context。
3. problem_type 是字符串数组，用于识别题型，如：数组、哈希表、双指针、滑动窗口、动态规划、栈、队列、树、图、回溯、贪心等。
4. estimated_difficulty 取值为：简单、中等、困难。
5. difficulty_reason 解释为什么属于该难度。
6. rag_context 返回最相关的算法模板名称，用顿号分隔，如："数组与哈希表"、"双指针与排序"、"动态规划-背包问题"、"图论-DFS/BFS"等。如果没有匹配到明确模板，返回空字符串""。
7. step_by_step_solution 是字符串数组。
8. edge_cases 至少包含 3 个对象，每个对象包含 input, output, explanation 字段。
9. common_mistakes 是字符串数组。
10. reference_code 包含完整可运行的代码。
11. time_complexity 和 space_complexity 说明复杂度并解释变量含义。

开始输出："""

    try:
        client = OpenAI(
            api_key=api_key,
            base_url=api_base
        )
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "请生成算法题解，只输出 JSON。"}
            ],
            temperature=0.3,
            max_tokens=3000,
            response_format={"type": "json_object"}
        )
        
        result_text = response.choices[0].message.content.strip()
        result = parse_json_safely(result_text)
        
        if result is None:
            return {
                "success": False,
                "message": "无法解析模型输出",
                "data": None
            }
        
        required_fields = [
            "problem_type", "estimated_difficulty", "difficulty_reason",
            "core_idea", "data_structure", "step_by_step_solution",
            "reference_code", "time_complexity", "space_complexity",
            "edge_cases", "common_mistakes", "optimization", "rag_context"
        ]
        
        for field in required_fields:
            if field not in result or result[field] is None:
                result[field] = "" if field not in ["problem_type", "step_by_step_solution", "edge_cases", "common_mistakes"] else []
        
        if not isinstance(result["edge_cases"], list):
            result["edge_cases"] = []
        else:
            valid_cases = []
            for case in result["edge_cases"]:
                if isinstance(case, dict) and "input" in case and "output" in case:
                    valid_cases.append({
                        "input": case.get("input", ""),
                        "output": case.get("output", ""),
                        "explanation": case.get("explanation", "")
                    })
            result["edge_cases"] = valid_cases
        
        if not result["rag_context"]:
            result["rag_context"] = ""
        
        return {
            "success": True,
            "message": "算法题解生成成功",
            "data": result
        }
        
    except AuthenticationError:
        return {
            "success": False,
            "message": "API Key 无效或已过期",
            "data": None
        }
    except RateLimitError:
        return {
            "success": False,
            "message": "API 请求超限，请稍后重试",
            "data": None
        }
    except APIError as e:
        return {
            "success": False,
            "message": f"API 服务异常: {str(e)}",
            "data": None
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"生成算法题解失败: {str(e)}",
            "data": None
        }


# Vercel Serverless 部署需要的 Mangum 适配器
from mangum import Mangum

handler = Mangum(app)
