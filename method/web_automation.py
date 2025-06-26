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
            print(f"✅ 已填入密码: {password}")

            return True

        except Exception as e:
            print(f"❌ 填充登录表单失败: {e}")
            return False

    def click_login_button(self):
        """点击登录按钮"""
        try:
            # Instagram登录按钮的多种选择器
            login_button_selectors = [
                'button[type="submit"]',
                'button:contains("登录")',
                'button:contains("Log In")',
                'button:contains("Log in")',
                'div[role="button"]:contains("登录")',
                'div[role="button"]:contains("Log In")',
                'div[role="button"]:contains("Log in")',
                '[data-testid="royal_login_button"]',
                'button._acan._acap._acas._aj1-._ap30',
                'button._acan._acap._acas._aj1-'
            ]

            login_button = None
            
            # 首先尝试通过type="submit"找到按钮
            try:
                login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
                print("✅ 通过type='submit'找到登录按钮")
            except NoSuchElementException:
                pass

            # 如果没找到，尝试其他选择器
            if not login_button:
                for selector in login_button_selectors[1:]:  # 跳过第一个已经试过的
                    try:
                        if ':contains(' in selector:
                            # 对于包含文本的选择器，使用XPath
                            if '登录' in selector:
                                xpath = "//button[contains(text(), '登录')] | //div[@role='button' and contains(text(), '登录')]"
                            else:
                                xpath = "//button[contains(text(), 'Log')] | //div[@role='button' and contains(text(), 'Log')]"
                            login_button = self.driver.find_element(By.XPATH, xpath)
                        else:
                            login_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                        print(f"✅ 通过选择器找到登录按钮: {selector}")
                        break
                    except NoSuchElementException:
                        continue

            if not login_button:
                # 最后尝试通过文本内容查找
                try:
                    login_button = self.driver.find_element(By.XPATH, 
                        "//button[contains(text(), 'Log')] | //button[contains(text(), '登录')] | //div[@role='button' and (contains(text(), 'Log') or contains(text(), '登录'))]")
                    print("✅ 通过文本内容找到登录按钮")
                except NoSuchElementException:
                    pass

            if not login_button:
                print("❌ 未找到登录按钮")
                return False

            # 等待按钮可点击
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(login_button)
            )

            # 点击登录按钮
            login_button.click()
            print("✅ 已点击登录按钮")
            
            # 等待一下，让页面处理登录请求
            time.sleep(2)
            
            return True

        except Exception as e:
            print(f"❌ 点击登录按钮失败: {e}")
            return False

    def check_login_result(self):
        """检查登录结果"""
        try:
            print("🔍 正在检查登录结果...")
            
            # 等待页面响应
            time.sleep(3)
            
            # 检查是否出现错误消息
            error_selectors = [
                '[data-testid="login-error-message"]',
                '.error-message',
                '[role="alert"]',
                '.alert-danger',
                'div:contains("incorrect")',
                'div:contains("错误")',
                'div:contains("Invalid")'
            ]
            
            for selector in error_selectors:
                try:
                    if ':contains(' in selector:
                        # 使用XPath查找包含错误文本的元素
                        xpath = "//div[contains(text(), 'incorrect') or contains(text(), '错误') or contains(text(), 'Invalid') or contains(text(), 'wrong')]"
                        error_element = self.driver.find_element(By.XPATH, xpath)
                    else:
                        error_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if error_element.is_displayed():
                        error_text = error_element.text
                        print(f"❌ 登录失败，错误信息: {error_text}")
                        return False, f"登录失败: {error_text}"
                except NoSuchElementException:
                    continue
            
            # 检查是否成功跳转或出现成功标识
            success_indicators = [
                # URL变化检查
                lambda: 'instagram.com' in self.driver.current_url and 'accounts/login' not in self.driver.current_url,
                # 页面元素检查
                lambda: self.check_element_exists('[data-testid="user-avatar"]'),
                lambda: self.check_element_exists('[aria-label="Home"]'),
                lambda: self.check_element_exists('nav[role="navigation"]')
            ]
            
            for indicator in success_indicators:
                try:
                    if indicator():
                        print("✅ 登录成功！")
                        return True, "登录成功"
                except:
                    continue
            
            # 如果没有明确的成功或失败标识，返回未知状态
            current_url = self.driver.current_url
            print(f"🤔 登录状态未知，当前URL: {current_url}")
            return None, f"登录状态未知，请查看浏览器页面。当前URL: {current_url}"
            
        except Exception as e:
            print(f"❌ 检查登录结果时出错: {e}")
            return None, f"检查登录结果时出错: {e}"

    def check_element_exists(self, selector):
        """检查元素是否存在"""
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            return element.is_displayed()
        except:
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

            # 5. 点击登录按钮
            if not self.click_login_button():
                return False, "点击登录按钮失败"

            # 6. 检查登录结果
            login_success, result_message = self.check_login_result()
            
            if login_success is True:
                print("✅ 自动登录完全成功！")
                result_msg = f"登录成功！{result_message}"
            elif login_success is False:
                print(f"❌ 自动登录失败: {result_message}")
                result_msg = f"登录失败: {result_message}"
            else:
                print("🤔 登录状态未知，请查看浏览器")
                result_msg = f"已完成自动登录尝试，{result_message}"

            # 设置浏览器保持活跃
            self.keep_browser_alive()

            # 不关闭浏览器，让用户继续操作
            return True, result_msg

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
