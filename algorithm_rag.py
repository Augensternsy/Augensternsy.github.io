# -*- coding: utf-8 -*-
"""
轻量级向量检索式 RAG 模块

功能：
1. 读取算法题型知识库
2. 文档切分
3. 使用 OpenAI Embedding API 向量化
4. 余弦相似度 Top-K 检索
5. 关键词检索兜底

不依赖外部向量数据库，使用纯 Python 实现。
"""

import os
import re
import json
import numpy as np
from typing import List, Dict, Tuple, Optional
from openai import OpenAI


class AlgorithmRAG:
    """轻量级算法题型知识库检索器"""
    
    def __init__(self, knowledge_base_path: str = "docs/算法题型知识库.md"):
        """
        初始化 RAG 检索器
        
        参数:
            knowledge_base_path: 知识库文件路径
        """
        self.knowledge_base_path = knowledge_base_path
        self.chunks: List[Dict] = []
        self.embeddings: Optional[np.ndarray] = None
        self.keyword_index: Dict[str, List[int]] = {}
        
        # 关键词映射表（用于兜底）
        self.keyword_map = {
            "两数之和": ["数组与哈希表"],
            "三数之和": ["数组与哈希表", "双指针与排序"],
            "01背包": ["动态规划 - 背包问题"],
            "背包": ["动态规划 - 背包问题"],
            "最长无重复子串": ["滑动窗口", "数组与哈希表"],
            "岛屿数量": ["图论 - DFS与BFS"],
            "接雨水": ["栈与单调栈", "双指针与排序"],
            "动态规划": ["动态规划 - 其他问题"],
            "DFS": ["图论 - DFS与BFS"],
            "BFS": ["图论 - DFS与BFS"],
            "二叉树": ["树与二叉树"],
            "链表": ["链表操作"],
            "滑动窗口": ["滑动窗口"],
            "双指针": ["双指针与排序"],
            "单调栈": ["栈与单调栈"],
            "二分查找": ["二分查找"],
            "贪心": ["贪心算法"]
        }
        
        # 初始化 OpenAI 客户端
        api_key = os.getenv("OPENAI_API_KEY")
        api_base = os.getenv("OPENAI_BASE_URL", "https://api.qnaigc.com/v1")
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        
        self.client = None
        if api_key:
            self.client = OpenAI(api_key=api_key, base_url=api_base)
        
        # 加载知识库
        self._load_knowledge_base()
    
    def _load_knowledge_base(self):
        """加载并切分知识库"""
        try:
            if not os.path.exists(self.knowledge_base_path):
                print(f"警告: 知识库文件不存在: {self.knowledge_base_path}")
                return
            
            with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 按标题切分文档
            self.chunks = self._split_by_headings(content)
            
            # 构建关键词索引
            self._build_keyword_index()
            
            # 尝试生成 Embeddings
            if self.client:
                self._generate_embeddings()
            
            print(f"知识库加载成功，共 {len(self.chunks)} 个文档块")
            
        except Exception as e:
            print(f"知识库加载失败: {e}")
    
    def _split_by_headings(self, content: str) -> List[Dict]:
        """
        按 Markdown 标题切分文档
        
        参数:
            content: Markdown 文本内容
            
        返回:
            文档块列表
        """
        chunks = []
        
        # 匹配二级标题 (##) 作为块的开始
        pattern = r'##\s+([^\n]+)\n([\s\S]*?)(?=##|$)'
        matches = re.findall(pattern, content)
        
        for title, body in matches:
            title = title.strip()
            body = body.strip()
            
            if body:
                chunks.append({
                    "title": title,
                    "content": body,
                    "full_text": f"## {title}\n{body}"
                })
        
        return chunks
    
    def _build_keyword_index(self):
        """构建关键词索引（用于兜底检索）"""
        for i, chunk in enumerate(self.chunks):
            title = chunk["title"]
            content = chunk["content"]
            
            # 提取关键词（标题 + 典型题目）
            keywords = []
            keywords.extend(re.findall(r'[^\s，、]+', title))
            
            # 从典型题目中提取
            problems_match = re.search(r'### 典型题目\n([\s\S]*?)(?=###|$)', content)
            if problems_match:
                problems = problems_match.group(1)
                keywords.extend(re.findall(r'- (.+)', problems))
            
            # 建立关键词到文档索引的映射
            for keyword in keywords:
                keyword = keyword.strip()
                if keyword:
                    if keyword not in self.keyword_index:
                        self.keyword_index[keyword] = []
                    self.keyword_index[keyword].append(i)
    
    def _generate_embeddings(self):
        """使用 OpenAI Embedding API 生成向量"""
        try:
            if not self.chunks:
                return
            
            print("正在生成 Embeddings...")
            
            # 提取所有块的文本
            texts = [chunk["full_text"] for chunk in self.chunks]
            
            # 批量生成 Embeddings
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=texts
            )
            
            # 提取向量
            self.embeddings = np.array([
                item.embedding for item in response.data
            ])
            
            print(f"Embeddings 生成成功，共 {len(self.embeddings)} 个向量")
            
        except Exception as e:
            print(f"Embedding 生成失败: {e}")
            self.embeddings = None
    
    def _get_embedding(self, text: str) -> Optional[np.ndarray]:
        """获取单个文本的 Embedding"""
        try:
            if not self.client:
                return None
            
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            return np.array(response.data[0].embedding)
            
        except Exception as e:
            print(f"获取 Embedding 失败: {e}")
            return None
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """计算余弦相似度"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        return dot_product / (norm1 * norm2)
    
    def _semantic_search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        语义检索（使用 Embeddings）
        
        参数:
            query: 查询文本
            top_k: 返回的文档数量
            
        返回:
            相关文档块列表
        """
        if self.embeddings is None or self.client is None:
            return []
        
        try:
            # 获取查询 Embedding
            query_embedding = self._get_embedding(query)
            if query_embedding is None:
                return []
            
            # 计算相似度
            similarities = []
            for i, chunk_embedding in enumerate(self.embeddings):
                sim = self._cosine_similarity(query_embedding, chunk_embedding)
                similarities.append((sim, i))
            
            # 排序并取 Top-K
            similarities.sort(key=lambda x: x[0], reverse=True)
            top_indices = [idx for sim, idx in similarities[:top_k]]
            
            results = []
            for idx in top_indices:
                chunk = self.chunks[idx]
                results.append({
                    "title": chunk["title"],
                    "content": chunk["content"],
                    "similarity": float(similarities[top_indices.index(idx)][0])
                })
            
            return results
            
        except Exception as e:
            print(f"语义检索失败: {e}")
            return []
    
    def _keyword_search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        关键词检索（兜底策略）
        
        参数:
            query: 查询文本
            top_k: 返回的文档数量
            
        返回:
            相关文档块列表
        """
        # 首先查询预定义的关键词映射
        for keyword, templates in self.keyword_map.items():
            if keyword in query:
                # 找到对应的模板标题
                for template in templates:
                    for i, chunk in enumerate(self.chunks):
                        if chunk["title"] == template:
                            return [{
                                "title": chunk["title"],
                                "content": chunk["content"],
                                "similarity": 1.0
                            }]
        
        # 否则进行简单关键词匹配
        query_keywords = re.findall(r'[^\s，、。]+', query)
        score = [0] * len(self.chunks)
        
        for keyword in query_keywords:
            if keyword in self.keyword_index:
                for idx in self.keyword_index[keyword]:
                    score[idx] += 1
        
        # 排序
        scored_indices = [(score[i], i) for i in range(len(self.chunks))]
        scored_indices.sort(key=lambda x: x[0], reverse=True)
        
        results = []
        for s, idx in scored_indices[:top_k]:
            if s > 0:
                chunk = self.chunks[idx]
                results.append({
                    "title": chunk["title"],
                    "content": chunk["content"],
                    "similarity": s / max(len(query_keywords), 1)
                })
        
        return results
    
    def search(self, query: str, top_k: int = 3, use_semantic: bool = True) -> Tuple[List[Dict], str]:
        """
        检索相关算法模板
        
        参数:
            query: 查询文本（算法题描述）
            top_k: 返回的文档数量
            use_semantic: 是否使用语义检索（False 则只用关键词）
            
        返回:
            (检索结果列表, 检索方法: "semantic" | "keyword" | "none")
        """
        if not self.chunks:
            return [], "none"
        
        # 优先使用语义检索
        if use_semantic and self.embeddings is not None and self.client is not None:
            results = self._semantic_search(query, top_k)
            if results:
                return results, "semantic"
        
        # 兜底使用关键词检索
        results = self._keyword_search(query, top_k)
        if results:
            return results, "keyword"
        
        return [], "none"
    
    def get_rag_context(self, query: str) -> Tuple[str, str]:
        """
        获取 RAG 上下文（用于 Prompt 注入）
        
        参数:
            query: 查询文本
            
        返回:
            (上下文文本, 模板名称)
        """
        results, method = self.search(query, top_k=2)
        
        if not results:
            return "", ""
        
        # 构建上下文文本
        context_parts = []
        template_names = []
        
        for result in results:
            context_parts.append(f"## {result['title']}\n{result['content']}")
            template_names.append(result['title'])
        
        context = "\n\n---\n\n".join(context_parts)
        template_str = "、".join(template_names)
        
        return context, template_str


# 全局 RAG 实例（单例模式）
_rag_instance: Optional[AlgorithmRAG] = None


def get_rag() -> AlgorithmRAG:
    """获取 RAG 实例（懒加载）"""
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = AlgorithmRAG()
    return _rag_instance


if __name__ == "__main__":
    # 测试 RAG
    rag = AlgorithmRAG()
    
    test_queries = [
        "两数之和",
        "01背包问题",
        "最长无重复子串",
        "岛屿数量",
        "接雨水"
    ]
    
    for query in test_queries:
        print(f"\n查询: {query}")
        print("=" * 50)
        
        context, template = rag.get_rag_context(query)
        
        if template:
            print(f"匹配模板: {template}")
            print(f"上下文长度: {len(context)} 字符")
        else:
            print("未匹配到模板")
