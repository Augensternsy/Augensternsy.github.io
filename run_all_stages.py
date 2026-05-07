# -*- coding: utf-8 -*-
"""
AI 测试工程师面试项目 - 四阶段统一运行入口

功能说明：
1. 第一阶段：RAG 向量检索基础（文档切片与 Embedding）
2. 第二阶段：结构化 Prompt 生成 JSON 用例（测试用例生成）
3. 第三阶段：对话记忆管理器（滑动窗口截断策略）
4. 第四阶段：HTML 到 Selenium 脚本生成器（自动化测试辅助）

环境变量配置：
- OPENAI_API_KEY: API 密钥
- OPENAI_BASE_URL: API 基础 URL
- MODEL_NAME: 模型名称
"""

import os
import sys
import subprocess
from datetime import datetime


# 颜色输出
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    print(f"\n{Colors.HEADER}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*70}{Colors.ENDC}\n")


def print_stage(stage_num, title):
    print(f"\n{Colors.BLUE}{'─'*70}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}第{stage_num}阶段：{title}{Colors.ENDC}")
    print(f"{Colors.BLUE}{'─'*70}{Colors.ENDC}\n")


def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")


def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")


def print_info(text):
    print(f"{Colors.YELLOW}ℹ {text}{Colors.ENDC}")


def run_stage(stage_name, script_path, args=None, env=None):
    """运行单个阶段脚本"""
    print_info(f"正在运行: {stage_name}")
    print_info(f"脚本路径: {script_path}")
    
    if not os.path.exists(script_path):
        print_error(f"脚本不存在: {script_path}")
        return False
    
    # 构建命令
    cmd = [sys.executable, script_path]
    if args:
        cmd.extend(args)
    
    # 合并环境变量
    run_env = os.environ.copy()
    if env:
        run_env.update(env)
    
    try:
        result = subprocess.run(
            cmd,
            env=run_env,
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print_success(f"{stage_name} 完成")
            return True
        else:
            print_error(f"{stage_name} 失败 (退出码: {result.returncode})")
            return False
            
    except Exception as e:
        print_error(f"{stage_name} 异常: {str(e)}")
        return False


def check_env():
    """检查环境变量配置"""
    print_header("环境检查")
    
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model_name = os.getenv("MODEL_NAME")
    
    if not api_key:
        print_error("未设置 OPENAI_API_KEY 环境变量")
        print_info("请设置: $env:OPENAI_API_KEY='your-api-key'")
        return False
    else:
        print_success(f"OPENAI_API_KEY: {api_key[:10]}...{api_key[-4:]}")
    
    if base_url:
        print_success(f"OPENAI_BASE_URL: {base_url}")
    else:
        print_info("OPENAI_BASE_URL 未设置，使用默认值")
    
    if model_name:
        print_success(f"MODEL_NAME: {model_name}")
    else:
        print_info("MODEL_NAME 未设置，使用默认值")
    
    return True


def run_all_stages():
    """运行所有四个阶段"""
    print_header("AI 测试工程师面试项目 - 四阶段完整演示")
    
    # 检查环境
    if not check_env():
        print_error("环境检查失败，请先配置环境变量")
        return False
    
    # 获取项目根目录
    project_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 环境变量配置
    env = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
        "OPENAI_BASE_URL": os.getenv("OPENAI_BASE_URL", "https://api.qnaigc.com/v1"),
        "MODEL_NAME": os.getenv("MODEL_NAME", "deepseek-v3")
    }
    
    results = {}
    
    # 第一阶段：RAG 向量检索基础
    print_stage(1, "RAG 向量检索基础（文档切片与 Embedding）")
    results["stage1"] = run_stage(
        "RAG 向量知识库构建",
        os.path.join(project_dir, "rag_knowledge_base.py"),
        env=env
    )
    
    # 第二阶段：结构化 Prompt 生成 JSON 用例
    print_stage(2, "结构化 Prompt 生成 JSON 用例（测试用例生成）")
    results["stage2"] = run_stage(
        "测试用例生成器",
        os.path.join(project_dir, "test_case_generator.py"),
        env=env
    )
    
    # 第三阶段：对话记忆管理器
    print_stage(3, "对话记忆管理器（滑动窗口截断策略）")
    results["stage3"] = run_stage(
        "对话记忆管理器",
        os.path.join(project_dir, "conversation_memory.py"),
        args=["--demo-memory"],
        env=env
    )
    
    # 第四阶段：HTML 到 Selenium 脚本生成器
    print_stage(4, "HTML 到 Selenium 脚本生成器（自动化测试辅助）")
    results["stage4"] = run_stage(
        "Selenium 脚本生成器",
        os.path.join(project_dir, "html_to_selenium.py"),
        args=["login"],
        env=env
    )
    
    # 汇总结果
    print_header("运行结果汇总")
    
    stage_names = {
        "stage1": "第一阶段：RAG 向量检索基础",
        "stage2": "第二阶段：JSON 用例生成",
        "stage3": "第三阶段：对话记忆管理",
        "stage4": "第四阶段：Selenium 脚本生成"
    }
    
    all_passed = True
    for key, name in stage_names.items():
        status = "成功" if results.get(key) else "失败"
        icon = "✓" if results.get(key) else "✗"
        color = Colors.GREEN if results.get(key) else Colors.RED
        print(f"  {color}{icon}{Colors.ENDC} {name}: {status}")
        if not results.get(key):
            all_passed = False
    
    print()
    if all_passed:
        print_success("所有阶段运行完成！")
    else:
        print_error("部分阶段运行失败，请检查日志")
    
    return all_passed


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AI 测试工程师面试项目 - 四阶段运行入口")
    parser.add_argument(
        "--stage",
        type=int,
        choices=[1, 2, 3, 4],
        help="运行指定阶段（1-4），不指定则运行全部"
    )
    
    args = parser.parse_args()
    
    if args.stage:
        # 运行单个阶段
        project_dir = os.path.dirname(os.path.abspath(__file__))
        env = {
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
            "OPENAI_BASE_URL": os.getenv("OPENAI_BASE_URL", "https://api.qnaigc.com/v1"),
            "MODEL_NAME": os.getenv("MODEL_NAME", "deepseek-v3")
        }
        
        stage_scripts = {
            1: ("rag_knowledge_base.py", []),
            2: ("test_case_generator.py", []),
            3: ("conversation_memory.py", ["--demo-memory"]),
            4: ("html_to_selenium.py", ["login"])
        }
        
        script, script_args = stage_scripts[args.stage]
        run_stage(f"第{args.stage}阶段", os.path.join(project_dir, script), script_args, env)
    else:
        # 运行全部阶段
        success = run_all_stages()
        sys.exit(0 if success else 1)
