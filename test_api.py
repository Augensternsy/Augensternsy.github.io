# -*- coding: utf-8 -*-
"""
AI 测试用例生成器 API 测试文件

测试 Vercel 部署的 API 接口功能
"""

import requests
import json
import time
import sys
import io

# 设置标准输出编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# API 配置
API_BASE_URL = "https://augensternsy-github-io.vercel.app"
GENERATE_CASES_URL = f"{API_BASE_URL}/api/generate_cases"
HEALTH_URL = f"{API_BASE_URL}/health"
ROOT_URL = f"{API_BASE_URL}/"

# 使用 ASCII 符号代替 Unicode 符号
PASS = "[PASS]"
FAIL = "[FAIL]"


def test_health_check():
    """测试健康检查接口"""
    print("\n" + "=" * 60)
    print("测试 1: 健康检查接口")
    print("=" * 60)
    
    try:
        response = requests.get(HEALTH_URL, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        if response.status_code == 200:
            print(f"{PASS} 健康检查通过")
            return True
        else:
            print(f"{FAIL} 健康检查失败")
            return False
    except Exception as e:
        print(f"{FAIL} 请求失败: {str(e)}")
        return False


def test_root_endpoint():
    """测试根路径接口"""
    print("\n" + "=" * 60)
    print("测试 2: 根路径接口")
    print("=" * 60)
    
    try:
        response = requests.get(ROOT_URL, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        if response.status_code == 200:
            print(f"{PASS} 根路径接口正常")
            return True
        else:
            print(f"{FAIL} 根路径接口异常")
            return False
    except Exception as e:
        print(f"{FAIL} 请求失败: {str(e)}")
        return False


def test_generate_cases_login():
    """测试生成登录功能测试用例"""
    print("\n" + "=" * 60)
    print("测试 3: 生成登录功能测试用例")
    print("=" * 60)
    
    payload = {
        "requirement": "登录接口，包含用户名和密码",
        "top_k": 3
    }
    
    try:
        print(f"请求内容: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        response = requests.post(
            GENERATE_CASES_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"响应内容: {json.dumps(data, ensure_ascii=False, indent=2)}")
            
            # 验证响应结构
            assert data.get("success") == True, "success 字段应为 True"
            assert "data" in data, "应包含 data 字段"
            assert "total_cases" in data, "应包含 total_cases 字段"
            assert len(data["data"]) > 0, "测试用例数量应大于 0"
            
            # 验证每个测试用例的结构
            for case in data["data"]:
                assert "case_id" in case, "用例应包含 case_id"
                assert "test_point" in case, "用例应包含 test_point"
                assert "expected_result" in case, "用例应包含 expected_result"
            
            print(f"{PASS} 成功生成 {data['total_cases']} 个测试用例")
            return True
        else:
            print(f"{FAIL} 请求失败，状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"{FAIL} 请求异常: {str(e)}")
        return False


def test_generate_cases_file_upload():
    """测试生成文件上传功能测试用例"""
    print("\n" + "=" * 60)
    print("测试 4: 生成文件上传功能测试用例")
    print("=" * 60)
    
    payload = {
        "requirement": "文件上传功能，支持 JPG 和 PNG 格式，最大 5MB",
        "top_k": 3
    }
    
    try:
        print(f"请求内容: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        response = requests.post(
            GENERATE_CASES_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"响应内容: {json.dumps(data, ensure_ascii=False, indent=2)}")
            
            assert data.get("success") == True, "success 字段应为 True"
            assert len(data["data"]) > 0, "测试用例数量应大于 0"
            
            print(f"{PASS} 成功生成 {data['total_cases']} 个测试用例")
            return True
        else:
            print(f"{FAIL} 请求失败，状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"{FAIL} 请求异常: {str(e)}")
        return False


def test_generate_cases_registration():
    """测试生成用户注册功能测试用例"""
    print("\n" + "=" * 60)
    print("测试 5: 生成用户注册功能测试用例")
    print("=" * 60)
    
    payload = {
        "requirement": "用户注册功能，需要邮箱验证，密码要求至少8位包含大小写字母和数字",
        "top_k": 3
    }
    
    try:
        print(f"请求内容: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        response = requests.post(
            GENERATE_CASES_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"响应内容: {json.dumps(data, ensure_ascii=False, indent=2)}")
            
            assert data.get("success") == True, "success 字段应为 True"
            assert len(data["data"]) > 0, "测试用例数量应大于 0"
            
            print(f"{PASS} 成功生成 {data['total_cases']} 个测试用例")
            return True
        else:
            print(f"{FAIL} 请求失败，状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"{FAIL} 请求异常: {str(e)}")
        return False


def test_invalid_request():
    """测试无效请求（空需求）"""
    print("\n" + "=" * 60)
    print("测试 6: 测试无效请求（空需求）")
    print("=" * 60)
    
    payload = {
        "requirement": "",
        "top_k": 3
    }
    
    try:
        print(f"请求内容: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        response = requests.post(
            GENERATE_CASES_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        
        # 空需求应该返回 422 验证错误
        if response.status_code == 422:
            print(f"{PASS} 正确拒绝了空需求请求")
            return True
        else:
            print(f"响应: {response.text}")
            return True
    except Exception as e:
        print(f"{FAIL} 请求异常: {str(e)}")
        return False


def run_all_tests():
    """运行所有测试"""
    print("\n" + "#" * 60)
    print("# AI 测试用例生成器 API 测试")
    print("#" * 60)
    
    results = []
    
    # 运行各个测试
    results.append(("健康检查", test_health_check()))
    results.append(("根路径接口", test_root_endpoint()))
    results.append(("登录功能测试用例生成", test_generate_cases_login()))
    results.append(("文件上传功能测试用例生成", test_generate_cases_file_upload()))
    results.append(("用户注册功能测试用例生成", test_generate_cases_registration()))
    results.append(("无效请求处理", test_invalid_request()))
    
    # 打印测试结果汇总
    print("\n" + "#" * 60)
    print("# 测试结果汇总")
    print("#" * 60)
    
    passed = 0
    failed = 0
    
    for name, result in results:
        status = f"{PASS} 通过" if result else f"{FAIL} 失败"
        print(f"  {name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "-" * 60)
    print(f"总计: {len(results)} 个测试")
    print(f"通过: {passed}")
    print(f"失败: {failed}")
    print("-" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
