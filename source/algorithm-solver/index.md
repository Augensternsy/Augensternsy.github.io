---
title: AI 算法题解与复杂度分析生成器
date: 2024-01-01 00:00:00
type: page
layout: page
---

{% raw %}
<div class="algorithm-container">
    <h1 style="text-align:center; color:#007bff; margin-bottom:30px;">AI 算法题解与复杂度分析生成器</h1>

    <div class="card">
        <div style="margin-bottom: 15px; position: relative; z-index: 100;">
            <label style="display: block !important; margin-bottom: 5px; font-weight: bold;">算法题描述</label>
            <textarea id="problemInput" placeholder="请输入算法题目描述，例如：给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的两个整数，并返回它们的数组下标。" style="width: 100% !important; padding: 10px; border: 1px solid #ddd !important; border-radius: 4px; height: 100px; display: block !important; visibility: visible !important; opacity: 1 !important;"></textarea>
        </div>
        
        <div style="display: flex; gap: 15px; position: relative; z-index: 100;">
            <div style="flex: 1;">
                <label style="display: block !important; margin-bottom: 5px; font-weight: bold;">编程语言</label>
                <select id="languageSelect" style="width: 100% !important; padding: 10px; border: 1px solid #ddd !important; border-radius: 4px; height: 45px; background: white !important; color: #333; font-size: 14px; display: block !important; visibility: visible !important; opacity: 1 !important;">
                    <option value="Python">Python</option>
                    <option value="Java">Java</option>
                    <option value="C++">C++</option>
                    <option value="JavaScript">JavaScript</option>
                </select>
            </div>
        </div>

        <button id="solveBtn" style="width: 100% !important; padding: 12px; background: #007bff !important; color: white !important; border: none !important; border-radius: 4px; font-size: 16px; cursor: pointer; display: block !important; position: relative; z-index: 100;">🚀 生成题解</button>
        
        <div id="loading" style="display:none;" class="loading">
            <div>AI 正在分析题目...</div>
        </div>
    </div>

    <div id="error" style="display:none;" class="error">
        <strong>错误:</strong> <span id="errorMsg"></span>
    </div>

    <div id="result" style="display:none;" class="card">
        <h3 style="color:#007bff; margin-bottom:20px;">📝 题解结果</h3>
        
        <div class="result-section">
            <h4>🏷️ 题型识别</h4>
            <div id="problemType"></div>
        </div>

        <div class="result-section">
            <h4>📊 题目难度</h4>
            <div id="estimatedDifficulty" style="background:#ffc107; color:#333; padding:5px 10px; border-radius:4px; display:inline-block;"></div>
        </div>

        <div class="result-section">
            <h4>🤔 难度判断理由</h4>
            <p id="difficultyReason"></p>
        </div>

        <div class="result-section">
            <h4>💡 解题思路</h4>
            <p id="coreIdea"></p>
        </div>

        <div class="result-section">
            <h4>🗄️ 数据结构选择</h4>
            <p id="dataStructure"></p>
        </div>

        <div class="result-section">
            <h4>📋 步骤解析</h4>
            <ul id="steps"></ul>
        </div>

        <div class="result-section">
            <h4>💻 参考代码</h4>
            <div id="codeCard" class="code-card">
                <div class="code-card-header">
                    <span id="codeLanguage">Python</span>
                    <button id="copyCodeBtn" class="copy-btn" onclick="copyCode()">📋 复制代码</button>
                </div>
                <pre><code id="referenceCode"></code></pre>
            </div>
        </div>

        <div style="display: flex; gap: 20px;">
            <div class="result-section" style="flex: 1;">
                <h4>⏱️ 时间复杂度</h4>
                <div id="timeComplexity" style="background:#ffc107; color:#333; padding:5px 10px; border-radius:4px; display:inline-block;"></div>
            </div>
            <div class="result-section" style="flex: 1;">
                <h4>💾 空间复杂度</h4>
                <div id="spaceComplexity" style="background:#ffc107; color:#333; padding:5px 10px; border-radius:4px; display:inline-block;"></div>
            </div>
        </div>

        <div class="result-section">
            <h4>⚠️ 边界样例</h4>
            <ul id="edgeCases"></ul>
        </div>

        <div class="result-section">
            <h4>⚠️ 易错点</h4>
            <ul id="mistakes"></ul>
        </div>

        <div class="result-section">
            <h4>⬆️ 优化方案</h4>
            <p id="optimization"></p>
        </div>

        <div class="result-section" style="display:none;" id="ragSection">
            <h4>📚 参考算法模板</h4>
            <div id="ragContext" class="rag-context"></div>
        </div>
    </div>
</div>

<style>
.algorithm-container { max-width: 900px; margin: 0 auto; padding: 20px; position: relative; z-index: 10; }
.card { border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); background: white; }
.form-group { margin-bottom: 15px; display: block; }
label { display: block; margin-bottom: 5px; font-weight: bold; }
textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; display: block; }
textarea { height: 100px; }
select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; height: 45px; background: white; color: #333; font-size: 14px; display: block; }
button { width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; display: block; }
button:hover { background: #0056b3; }
.loading { text-align: center; color: #007bff; }
.error { background: #f8d7da; color: #721c24; padding: 10px; border-radius: 4px; }
.result-section { margin-bottom: 20px; }
.result-section h4 { color: #007bff; border-bottom: 2px solid #007bff; padding-bottom: 5px; }
ul { padding-left: 20px; }

/* 代码卡片样式 */
.code-card {
    margin-top: 16px;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #333;
    background: #1e1e1e;
}
.code-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #2d2d2d;
    color: #f8f8f2;
    padding: 10px 14px;
    font-size: 14px;
}
.code-card pre {
    margin: 0;
    padding: 16px;
    overflow-x: auto;
    background: #1e1e1e;
}
.code-card code {
    font-family: Consolas, Monaco, "Courier New", monospace;
    font-size: 14px;
    line-height: 1.7;
    color: #f8f8f2;
    white-space: pre;
}
.copy-btn {
    background: #4a4a4a !important;
    color: #fff !important;
    padding: 6px 12px !important;
    border-radius: 4px !important;
    font-size: 13px !important;
    width: auto !important;
    border: 1px solid #666 !important;
}
.copy-btn:hover {
    background: #666 !important;
}

/* RAG 上下文样式 */
.rag-context {
    background: #f5f5f5;
    padding: 12px 16px;
    border-radius: 6px;
    color: #666;
    font-size: 14px;
    line-height: 1.6;
    border-left: 3px solid #ccc;
}
</style>

<script>
let currentCode = '';

function copyCode() {
    const btn = document.getElementById('copyCodeBtn');
    if (!currentCode) {
        btn.textContent = '暂无代码';
        return;
    }
    
    navigator.clipboard.writeText(currentCode).then(() => {
        const oldText = btn.textContent;
        btn.textContent = '✅ 已复制';
        setTimeout(() => {
            btn.textContent = oldText;
        }, 1500);
    }).catch(err => {
        console.error('复制失败', err);
        btn.textContent = '复制失败';
        setTimeout(() => {
            btn.textContent = '📋 复制代码';
        }, 1500);
    });
}

window.addEventListener('DOMContentLoaded', function() {
    const PRODUCTION_API_BASE_URL = "https://augensternsy-github-io.vercel.app";
    const API_BASE_URL = location.hostname === "localhost" || location.hostname === "127.0.0.1"
        ? "http://127.0.0.1:8000"
        : PRODUCTION_API_BASE_URL;

    const solveBtn = document.getElementById('solveBtn');
    if (solveBtn) {
        solveBtn.addEventListener('click', function() {
            const problem = document.getElementById('problemInput').value.trim();
            const language = document.getElementById('languageSelect').value;

            if (!problem) {
                alert('请输入算法题描述');
                return;
            }

            solveBtn.style.display = 'none';
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            document.getElementById('error').style.display = 'none';

            const requestUrl = `${API_BASE_URL}/api/algorithm-solver`;
            console.log("API_BASE_URL:", API_BASE_URL);
            console.log("Request URL:", requestUrl);
            console.log("Request body:", { problem, language });

            fetch(requestUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ problem, language })
            })
            .then(response => {
                console.log("Response status:", response.status);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(response => {
                console.log("Response data:", response);
                if (!response.success) {
                    throw new Error(response.message || '生成失败');
                }
                const data = response.data;
                
                document.getElementById('problemType').textContent = data.problem_type?.join(', ') || '未知';
                document.getElementById('estimatedDifficulty').textContent = data.estimated_difficulty || '未知';
                document.getElementById('difficultyReason').textContent = data.difficulty_reason || '-';
                document.getElementById('coreIdea').textContent = data.core_idea || '-';
                document.getElementById('dataStructure').textContent = data.data_structure || '-';
                document.getElementById('timeComplexity').textContent = data.time_complexity || '-';
                document.getElementById('spaceComplexity').textContent = data.space_complexity || '-';
                document.getElementById('optimization').textContent = data.optimization || '-';
                
                const codeElement = document.getElementById('referenceCode');
                const languageElement = document.getElementById('codeLanguage');
                currentCode = data.reference_code || '';
                codeElement.textContent = currentCode || '暂无参考代码';
                languageElement.textContent = language;
                
                const steps = document.getElementById('steps');
                steps.innerHTML = '';
                (data.step_by_step_solution || []).forEach((step, i) => {
                    const li = document.createElement('li');
                    li.textContent = `步骤 ${i+1}: ${step}`;
                    steps.appendChild(li);
                });

                const edgeCases = document.getElementById('edgeCases');
                edgeCases.innerHTML = '';
                (data.edge_cases || []).forEach((ec, i) => {
                    const li = document.createElement('li');
                    li.textContent = `样例 ${i+1}: ${ec.input || ec}`;
                    edgeCases.appendChild(li);
                });

                const mistakes = document.getElementById('mistakes');
                mistakes.innerHTML = '';
                (data.common_mistakes || []).forEach((m, i) => {
                    const li = document.createElement('li');
                    li.textContent = `注意点 ${i+1}: ${m}`;
                    mistakes.appendChild(li);
                });

                const ragSection = document.getElementById('ragSection');
                const rag = document.getElementById('ragContext');
                if (data.rag_context && data.rag_context.trim()) {
                    let ragText = data.rag_context;
                    if (ragText.includes('未检索到') || ragText.includes('未匹配到')) {
                        ragText = '系统未匹配到强相关算法模板，本次基于通用算法知识生成。';
                    } else {
                        ragText = '系统参考了：' + ragText;
                    }
                    rag.textContent = ragText;
                    ragSection.style.display = 'block';
                } else {
                    ragSection.style.display = 'none';
                }

                document.getElementById('result').style.display = 'block';
            })
            .catch(err => {
                console.error("请求失败:", err);
                let errorMsg = err.message || '未知错误';
                if (err.message.includes('Failed to fetch') || err.message.includes('net::ERR')) {
                    errorMsg = '无法连接到API服务，请检查：\n1. Vercel后端是否已部署\n2. 网络连接是否正常\n3. API地址是否正确';
                }
                document.getElementById('errorMsg').textContent = errorMsg;
                document.getElementById('error').style.display = 'block';
            })
            .finally(() => {
                solveBtn.style.display = 'block';
                document.getElementById('loading').style.display = 'none';
            });
        });
    }
});
</script>
{% endraw %}
