from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class TestLoginPage(unittest.TestCase):
    def setUp(self):
        """初始化测试环境"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        # 假设登录页面URL，实际测试时需要替换为真实URL
        self.login_url = "http://example.com/login"
    
    def test_login_functionality(self):
        """测试登录功能"""
        try:
            # 打开登录页面
            self.driver.get(self.login_url)
            
            # 等待页面标题加载
            self.wait.until(EC.title_contains("用户登录"))
            
            # 定位用户名输入框并输入
            username_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_input.send_keys("testuser")
            
            # 定位密码输入框并输入
            password_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            password_input.send_keys("testpass")
            
            # 勾选记住我复选框
            remember_checkbox = self.wait.until(
                EC.presence_of_element_located((By.ID, "rememberMe"))
            )
            remember_checkbox.click()
            
            # 点击登录按钮
            login_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "loginBtn"))
            )
            login_button.click()
            
            # 断言登录按钮文本是否正确
            self.assertEqual(login_button.text, "登录")
            
            # 断言注册链接是否存在
            register_link = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "register-link"))
            )
            self.assertTrue(register_link.is_displayed())
            
        except Exception as e:
            # 捕获异常并截图
            self.driver.save_screenshot("login_test_error.png")
            raise e
    
    def tearDown(self):
        """清理测试环境"""
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()