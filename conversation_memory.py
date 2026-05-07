# -*- coding: utf-8 -*-
"""
对话记忆管理器 - 滑动窗口截断策略

功能说明：
1. 管理多轮对话历史消息
2. 实现 Token 计数和消息过滤逻辑
3. 滑动窗口策略：超过 10 轮或 3000 tokens 时，自动丢弃最老的 4 轮对话
4. 保留 System Prompt 和最新对话上下文
5. 防止 LLM Token 撑爆

依赖安装：
pip install openai tiktoken
"""

import os
import json
import time
from typing import List, Dict, Optional
from openai import OpenAI
import tiktoken


class ConversationMemory:
    """
    对话记忆管理器 - 实现滑动窗口截断策略
    
    核心功能：
    - 管理对话历史消息列表
    - Token 计数和估算
    - 自动截断过期消息
    - 保留 System Prompt
    """
    
    def __init__(
        self,
        system_prompt: str = "",
        max_rounds: int = 10,
        max_tokens: int = 3000,
        truncate_rounds: int = 4,
        model: str = "gpt-3.5-turbo"
    ):
        """
        初始化对话记忆管理器
        
        参数:
            system_prompt: 系统提示词（始终保留）
            max_rounds: 最大对话轮数阈值
            max_tokens: 最大 Token 数阈值
            truncate_rounds: 每次截断的轮数
            model: 用于 Token 计数的模型名称
        """
        self.system_prompt = system_prompt
        self.max_rounds = max_rounds
        self.max_tokens = max_tokens
        self.truncate_rounds = truncate_rounds
        self.model = model
        
        # 对话历史消息列表
        self.messages: List[Dict[str, str]] = []
        
        # 初始化 Token 编码器
        try:
            self.encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            # 如果模型不支持，使用默认编码器
            self.encoding = tiktoken.get_encoding("cl100k_base")
        
        # 统计信息
        self.stats = {
            "total_messages": 0,
            "total_truncations": 0,
            "total_tokens_used": 0
        }
        
        print(f"对话记忆管理器初始化完成")
        print(f"  最大轮数: {max_rounds}")
        print(f"  最大 Token: {max_tokens}")
        print(f"  截断轮数: {truncate_rounds}")
        print(f"  模型: {model}")
    
    def add_message(self, role: str, content: str):
        """
        添加一条消息到对话历史
        
        参数:
            role: 消息角色（system/user/assistant）
            content: 消息内容
        """
        message = {"role": role, "content": content}
        self.messages.append(message)
        self.stats["total_messages"] += 1
        
        print(f"  [添加消息] {role}: {content[:50]}...")
    
    def count_tokens(self, messages: List[Dict[str, str]] = None) -> int:
        """
        计算消息列表的 Token 数量
        
        参数:
            messages: 要计算的消息列表（默认使用当前历史）
        
        返回:
            token_count: Token 总数
        """
        if messages is None:
            messages = self.messages
        
        token_count = 0
        for msg in messages:
            # 计算角色和内容的 Token
            token_count += len(self.encoding.encode(msg.get("role", "")))
            token_count += len(self.encoding.encode(msg.get("content", "")))
            # 每条消息额外加 4 个 token（OpenAI 的格式开销）
            token_count += 4
        
        return token_count
    
    def count_rounds(self) -> int:
        """
        计算当前对话轮数（user + assistant 为一轮）
        
        返回:
            rounds: 对话轮数
        """
        # 统计 user 消息的数量即为轮数
        user_count = sum(1 for msg in self.messages if msg["role"] == "user")
        return user_count
    
    def should_truncate(self) -> bool:
        """
        判断是否需要截断
        
        返回:
            bool: 是否需要截断
        """
        current_rounds = self.count_rounds()
        current_tokens = self.count_tokens()
        
        needs_truncate = (
            current_rounds > self.max_rounds or 
            current_tokens > self.max_tokens
        )
        
        if needs_truncate:
            print(f"\n  [触发截断条件]")
            print(f"    当前轮数: {current_rounds} / {self.max_rounds}")
            print(f"    当前 Token: {current_tokens} / {self.max_tokens}")
        
        return needs_truncate
    
    def truncate(self) -> List[Dict[str, str]]:
        """
        执行截断操作 - 滑动窗口策略
        
        核心逻辑：
        1. 保留 System Prompt
        2. 丢弃最老的 truncate_rounds 轮对话
        3. 保留最新的对话上下文
        
        返回:
            truncated_messages: 截断后的消息列表
        """
        print(f"\n  [执行截断] 丢弃最老的 {self.truncate_rounds} 轮对话...")
        
        # 分离 System Prompt 和其他消息
        system_messages = [msg for msg in self.messages if msg["role"] == "system"]
        other_messages = [msg for msg in self.messages if msg["role"] != "system"]
        
        # 计算要保留的消息数量
        # 每轮包含 user + assistant 两条消息
        messages_to_remove = self.truncate_rounds * 2
        
        # 如果消息不够截断，保留所有
        if len(other_messages) <= messages_to_remove:
            print(f"    消息数量不足，保留所有消息")
            return self.messages
        
        # 保留最新的消息
        retained_messages = other_messages[messages_to_remove:]
        
        # 重新组合：System Prompt + 保留的消息
        self.messages = system_messages + retained_messages
        
        self.stats["total_truncations"] += 1
        
        # 打印截断后的状态
        new_rounds = self.count_rounds()
        new_tokens = self.count_tokens()
        print(f"    截断后轮数: {new_rounds}")
        print(f"    截断后 Token: {new_tokens}")
        
        return self.messages
    
    def get_messages(self) -> List[Dict[str, str]]:
        """
        获取当前消息列表（自动检查并执行截断）
        
        返回:
            messages: 处理后的消息列表
        """
        # 检查是否需要截断
        if self.should_truncate():
            self.truncate()
        
        # 更新统计信息
        self.stats["total_tokens_used"] = self.count_tokens()
        
        return self.messages
    
    def get_stats(self) -> Dict:
        """
        获取统计信息
        
        返回:
            stats: 统计信息字典
        """
        self.stats["current_rounds"] = self.count_rounds()
        self.stats["current_tokens"] = self.count_tokens()
        self.stats["current_messages"] = len(self.messages)
        return self.stats
    
    def clear(self):
        """清空对话历史（保留 System Prompt）"""
        system_messages = [msg for msg in self.messages if msg["role"] == "system"]
        self.messages = system_messages
        print("  [清空对话历史]")
    
    def export_history(self, filename: str = None) -> str:
        """
        导出对话历史到文件
        
        参数:
            filename: 输出文件名
        
        返回:
            filepath: 保存的文件路径
        """
        if filename is None:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_history_{timestamp}.json"
        
        export_data = {
            "system_prompt": self.system_prompt,
            "messages": self.messages,
            "stats": self.get_stats()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n  [导出历史] 已保存到: {filename}")
        return filename


class ChatAgent:
    """
    带记忆功能的对话 Agent
    
    集成 ConversationMemory 实现多轮对话
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        system_prompt: str = "你是一个 helpful 的 AI 助手。",
        max_rounds: int = 10,
        max_tokens: int = 3000
    ):
        """
        初始化对话 Agent
        
        参数:
            api_key: API 密钥
            base_url: API 基础 URL
            model: 模型名称
            system_prompt: 系统提示词
            max_rounds: 最大对话轮数
            max_tokens: 最大 Token 数
        """
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model
        
        # 初始化对话记忆
        self.memory = ConversationMemory(
            system_prompt=system_prompt,
            max_rounds=max_rounds,
            max_tokens=max_tokens
        )
        
        # 添加 System Prompt
        if system_prompt:
            self.memory.add_message("system", system_prompt)
    
    def chat(self, user_input: str) -> str:
        """
        发送消息并获取回复
        
        参数:
            user_input: 用户输入
        
        返回:
            response: AI 回复
        """
        print(f"\n{'='*60}")
        print(f"用户: {user_input}")
        print(f"{'='*60}")
        
        # 添加用户消息
        self.memory.add_message("user", user_input)
        
        # 获取处理后的消息列表（自动截断）
        messages = self.memory.get_messages()
        
        # 打印当前状态
        stats = self.memory.get_stats()
        print(f"\n  [当前状态]")
        print(f"    消息数: {stats['current_messages']}")
        print(f"    对话轮数: {stats['current_rounds']}")
        print(f"    Token 数: {stats['current_tokens']}")
        print(f"    截断次数: {stats['total_truncations']}")
        
        # 调用 LLM
        print(f"\n  [调用 LLM] 模型: {self.model}")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            assistant_reply = response.choices[0].message.content
            
            # 添加 AI 回复到历史
            self.memory.add_message("assistant", assistant_reply)
            
            print(f"\nAI: {assistant_reply}")
            return assistant_reply
            
        except Exception as e:
            error_msg = f"调用失败: {str(e)}"
            print(f"\n错误: {error_msg}")
            return error_msg
    
    def export_history(self, filename: str = None) -> str:
        """导出对话历史"""
        return self.memory.export_history(filename)


def demo_conversation():
    """
    演示多轮对话和滑动窗口截断功能
    """
    print("=" * 60)
    print("对话记忆管理器 - 滑动窗口截断策略 Demo")
    print("=" * 60)
    
    # 从环境变量读取配置
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.qnaigc.com/v1")
    model = os.getenv("MODEL_NAME", "deepseek-v3")
    
    if not api_key:
        print("\n错误: 未设置 OPENAI_API_KEY 环境变量")
        print("请先配置环境变量后运行")
        return
    
    # 系统提示词
    system_prompt = """你是一个测试专家助手。请帮助用户解答软件测试相关的问题，
包括测试方法、测试用例设计、测试流程等。回答要简洁明了。"""
    
    # 创建 Agent（设置较小的阈值以便演示截断）
    agent = ChatAgent(
        api_key=api_key,
        base_url=base_url,
        model=model,
        system_prompt=system_prompt,
        max_rounds=5,      # 演示用：设置为 5 轮
        max_tokens=2000    # 演示用：设置为 2000 tokens
    )
    
    # 测试对话列表
    test_conversations = [
        "什么是等价类划分法？",
        "能举个例子说明吗？",
        "边界值分析和等价类划分有什么区别？",
        "测试用例应该包含哪些要素？",
        "如何设计登录功能的测试用例？",
        "性能测试和负载测试有什么区别？",
        "自动化测试适合哪些场景？",
        "回归测试的目的是什么？",
        "黑盒测试和白盒测试的区别？",
        "如何评估测试覆盖率？",
        "持续集成中的测试策略是什么？",
        "DevOps 中测试的角色是什么？"
    ]
    
    print(f"\n开始多轮对话测试（共 {len(test_conversations)} 轮）...")
    print(f"配置: 最大 {agent.memory.max_rounds} 轮 / {agent.memory.max_tokens} tokens")
    print(f"      超过阈值将截断最老的 {agent.memory.truncate_rounds} 轮\n")
    
    # 执行对话
    for i, question in enumerate(test_conversations, 1):
        print(f"\n{'#'*60}")
        print(f"第 {i} 轮对话")
        print(f"{'#'*60}")
        
        agent.chat(question)
        
        # 每轮之间稍作延迟
        time.sleep(0.5)
    
    # 导出对话历史
    print(f"\n{'='*60}")
    print("对话结束，导出历史记录")
    print(f"{'='*60}")
    
    filepath = agent.export_history()
    
    # 打印最终统计
    print(f"\n{'='*60}")
    print("最终统计信息")
    print(f"{'='*60}")
    stats = agent.memory.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")


def demo_memory_only():
    """
    仅演示记忆管理器的功能（不调用 LLM）
    """
    print("=" * 60)
    print("对话记忆管理器 - 纯功能演示（不调用 LLM）")
    print("=" * 60)
    
    # 创建记忆管理器
    memory = ConversationMemory(
        system_prompt="你是一个测试专家助手。",
        max_rounds=5,
        max_tokens=2000,
        truncate_rounds=2
    )
    
    # 添加 System Prompt
    memory.add_message("system", memory.system_prompt)
    
    # 模拟多轮对话
    conversations = [
        ("user", "什么是等价类划分？"),
        ("assistant", "等价类划分是一种黑盒测试方法..."),
        ("user", "能举个例子吗？"),
        ("assistant", "比如输入框要求 1-100..."),
        ("user", "边界值分析呢？"),
        ("assistant", "边界值分析关注边界条件..."),
        ("user", "两者有什么区别？"),
        ("assistant", "等价类划分关注区间..."),
        ("user", "如何设计测试用例？"),
        ("assistant", "测试用例应包含..."),
        ("user", "性能测试怎么做？"),
        ("assistant", "性能测试需要..."),
        ("user", "自动化测试适合什么场景？"),
        ("assistant", "自动化测试适合..."),
    ]
    
    print(f"\n模拟 {len(conversations)//2} 轮对话...\n")
    
    for role, content in conversations:
        memory.add_message(role, content)
        
        # 获取消息（自动检查截断）
        messages = memory.get_messages()
        
        # 打印状态
        stats = memory.get_stats()
        print(f"  轮数: {stats['current_rounds']:2d} | "
              f"Token: {stats['current_tokens']:4d} | "
              f"消息: {stats['current_messages']:2d} | "
              f"截断: {stats['total_truncations']}")
    
    # 导出历史
    print(f"\n导出对话历史...")
    memory.export_history("demo_memory_history.json")
    
    # 打印最终状态
    print(f"\n最终消息列表:")
    for i, msg in enumerate(memory.messages):
        preview = msg['content'][:30] + "..." if len(msg['content']) > 30 else msg['content']
        print(f"  [{i}] {msg['role']}: {preview}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--demo-memory":
        # 仅演示记忆管理器
        demo_memory_only()
    else:
        # 完整演示（调用 LLM）
        demo_conversation()
