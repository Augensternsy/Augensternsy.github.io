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

def validate_response_fields(data):
    """验证响应字段完整性"""
    required_fields = [
        "problem_type", "core_idea", "data_structure",
        "step_by_step_solution", "reference_code",
        "time_complexity", "space_complexity",
        "edge_cases", "common_mistakes", "optimization", "rag_context"
    ]
    
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
        elif data[field] is None:
            missing_fields.append(field)
    
    return missing_fields

def test_two_sum():
    """测试两数之和 - 数组 + 哈希表"""
    print_test_title("两数之和 - 数组 + 哈希表")
    
    payload = {
        "problem": "给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的两个整数，并返回它们的数组下标。你可以假设每种输入只会对应一个答案。但是，数组中同一个元素在答案里不能重复出现。你可以按任意顺序返回答案。",
        "language": "Python",
        "difficulty": "easy"
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
        missing_fields = validate_response_fields(result)
        if missing_fields:
            return print_test_result(False, f"缺少字段: {', '.join(missing_fields)}")
        
        # 验证题型识别
        if "数组" not in result["problem_type"] and "哈希表" not in result["problem_type"]:
            return print_test_result(False, f"题型识别错误: {result['problem_type']}")
        
        # 验证边界样例数量
        if len(result["edge_cases"]) < 3:
            return print_test_result(False, f"边界样例不足3个: {len(result['edge_cases'])}")
        
        # 验证代码不为空
        if not result["reference_code"]:
            return print_test_result(False, "参考代码为空")
        
        return print_test_result(True, "两数之和测试通过")
    
    except Exception as e:
        return print_test_result(False, f"异常: {str(e)}")

def test_longest_substring():
    """测试最长无重复子串 - 滑动窗口"""
    print_test_title("最长无重复子串 - 滑动窗口")
    
    payload = {
        "problem": "给定一个字符串 s，请你找出其中不含有重复字符的最长子串的长度。",
        "language": "Python",
        "difficulty": "medium"
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
        missing_fields = validate_response_fields(result)
        if missing_fields:
            return print_test_result(False, f"缺少字段: {', '.join(missing_fields)}")
        
        # 验证题型识别
        if "滑动窗口" not in result["problem_type"]:
            return print_test_result(False, f"题型识别错误: {result['problem_type']}")
        
        # 验证边界样例数量
        if len(result["edge_cases"]) < 3:
            return print_test_result(False, f"边界样例不足3个: {len(result['edge_cases'])}")
        
        return print_test_result(True, "最长无重复子串测试通过")
    
    except Exception as e:
        return print_test_result(False, f"异常: {str(e)}")

def test_climb_stairs():
    """测试爬楼梯 - 动态规划"""
    print_test_title("爬楼梯 - 动态规划")
    
    payload = {
        "problem": "假设你正在爬楼梯。需要 n 阶你才能到达楼顶。每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？",
        "language": "Python",
        "difficulty": "easy"
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
        missing_fields = validate_response_fields(result)
        if missing_fields:
            return print_test_result(False, f"缺少字段: {', '.join(missing_fields)}")
        
        # 验证题型识别
        if "动态规划" not in result["problem_type"]:
            return print_test_result(False, f"题型识别错误: {result['problem_type']}")
        
        # 验证边界样例数量
        if len(result["edge_cases"]) < 3:
            return print_test_result(False, f"边界样例不足3个: {len(result['edge_cases'])}")
        
        return print_test_result(True, "爬楼梯测试通过")
    
    except Exception as e:
        return print_test_result(False, f"异常: {str(e)}")

def test_island_count():
    """测试岛屿数量 - DFS / BFS"""
    print_test_title("岛屿数量 - DFS / BFS")
    
    payload = {
        "problem": "给你一个由 '1'（陆地）和 '0'（水）组成的的二维网格，请你计算网格中岛屿的数量。岛屿总是被水包围，并且每座岛屿只能由水平方向和/或竖直方向上相邻的陆地连接形成。此外，你可以假设该网格的四条边均被水包围。",
        "language": "Python",
        "difficulty": "medium"
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
        missing_fields = validate_response_fields(result)
        if missing_fields:
            return print_test_result(False, f"缺少字段: {', '.join(missing_fields)}")
        
        # 验证题型识别
        has_dfs_or_bfs = False
        for pt in result["problem_type"]:
            if "DFS" in pt or "BFS" in pt or "深度优先" in pt or "广度优先" in pt:
                has_dfs_or_bfs = True
                break
        if not has_dfs_or_bfs:
            return print_test_result(False, f"题型识别错误: {result['problem_type']}")
        
        # 验证边界样例数量
        if len(result["edge_cases"]) < 3:
            return print_test_result(False, f"边界样例不足3个: {len(result['edge_cases'])}")
        
        return print_test_result(True, "岛屿数量测试通过")
    
    except Exception as e:
        return print_test_result(False, f"异常: {str(e)}")

def test_empty_problem():
    """测试空问题输入"""
    print_test_title("空问题输入")
    
    payload = {
        "problem": "",
        "language": "Python",
        "difficulty": "easy"
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        
        if response.status_code != 200:
            return print_test_result(False, f"请求失败，状态码: {response.status_code}")
        
        data = response.json()
        
        # 应该成功返回但包含错误信息
        if data.get("success"):
            result = data.get("data", {})
            if "错误：题目描述不能为空" in result.get("core_idea", ""):
                return print_test_result(True, "空输入测试通过")
        
        return print_test_result(False, "空输入处理不正确")
    
    except Exception as e:
        return print_test_result(False, f"异常: {str(e)}")

def test_edge_cases_count():
    """测试边界样例数量"""
    print_test_title("边界样例数量验证")
    
    payload = {
        "problem": "给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的两个整数，并返回它们的数组下标。",
        "language": "Python",
        "difficulty": "easy"
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        
        if response.status_code != 200:
            return print_test_result(False, f"请求失败，状态码: {response.status_code}")
        
        data = response.json()
        if not data.get("success"):
            return print_test_result(False, f"生成失败: {data.get('message')}")
        
        result = data.get("data", {})
        
        # 验证边界样例数量 >= 3
        edge_cases = result.get("edge_cases", [])
        if len(edge_cases) >= 3:
            return print_test_result(True, f"边界样例数量: {len(edge_cases)} (>=3)")
        else:
            return print_test_result(False, f"边界样例数量不足: {len(edge_cases)}")
    
    except Exception as e:
        return print_test_result(False, f"异常: {str(e)}")

def main():
    """运行所有测试"""
    print("\n" + "=" * 70)
    print("AI 算法题解生成器 - 综合测试套件")
    print("=" * 70 + "\n")
    
    results = []
    
    # 运行所有测试
    results.append(test_two_sum())
    results.append(test_longest_substring())
    results.append(test_climb_stairs())
    results.append(test_island_count())
    results.append(test_empty_problem())
    results.append(test_edge_cases_count())
    
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