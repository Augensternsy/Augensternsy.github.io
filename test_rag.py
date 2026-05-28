# -*- coding: utf-8 -*-
"""
测试 RAG 检索模块
"""

from algorithm_rag import AlgorithmRAG


def test_rag():
    """测试 RAG 功能"""
    print("=" * 60)
    print("测试 RAG 检索模块")
    print("=" * 60)
    
    # 初始化 RAG（由于没有 OpenAI API Key，将使用关键词兜底）
    print("\n初始化 RAG...")
    rag = AlgorithmRAG()
    
    # 测试题目
    test_cases = [
        "两数之和",
        "01背包问题",
        "最长无重复子串",
        "岛屿数量",
        "接雨水"
    ]
    
    for query in test_cases:
        print(f"\n查询: {query}")
        print("-" * 50)
        
        # 检索（强制使用关键词检索，因为可能没有 API Key）
        results, method = rag.search(query, top_k=2, use_semantic=False)
        
        if results:
            print(f"检索方法: {method}")
            print(f"匹配到 {len(results)} 个相关文档:")
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result['title']} (相似度: {result['similarity']:.2f})")
            
            # 测试获取上下文
            context, template = rag.get_rag_context(query)
            print(f"\n模板名称: {template}")
            print(f"上下文长度: {len(context)} 字符")
        else:
            print("未找到相关文档")
    
    print("\n" + "=" * 60)
    print("RAG 测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    test_rag()
