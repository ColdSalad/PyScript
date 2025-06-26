#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网页自动化模块
使用Selenium控制浏览器并自动填充Instagram登录表单
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException


class InstagramWebAutomation:
    """Instagram网页自动化类"""

    def __init__(self):
        """初始化网页自动化"""
        self.driver = None
        self.wait_timeout = 10
        self.auto_close_on_destroy = False  # 控制是否在对象销毁时自动关闭浏览器

    def __del__(self):
        """析构函数 - 仅在明确设置时才关闭浏览器"""
        if self.auto_close_on_destroy and self.driver:
            try:
                self.driver.quit()
                print("🔄 对象销毁时关闭浏览器")
            except:
                pass

    def setup_edge_driver(self):
        """设置Edge浏览器驱动"""
        try:
            edge_options = EdgeOptions()
            edge_options.add_argument("--disable-blink-features=AutomationControlled")
            edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            edge_options.add_experimental_option('useAutomationExtension', False)

            # 尝试使用系统中的Edge浏览器
            edge_paths = [
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\Application\msedge.exe")
            ]

            for edge_path in edge_paths:
                if os.path.exists(edge_path):
                    edge_options.binary_location = edge_path
                    break

            self.driver = webdriver.Edge(options=edge_options)
            print("✅ Edge浏览器驱动初始化成功")
            return True

        except Exception as e:
            print(f"❌ Edge驱动初始化失败: {e}")
            return False

    def setup_chrome_driver(self):
        """设置Chrome浏览器驱动"""
        try:
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            # 尝试使用系统中的Chrome浏览器
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
            ]

            for chrome_path in chrome_paths:
                if os.path.exists(chrome_path):
                    chrome_options.binary_location = chrome_path
                    break

            self.driver = webdriver.Chrome(options=chrome_options)
            print("✅ Chrome浏览器驱动初始化成功")
            return True

        except Exception as e:
            print(f"❌ Chrome驱动初始化失败: {e}")
            return False

    def setup_driver(self, prefer_edge=True):
        """设置浏览器驱动"""
        if prefer_edge:
            # 优先尝试Edge
            if self.setup_edge_driver():
                return True
            # Edge失败则尝试Chrome
            elif self.setup_chrome_driver():
                return True
        else:
            # 优先尝试Chrome
            if self.setup_chrome_driver():
                return True
            # Chrome失败则尝试Edge
            elif self.setup_edge_driver():
                return True

        print("❌ 无法初始化任何浏览器驱动")
        return False

    def open_instagram(self):
        """打开Instagram登录页面"""
        try:
            self.driver.get("https://www.instagram.com/")
            print("✅ 成功打开Instagram页面")

            # 等待页面加载
            time.sleep(3)
            return True

        except Exception as e:
            print(f"❌ 打开Instagram页面失败: {e}")
            return False

    def wait_for_login_form(self):
        """等待登录表单加载"""
        try:
            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            print("✅ 登录表单已加载")
            return True

        except TimeoutException:
            print("❌ 等待登录表单超时")
            return False
        except Exception as e:
            print(f"❌ 等待登录表单失败: {e}")
            return False

    def fill_login_form(self, username, password):
        """填充登录表单"""
        try:
            # 查找用户名输入框
            username_selectors = [
                'input[name="username"]',
                'input[aria-label="手机号、用户名或邮箱"]',
                'input[aria-label="Phone number, username, or email"]',
                'input[placeholder*="用户名"]',
                'input[placeholder*="username"]'
            ]

            username_input = None
            for selector in username_selectors:
                try:
                    username_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue

            if not username_input:
                print("❌ 未找到用户名输入框")
                return False

            # 清空并填入用户名
            username_input.clear()
            time.sleep(0.5)
            username_input.send_keys(username)
            print(f"✅ 已填入用户名: {username}")

            # 查找密码输入框
            password_selectors = [
                'input[name="password"]',
                'input[type="password"]',
                'input[aria-label="密码"]',
                'input[aria-label="Password"]'
            ]

            password_input = None
            for selector in password_selectors:
                try:
                    password_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue

            if not password_input:
                print("❌ 未找到密码输入框")
                return False

            # 清空并填入密码
            password_input.clear()
            time.sleep(0.5)
            password_input.send_keys(password)
            print("✅ 已填入密码")

            return True

        except Exception as e:
            print(f"❌ 填充登录表单失败: {e}")
            return False

    def keep_browser_alive(self):
        """设置浏览器保持活跃状态"""
        self.auto_close_on_destroy = False
        print("🌐 浏览器已设置为保持打开状态")

    def auto_login_instagram(self, username, password):
        """自动登录Instagram的完整流程"""
        try:
            print("=== 开始Instagram自动登录流程 ===")

            # 1. 设置浏览器驱动
            if not self.setup_driver():
                return False, "无法初始化浏览器驱动"

            # 2. 打开Instagram页面
            if not self.open_instagram():
                return False, "无法打开Instagram页面"

            # 3. 等待登录表单加载
            if not self.wait_for_login_form():
                return False, "登录表单加载失败"

            # 4. 填充登录表单
            if not self.fill_login_form(username, password):
                return False, "填充登录表单失败"

            print("✅ 自动登录流程完成！用户可以手动点击登录按钮")
            print("🌐 浏览器将保持打开状态，方便用户操作")

            # 设置浏览器保持活跃
            self.keep_browser_alive()

            # 不关闭浏览器，让用户继续操作
            return True, "登录信息已自动填入，浏览器保持打开"

        except Exception as e:
            error_msg = f"自动登录过程中出现错误: {e}"
            print(f"❌ {error_msg}")
            # 出错时才关闭浏览器
            self.close_browser()
            return False, error_msg

    def close_browser(self):
        """关闭浏览器"""
        try:
            if self.driver:
                self.driver.quit()
                print("✅ 浏览器已关闭")
        except Exception as e:
            print(f"❌ 关闭浏览器失败: {e}")

    def keep_browser_open(self, duration=300):
        """保持浏览器打开指定时间（秒）"""
        try:
            print(f"浏览器将保持打开 {duration} 秒...")
            time.sleep(duration)
        except KeyboardInterrupt:
            print("用户中断，关闭浏览器")
        finally:
            self.close_browser()


# 便捷函数
def auto_login_instagram(username, password, keep_open=True):
    """便捷函数：自动登录Instagram"""
    automation = InstagramWebAutomation()

    try:
        success, message = automation.auto_login_instagram(username, password)

        # 成功时不关闭浏览器，让用户继续操作
        # 失败时才关闭浏览器
        if not success:
            automation.close_browser()

        return success, message

    except Exception as e:
        automation.close_browser()
        return False, f"登录过程出现异常: {e}"


if __name__ == "__main__":
    # 测试代码
    print("=== Instagram网页自动化测试 ===")

    # 测试用的用户名和密码
    test_username = "test_user"
    test_password = "test_password"

    success, message = auto_login_instagram(test_username, test_password)

    if success:
        print(f"✅ 测试成功: {message}")
    else:
        print(f"❌ 测试失败: {message}")
