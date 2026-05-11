---
title: AI 测试用例生成器
date: 2026-05-07 10:00:00
tags:
  - AI
  - 测试
  - 自动化工具
categories:
  - 工具
---

# AI 测试用例生成器

基于 RAG 与大语言模型的智能测试用例生成工具，只需输入测试需求，即可自动生成标准化的测试用例。

## 功能特点

- 🤖 **智能生成**：基于 RAG 检索增强生成技术
- 📋 **标准化输出**：生成符合规范的 JSON 格式测试用例
- 🔍 **上下文理解**：自动检索相关测试规范作为参考
- ⚡ **快速响应**：秒级生成高质量测试用例

## 使用方式

在下方输入框中输入你的测试需求，点击"生成测试用例"按钮即可。

{% raw %}
<!-- AI 测试用例生成器 - 博客插件 -->
<!-- 引入 Tailwind CSS -->
<script src="https://cdn.tailwindcss.com"></script>

<!-- 测试用例生成器容器 -->
<div id="test-case-generator" class="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
  <h2 class="text-2xl font-bold mb-4 text-gray-800">AI 测试用例生成器</h2>
  
  <!-- 输入区域 -->
  <div class="mb-4">
    <label for="requirement-input" class="block text-sm font-medium text-gray-700 mb-2">
      请输入测试需求
    </label>
    <textarea 
      id="requirement-input" 
      class="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
      rows="4"
      placeholder="例如：登录接口，包含用户名和密码"
    ></textarea>
  </div>
  
<div id="button-container"></div>
  
  <!-- 结果展示区域 -->
  <div id="result-container" class="mt-6 hidden">
    <h3 class="text-xl font-semibold mb-3 text-gray-800">生成的测试用例</h3>
    <div id="result-table" class="overflow-x-auto">
      <!-- 动态生成的表格将插入这里 -->
    </div>
  </div>
</div>

<!-- JavaScript 逻辑 -->
<script>
document.addEventListener('DOMContentLoaded', function() {
  // 配置后端 API 地址（Vercel 部署后替换为实际地址）
  const API_URL = 'https://augensternsy-github-io.vercel.app/api/generate_cases';
  
  // 获取 DOM 元素
  const inputEl = document.getElementById('requirement-input');
  const buttonContainer = document.getElementById('button-container');
  const resultContainer = document.getElementById('result-container');
  const resultTable = document.getElementById('result-table');
  
  // 检查元素是否存在
  if (!inputEl || !buttonContainer) {
    console.error('未找到必要的 DOM 元素');
    return;
  }
  
  // 动态创建按钮
  const btnEl = document.createElement('button');
  btnEl.id = 'generate-btn';
  btnEl.className = 'bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-md transition duration-200';
  btnEl.textContent = '生成测试用例';
  buttonContainer.appendChild(btnEl);
  
  // 绑定按钮点击事件
  btnEl.addEventListener('click', async function() {
    const requirement = inputEl.value.trim();
    
    // 验证输入
    if (!requirement) {
      alert('请输入测试需求');
      return;
    }
    
    // 显示加载状态
    btnEl.disabled = true;
    btnEl.textContent = '生成中...';
    resultContainer.classList.add('hidden');
    
    try {
      // 发送 POST 请求
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          requirement: requirement,
          top_k: 3
        })
      });
      
      // 检查响应状态
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      // 解析响应数据
      const data = await response.json();
      
      // 渲染结果
      renderTestCases(data);
      
    } catch (error) {
      console.error('生成测试用例失败:', error);
      alert('生成失败，请检查网络连接或后端服务是否正常运行');
    } finally {
      // 恢复按钮状态
      btnEl.disabled = false;
      btnEl.textContent = '生成测试用例';
    }
  });
  
  // 渲染测试用例表格
  function renderTestCases(data) {
    if (!data || !data.data || data.data.length === 0) {
      resultTable.innerHTML = '<p class="text-gray-500">未生成任何测试用例</p>';
      resultContainer.classList.remove('hidden');
      return;
    }
    
    const testCases = data.data;
    
    // 构建表格 HTML
    let tableHTML = `
      <table class="min-w-full bg-white border border-gray-300">
        <thead>
          <tr class="bg-gray-100">
            <th class="py-2 px-4 border-b text-left">用例编号</th>
            <th class="py-2 px-4 border-b text-left">测试场景</th>
            <th class="py-2 px-4 border-b text-left">预期结果</th>
          </tr>
        </thead>
        <tbody>
    `;
    
    // 添加每一行数据
    testCases.forEach(function(testCase) {
      tableHTML += `
        <tr class="hover:bg-gray-50">
          <td class="py-2 px-4 border-b">${testCase.case_id || '-'}</td>
          <td class="py-2 px-4 border-b">${testCase.test_point || '-'}</td>
          <td class="py-2 px-4 border-b">${testCase.expected_result || '-'}</td>
        </tr>
      `;
    });
    
    tableHTML += `
        </tbody>
      </table>
    `;
    
    // 插入表格
    resultTable.innerHTML = tableHTML;
    resultContainer.classList.remove('hidden');
  }
});
</script>

## 技术架构

本项目采用以下技术栈：

- **后端**：Python + FastAPI
- **AI 模型**：DeepSeek-V3 大语言模型
- **向量数据库**：ChromaDB
- **Embedding 模型**：BGE (BAAI/bge-base-zh-v1.5)
- **前端**：原生 HTML + CSS + JavaScript
- **部署**：Vercel Serverless

## 项目源码

项目已开源至 GitHub，欢迎 Star 和 Fork：

[GitHub 仓库地址](https://github.com/Augensternsy/Augensternsy.github.io)
