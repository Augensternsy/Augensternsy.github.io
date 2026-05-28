# -*- coding: utf-8 -*-
"""
AI 算法题解生成器测试脚本
覆盖多种算法题型和异常场景
"""
import requests
import json
import sys

API_URL = "http://127.0.0.1:8000/api/algorithm-solver"

def print_test_title(title):
    """打印测试标题"""
    print("=" * 70)
    print(f"【测试】{title}")
    print("=" * 70)

def print_test_result(passed, message):
    """打印测试结果"""
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} {message}")
    print("-" * 70)
    return passed

def validate_standard_response_fields(data):
    """验证标准题解响应字段完整性"""
    required_fields = [
        "problem_type", "estimated_difficulty", "difficulty_reason",
        "core_idea", "data_structure", "step_by_step_solution",
        "reference_code", "time_complexity", "space_complexity",
        "edge_cases", "common_mistakes", "optimization", "rag_context"
    ]
    
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
        elif data[field] is None:
            missing_fields.append(field)
    
    return missing_fields

def validate_optimized_response_fields(data):
    """验证优化版题解响应字段完整性"""
    required_fields = [
        "optimized_core_idea", "comparison", "optimized_code",
        "optimized_time_complexity", "optimized_space_complexity",
        "correctness_explanation", "applicable_conditions",
        "optimized_common_mistakes", "optimization_summary"
    ]
    
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
        elif data[field] is None:
            missing_fields.append(field)
    
    # 验证 comparison 对象
    if "comparison" in data and data["comparison"] is not None:
        if not isinstance(data["comparison"], dict):
            missing_fields.append("comparison (should be dict)")
        else:
            if "before" not in data["comparison"]:
                missing_fields.append("comparison.before")
            if "after" not in data["comparison"]:
                missing_fields.append("comparison.after")
            if "improvement" not in data["comparison"]:
                missing_fields.append("comparison.improvement")
    
    return missing_fields

def test_two_sum_standard():
    """测试两数之和 - 标准题解"""
    print_test_title("两数之和 - 标准题解")
    
    payload = {
        "problem": "给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的两个整数，并返回它们的数组下标。",
        "language": "Python",
        "mode": "standard"
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        
        if response.status_code != 200:
            return print_test_result(False, f"请求失败，状态码: {response.status_code}")
        
        data = response.json()
        if not data.get("success"):
            return print_test_result(False, f"生成失败: {data.get('message')}")
        
        result = data.get("data", {})
        
        # 验证字段完整性
        missing_fields = validate_standard_response_fields(result)
        if missing_fields:
            return print_test_result(False, f"缺少字段: {', '.join(missing_fields)}")
        
        # 验证题型识别
        has_expected_type = False
        for pt in result["problem_type"]:
            if "数组" in pt or "哈希表" in pt:
                has_expected_type = True
                break
        if not has_expected_type:
            return print_test_result(False, f"题型识别错误: {result['problem_type']}")
        
        # 验证边界样例数量
        if len(result["edge_cases"]) < 3:
            return print_test_result(False, f"边界样例不足3个: {len(result['edge_cases'])}")
        
        # 验证代码不为空
        if not result["reference_code"]:
            return print_test_result(False, "参考代码为空")
        
        return print_test_result(True, "两数之和标准题解测试通过")
    
    except Exception as e:
        return print_test_result(False, f"异常: {str(e)}")

def test_two_sum_optimized():
    """测试两数之和 - 优化版题解"""
    print_test_title("两数之和 - 优化版题解")
    
    payload = {
        "problem": "给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的两个整数，并返回它们的数组下标。",
        "language": "Python",
        "mode": "optimized"
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        
        if response.status_code != 200:
            return print_test_result(False, f"请求失败，状态码: {response.status_code}")
        
        data = response.json()
        if not data.get("success"):
            return print_test_result(False, f"生成失败: {data.get('message')}")
        
        result = data.get("data", {})
        
        # 验证字段完整性
        missing_fields = validate_optimized_response_fields(result)
        if missing_fields:
            return print_test_result(False, f"缺少字段: {', '.join(missing_fields)}")
        
        # 验证优化代码不为空
        if not result["optimized_code"]:
            return print_test_result(False, "优化代码为空")
        
        return print_test_result(True, "两数之和优化版题解测试通过")
    
    except Exception as e:
        return print_test_result(False, f"异常: {str(e)}")

def test_knapsack_optimized():
    """测试01背包 - 优化版题解"""
    print_test_title("01背包 - 优化版题解")
    
    payload = {
        "problem": "有N件物品和一个容量为V的背包。第i件物品的体积是c[i]，价值是w[i]。求解将哪些物品装入背包可使价值总和最大。",
        "language": "Python",
        "mode": "optimized"
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        
        if response.status_code != 200:
            return print_test_result(False, f"请求失败，状态码: {response.status_code}")
        
        data = response.json()
        if not data.get("success"):
            return print_test_result(False, f"生成失败: {data.get('message')}")
        
        result = data.get("data", {})
        
        # 验证字段完整性
        missing_fields = validate_optimized_response_fields(result)
        if missing_fields:
            return print_test_result(False, f"缺少字段: {', '.join(missing_fields)}")
        
        # 验证优化代码不为空
        if not result["optimized_code"]:
            return print_test_result(False, "优化代码为空")
        
        return print_test_result(True, "01背包优化版题解测试通过")
    
    except Exception as e:
        return print_test_result(False, f"异常: {str(e)}")

def test_longest_substring_standard():
    """测试最长无重复子串 - 标准题解"""
    print_test_title("最长无重复子串 - 标准题解")
    
    payload = {
        "problem": "给定一个字符串 s，请你找出其中不含有重复字符的最长子串的长度。",
        "language": "Python"
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        
        if response.status_code != 200:
            return print_test_result(False, f"请求失败，状态码: {response.status_code}")
        
        data = response.json()
        if not data.get("success"):
            return print_test_result(False, f"生成失败: {data.get('message')}")
        
        result = data.get("data", {})
        
        # 验证字段完整性
        missing_fields = validate_standard_response_fields(result)
        if missing_fields:
            return print_test_result(False, f"缺少字段: {', '.join(missing_fields)}")
        
        return print_test_result(True, "最长无重复子串标准题解测试通过")
    
    except Exception as e:
        return print_test_result(False, f"异常: {str(e)}")

def test_island_count_standard():
    """测试岛屿数量 - 标准题解"""
    print_test_title("岛屿数量 - 标准题解")
    
    payload = {
        "problem": "给你一个由 '1'（陆地）和 '0'（水）组成的的二维网格，请你计算网格中岛屿的数量。",
        "language": "Python"
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        
        if response.status_code != 200:
            return print_test_result(False, f"请求失败，状态码: {response.status_code}")
        
        data = response.json()
        if not data.get("success"):
            return print_test_result(False, f"生成失败: {data.get('message')}")
        
        result = data.get("data", {})
        
        # 验证字段完整性
        missing_fields = validate_standard_response_fields(result)
        if missing_fields:
            return print_test_result(False, f"缺少字段: {', '.join(missing_fields)}")
        
        return print_test_result(True, "岛屿数量标准题解测试通过")
    
    except Exception as e:
        return print_test_result(False, f"异常: {str(e)}")

def test_empty_problem():
    """测试空问题输入"""
    print_test_title("空问题输入")
    
    payload = {
        "problem": "",
        "language": "Python"
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        
        if response.status_code != 200:
            return print_test_result(False, f"请求失败，状态码: {response.status_code}")
        
        data = response.json()
        
        # 应该返回失败
        if not data.get("success"):
            return print_test_result(True, "空输入处理正确")
        
        return print_test_result(False, "空输入处理不正确")
    
    except Exception as e:
        return print_test_result(False, f"异常: {str(e)}")

def main():
    """运行所有测试"""
    print("\n" + "=" * 70)
    print("AI 算法题解生成器 - 综合测试套件")
    print("=" * 70 + "\n")
    
    results = []
    
    # 运行所有测试
    results.append(test_two_sum_standard())
    results.append(test_two_sum_optimized())
    results.append(test_knapsack_optimized())
    results.append(test_longest_substring_standard())
    results.append(test_island_count_standard())
    results.append(test_empty_problem())
    
    # 统计结果
    passed = sum(results)
    total = len(results)
    
    print("\n" + "=" * 70)
    print(f"测试结果统计: {passed}/{total} 通过")
    print("=" * 70)
    
    if passed < total:
        sys.exit(1)

if __name__ == "__main__":
    main()
