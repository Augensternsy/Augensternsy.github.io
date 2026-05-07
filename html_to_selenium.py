# -*- coding: utf-8 -*-
"""
HTML 到 Selenium 脚本生成器

功能说明：
1. 接收 HTML DOM 结构字符串
2. 使用结构化 Prompt 调用大模型
3. 生成基于 Python + Selenium 的 UI 自动化测试脚本
4. 脚本包含 WebDriverWait 显式等待和基础断言
5. 优先使用 id，其次是 name 或 class 定位元素

依赖安装：
pip install openai beautifulsoup4
"""

import os
import re
from typing import Optional
from openai import OpenAI
from bs4 import BeautifulSoup


class SeleniumScriptGenerator:
    """
    HTML 到 Selenium 脚本生成器
    
    核心功能：
    - 解析 HTML DOM 结构
    - 提取具有唯一标识的元素
    - 生成带显式等待的 Selenium 测试脚本
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        timeout: int = 10
    ):
        """
        初始化脚本生成器
        
        参数:
            api_key: API 密钥
            base_url: API 基础 URL
            model: 模型名称
            timeout: 显式等待超时时间（秒）
        """
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model
        self.timeout = timeout
        
        print(f"Selenium 脚本生成器初始化完成")
        print(f"  模型: {model}")
        print(f"  超时时间: {timeout} 秒")
    
    def extract_element_info(self, html_content: str) -> str:
        """
        使用 BeautifulSoup 预处理 HTML，提取元素信息
        
        参数:
            html_content: HTML 字符串
        
        返回:
            element_summary: 元素信息摘要
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 提取关键元素信息
        elements = []
        
        # 查找 input 元素
        for input_tag in soup.find_all('input'):
            elem_info = {
                'tag': 'input',
                'type': input_tag.get('type', 'text'),
                'id': input_tag.get('id'),
                'name': input_tag.get('name'),
                'class': input_tag.get('class', []),
                'placeholder': input_tag.get('placeholder'),
            }
            elements.append(elem_info)
        
        # 查找 button 元素
        for button_tag in soup.find_all('button'):
            elem_info = {
                'tag': 'button',
                'id': button_tag.get('id'),
                'name': button_tag.get('name'),
                'class': button_tag.get('class', []),
                'text': button_tag.get_text(strip=True),
            }
            elements.append(elem_info)
        
        # 查找 a 链接元素
        for a_tag in soup.find_all('a'):
            elem_info = {
                'tag': 'a',
                'id': a_tag.get('id'),
                'name': a_tag.get('name'),
                'class': a_tag.get('class', []),
                'href': a_tag.get('href'),
                'text': a_tag.get_text(strip=True),
            }
            elements.append(elem_info)
        
        # 查找其他可交互元素
        for select_tag in soup.find_all('select'):
            elem_info = {
                'tag': 'select',
                'id': select_tag.get('id'),
                'name': select_tag.get('name'),
                'class': select_tag.get('class', []),
            }
            elements.append(elem_info)
        
        for textarea_tag in soup.find_all('textarea'):
            elem_info = {
                'tag': 'textarea',
                'id': textarea_tag.get('id'),
                'name': textarea_tag.get('name'),
                'class': textarea_tag.get('class', []),
                'placeholder': textarea_tag.get('placeholder'),
            }
            elements.append(elem_info)
        
        # 生成元素摘要
        summary_lines = ["HTML 元素分析结果：\n"]
        
        for i, elem in enumerate(elements, 1):
            summary_lines.append(f"元素 {i}:")
            summary_lines.append(f"  标签: <{elem['tag']}>")
            
            if elem.get('type'):
                summary_lines.append(f"  类型: {elem['type']}")
            
            if elem.get('id'):
                summary_lines.append(f"  ID: {elem['id']}")
            
            if elem.get('name'):
                summary_lines.append(f"  Name: {elem['name']}")
            
            if elem.get('class'):
                summary_lines.append(f"  Class: {' '.join(elem['class'])}")
            
            if elem.get('placeholder'):
                summary_lines.append(f"  Placeholder: {elem['placeholder']}")
            
            if elem.get('text'):
                summary_lines.append(f"  文本: {elem['text']}")
            
            if elem.get('href'):
                summary_lines.append(f"  链接: {elem['href']}")
            
            summary_lines.append("")
        
        return "\n".join(summary_lines)
    
    def build_prompt(self, html_content: str, element_info: str) -> str:
        """
        构建结构化 Prompt
        
        参数:
            html_content: 原始 HTML 内容
            element_info: 元素信息摘要
        
        返回:
            prompt: 完整的提示词
        """
        prompt = f"""你是一个资深 UI 自动化测试工程师，精通 Python + Selenium 自动化测试。

## 任务
请分析提供的 HTML DOM 结构，生成一段完整的 Python + Selenium UI 自动化测试脚本。

## HTML 结构
```html
{html_content}
```

## 元素分析
{element_info}

## 要求

### 1. 元素定位策略（按优先级）
- 优先使用 `id` 定位（By.ID）
- 其次使用 `name` 定位（By.NAME）
- 最后使用 `class` 或 `css_selector` 定位

### 2. 显式等待
- 必须使用 WebDriverWait 进行显式等待
- 等待条件使用 expected_conditions
- 超时时间设置为 {self.timeout} 秒

### 3. 脚本结构
- 包含完整的导入语句
- 使用 unittest 或 pytest 框架
- 包含 setUp 和 tearDown 方法
- 包含至少一个测试方法

### 4. 断言
- 必须包含至少一条基础断言
- 使用 self.assertTrue / self.assertEqual 等

### 5. 代码质量
- 添加详细的中文注释
- 变量命名清晰
- 包含异常处理

## 输出格式
只输出 Python 代码，用 ```python 和 ``` 包裹，不要包含其他说明文字。

## 示例输出格式
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class TestExample(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, {self.timeout})
    
    def test_example(self):
        # 打开页面
        self.driver.get("https://example.com")
        
        # 定位元素并操作
        element = self.wait.until(
            EC.presence_of_element_located((By.ID, "element_id"))
        )
        element.send_keys("test value")
        
        # 断言
        self.assertTrue(element.is_displayed())
    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
```

现在请为上述 HTML 结构生成测试脚本："""
        
        return prompt
    
    def generate_script(self, html_content: str, test_name: str = "TestGenerated") -> str:
        """
        生成 Selenium 测试脚本
        
        参数:
            html_content: HTML DOM 结构字符串
            test_name: 测试类名称
        
        返回:
            script: 生成的 Python 测试脚本
        """
        print(f"\n{'='*60}")
        print(f"开始生成 Selenium 测试脚本")
        print(f"{'='*60}")
        
        # 步骤 1: 提取元素信息
        print(f"\n[步骤 1/3] 分析 HTML 结构...")
        element_info = self.extract_element_info(html_content)
        print(f"  ✓ 元素分析完成")
        
        # 步骤 2: 构建 Prompt
        print(f"\n[步骤 2/3] 构建 Prompt...")
        prompt = self.build_prompt(html_content, element_info)
        print(f"  ✓ Prompt 构建完成")
        
        # 步骤 3: 调用 LLM
        print(f"\n[步骤 3/3] 调用 LLM 生成脚本...")
        print(f"  模型: {self.model}")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的 UI 自动化测试工程师，擅长生成高质量的 Selenium 测试脚本。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=3000
            )
            
            script = response.choices[0].message.content
            print(f"  ✓ 脚本生成成功")
            
            return script
            
        except Exception as e:
            error_msg = f"调用失败: {str(e)}"
            print(f"   {error_msg}")
            return error_msg
    
    def extract_python_code(self, response_text: str) -> str:
        """
        从 LLM 响应中提取 Python 代码块
        
        参数:
            response_text: LLM 返回的文本
        
        返回:
            python_code: 提取的 Python 代码
        """
        # 尝试提取 ```python 代码块
        pattern = r'```python\s*(.*?)\s*```'
        match = re.search(pattern, response_text, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        
        # 如果没有找到 python 标记，尝试提取任意代码块
        pattern = r'```\s*(.*?)\s*```'
        match = re.search(pattern, response_text, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        
        # 如果没有代码块标记，返回整个响应
        return response_text.strip()
    
    def save_script(self, script: str, filename: str = None) -> str:
        """
        保存生成的脚本到文件
        
        参数:
            script: 脚本内容
            filename: 输出文件名
        
        返回:
            filepath: 保存的文件路径
        """
        if filename is None:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"selenium_test_{timestamp}.py"
        
        # 确保文件以 .py 结尾
        if not filename.endswith('.py'):
            filename += '.py'
        
        # 提取纯 Python 代码
        python_code = self.extract_python_code(script)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(python_code)
        
        print(f"\n  ✓ 脚本已保存到: {filename}")
        return filename


def demo_login_form():
    """
    演示：登录表单 HTML 生成 Selenium 脚本
    """
    print("=" * 60)
    print("HTML 到 Selenium 脚本生成器 - 登录表单项")
    print("=" * 60)
    
    # 登录表单 HTML
    login_html = """
<div class="login-container">
    <h2>用户登录</h2>
    <form id="loginForm" action="/api/login" method="POST">
        <div class="form-group">
            <label for="username">用户名</label>
            <input type="text" id="username" name="username" 
                   placeholder="请输入用户名" required>
        </div>
        <div class="form-group">
            <label for="password">密码</label>
            <input type="password" id="password" name="password" 
                   placeholder="请输入密码" required>
        </div>
        <div class="form-group">
            <label>
                <input type="checkbox" id="rememberMe" name="rememberMe">
                记住我
            </label>
        </div>
        <button type="submit" id="loginBtn" class="btn btn-primary">
            登录
        </button>
        <a href="/register" class="register-link">注册新账号</a>
    </form>
</div>
"""
    
    print(f"\n输入 HTML 结构:")
    print("-" * 60)
    print(login_html.strip())
    print("-" * 60)
    
    # 从环境变量读取配置
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.qnaigc.com/v1")
    model = os.getenv("MODEL_NAME", "deepseek-v3")
    
    if not api_key:
        print("\n错误: 未设置 OPENAI_API_KEY 环境变量")
        return
    
    # 创建生成器
    generator = SeleniumScriptGenerator(
        api_key=api_key,
        base_url=base_url,
        model=model,
        timeout=10
    )
    
    # 生成脚本
    script = generator.generate_script(login_html, "TestLoginForm")
    
    # 保存脚本
    if script and not script.startswith("调用失败"):
        filepath = generator.save_script(script, "test_login_form.py")
        
        # 打印生成的脚本
        print(f"\n{'='*60}")
        print("生成的 Selenium 测试脚本")
        print(f"{'='*60}")
        print(script)


def demo_search_box():
    """
    演示：搜索框 HTML 生成 Selenium 脚本
    """
    print("=" * 60)
    print("HTML 到 Selenium 脚本生成器 - 搜索框项")
    print("=" * 60)
    
    # 搜索框 HTML
    search_html = """
<div class="search-container">
    <form id="searchForm" role="search">
        <div class="search-input-wrapper">
            <input type="search" 
                   id="searchInput" 
                   name="q" 
                   class="form-control search-input"
                   placeholder="搜索文章、标签..."
                   autocomplete="off">
            <button type="submit" 
                    id="searchBtn" 
                    class="btn btn-search">
                <i class="icon-search"></i>
                搜索
            </button>
        </div>
        <div class="search-suggestions" id="suggestions">
            <ul class="suggestion-list">
                <li class="suggestion-item" data-value="python">Python</li>
                <li class="suggestion-item" data-value="java">Java</li>
            </ul>
        </div>
    </form>
</div>
"""
    
    print(f"\n输入 HTML 结构:")
    print("-" * 60)
    print(search_html.strip())
    print("-" * 60)
    
    # 从环境变量读取配置
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.qnaigc.com/v1")
    model = os.getenv("MODEL_NAME", "deepseek-v3")
    
    if not api_key:
        print("\n错误: 未设置 OPENAI_API_KEY 环境变量")
        return
    
    # 创建生成器
    generator = SeleniumScriptGenerator(
        api_key=api_key,
        base_url=base_url,
        model=model,
        timeout=10
    )
    
    # 生成脚本
    script = generator.generate_script(search_html, "TestSearchBox")
    
    # 保存脚本
    if script and not script.startswith("调用失败"):
        filepath = generator.save_script(script, "test_search_box.py")
        
        # 打印生成的脚本
        print(f"\n{'='*60}")
        print("生成的 Selenium 测试脚本")
        print(f"{'='*60}")
        print(script)


def demo_registration_form():
    """
    演示：注册表单 HTML 生成 Selenium 脚本
    """
    print("=" * 60)
    print("HTML 到 Selenium 脚本生成器 - 注册表单项")
    print("=" * 60)
    
    # 注册表单 HTML
    register_html = """
<div class="registration-container">
    <h2>用户注册</h2>
    <form id="registerForm" action="/api/register" method="POST">
        <div class="form-group">
            <label for="email">邮箱</label>
            <input type="email" id="email" name="email" 
                   placeholder="请输入邮箱地址" required>
            <span class="error-msg" id="emailError"></span>
        </div>
        <div class="form-group">
            <label for="phone">手机号</label>
            <input type="tel" id="phone" name="phone" 
                   placeholder="请输入手机号" pattern="[0-9]{11}">
        </div>
        <div class="form-group">
            <label for="regPassword">密码</label>
            <input type="password" id="regPassword" name="password" 
                   placeholder="至少8位，包含大小写字母和数字" required>
        </div>
        <div class="form-group">
            <label for="confirmPassword">确认密码</label>
            <input type="password" id="confirmPassword" name="confirmPassword" 
                   placeholder="请再次输入密码" required>
        </div>
        <div class="form-group">
            <label>
                <input type="checkbox" id="agreeTerms" name="agreeTerms" required>
                我已阅读并同意<a href="/terms">服务条款</a>
            </label>
        </div>
        <button type="submit" id="registerBtn" class="btn btn-success">
            立即注册
        </button>
    </form>
</div>
"""
    
    print(f"\n输入 HTML 结构:")
    print("-" * 60)
    print(register_html.strip())
    print("-" * 60)
    
    # 从环境变量读取配置
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.qnaigc.com/v1")
    model = os.getenv("MODEL_NAME", "deepseek-v3")
    
    if not api_key:
        print("\n错误: 未设置 OPENAI_API_KEY 环境变量")
        return
    
    # 创建生成器
    generator = SeleniumScriptGenerator(
        api_key=api_key,
        base_url=base_url,
        model=model,
        timeout=10
    )
    
    # 生成脚本
    script = generator.generate_script(register_html, "TestRegistrationForm")
    
    # 保存脚本
    if script and not script.startswith("调用失败"):
        filepath = generator.save_script(script, "test_registration_form.py")
        
        # 打印生成的脚本
        print(f"\n{'='*60}")
        print("生成的 Selenium 测试脚本")
        print(f"{'='*60}")
        print(script)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        demo_name = sys.argv[1]
        if demo_name == "login":
            demo_login_form()
        elif demo_name == "search":
            demo_search_box()
        elif demo_name == "register":
            demo_registration_form()
        else:
            print(f"未知演示: {demo_name}")
            print("可用演示: login, search, register")
    else:
        # 默认运行登录表单项
        demo_login_form()
