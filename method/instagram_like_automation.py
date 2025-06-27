#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram点赞自动化模块
在登录成功后自动进行点赞操作
"""

import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from web_automation import InstagramWebAutomation


class InstagramLikeAutomation(InstagramWebAutomation):
    """Instagram点赞自动化类，继承自InstagramWebAutomation"""

    def __init__(self):
        """初始化点赞自动化"""
        super().__init__()
        self.like_count = 0
        self.max_likes = 10  # 默认最大点赞数
        self.like_delay = (2, 5)  # 点赞间隔时间范围（秒）

    def navigate_to_target_url(self, target_url="https://www.instagram.com/?next=%2F"):
        """导航到目标地址"""
        try:
            print(f"🔄 正在导航到目标地址: {target_url}")
            self.driver.get(target_url)

            # 等待页面加载
            time.sleep(3)

            print("✅ 成功导航到目标地址")
            return True

        except Exception as e:
            print(f"❌ 导航到目标地址失败: {e}")
            return False

    def find_like_buttons(self):
        """查找页面上的点赞按钮"""
        try:
            # Instagram点赞按钮的多种XPath选择器（按优先级排序）
            like_button_xpaths = [
                # 方法1: 通过aria-label属性查找（最可靠）
                "//button[@aria-label='Like' or @aria-label='赞']",
                "//div[@role='button'][@aria-label='Like' or @aria-label='赞']",
                
                # 方法2: 通过包含Like文本的aria-label查找
                "//button[contains(@aria-label, 'Like')]",
                "//div[@role='button'][contains(@aria-label, 'Like')]",
                
                # 方法3: 通过SVG路径查找心形图标
                "//button[.//svg[@aria-label='Like']]",
                "//button[.//svg[@aria-label='赞']]",
                
                # 方法4: 通过文章内的按钮结构查找
                "//article//section//button[.//svg]",
                "//article//div[contains(@class, 'x1i10hfl')]//button",
                
                # 方法5: 通过帖子互动区域查找
                "//section[contains(@class, 'x1ja2u2z')]//button[.//svg]",
                "//div[contains(@class, '_ae2s')]//button[.//svg]",
                
                # 方法6: 通过span包装的按钮查找
                "//span[contains(@class, 'x1rg5ohu')]//button",
                "//span[contains(@class, '_aamw')]//button",
                
                # 方法7: 更通用的选择器（作为备选）
                "//button[.//svg[contains(@viewBox, '0 0 24 24')]]",
                "//div[@role='button'][.//svg[contains(@viewBox, '0 0 24 24')]]"
            ]

            like_buttons = []

            for xpath in like_button_xpaths:
                try:
                    buttons = self.driver.find_elements(By.XPATH, xpath)
                    for button in buttons:
                        # 检查按钮是否可见且可点击
                        if button.is_displayed() and button.is_enabled():
                            # 检查是否已经点赞（通过aria-label或SVG属性）
                            if not self.is_already_liked(button):
                                like_buttons.append(button)
                except Exception as e:
                    print(f"⚠️ 使用XPath {xpath} 查找按钮时出错: {e}")
                    continue

            print(f"✅ 找到 {len(like_buttons)} 个可点赞的按钮")
            return like_buttons

        except Exception as e:
            print(f"❌ 查找点赞按钮失败: {e}")
            return []

    def is_already_liked(self, button):
        """检查按钮是否已经被点赞"""
        try:
            # 检查aria-label是否包含"Unlike"或"取消赞"
            aria_label = button.get_attribute("aria-label") or ""
            if "Unlike" in aria_label or "取消赞" in aria_label:
                return True

            # 检查SVG的fill属性或class
            svg_elements = button.find_elements(By.TAG_NAME, "svg")
            for svg in svg_elements:
                # 检查SVG的aria-label
                svg_label = svg.get_attribute("aria-label") or ""
                if "Unlike" in svg_label or "取消赞" in svg_label:
                    return True

                # 检查SVG的fill属性（红色表示已点赞）
                fill_color = svg.get_attribute("fill") or ""
                if "#ed4956" in fill_color.lower() or "#ff3040" in fill_color.lower():
                    return True

            return False

        except Exception as e:
            print(f"⚠️ 检查点赞状态时出错: {e}")
            return False

    def click_like_button(self, button):
        """点击单个点赞按钮"""
        try:
            # 滚动到按钮位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(0.5)

            # 等待按钮可点击
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(button)
            )

            # 点击按钮
            button.click()
            print("✅ 成功点击点赞按钮")

            # 增加点赞计数
            self.like_count += 1

            # 随机延迟，模拟人类行为
            delay = random.uniform(self.like_delay[0], self.like_delay[1])
            print(f"⏳ 等待 {delay:.1f} 秒...")
            time.sleep(delay)

            return True

        except Exception as e:
            print(f"❌ 点击点赞按钮失败: {e}")
            return False

    def auto_like_posts(self, max_likes=10, scroll_count=3):
        """自动点赞帖子"""
        try:
            print("=== 开始自动点赞流程 ===")
            self.max_likes = max_likes
            self.like_count = 0

            for scroll_round in range(scroll_count):
                print(f"\n--- 第 {scroll_round + 1} 轮滚动和点赞 ---")

                # 查找当前页面的点赞按钮
                like_buttons = self.find_like_buttons()

                if not like_buttons:
                    print("⚠️ 当前页面没有找到可点赞的按钮")
                else:
                    # 点击找到的点赞按钮
                    for i, button in enumerate(like_buttons):
                        if self.like_count >= self.max_likes:
                            print(f"✅ 已达到最大点赞数 {self.max_likes}，停止点赞")
                            break

                        print(f"🔄 正在点击第 {i + 1} 个点赞按钮...")
                        if self.click_like_button(button):
                            print(f"✅ 成功点赞！当前总计: {self.like_count}/{self.max_likes}")
                        else:
                            print(f"❌ 点赞失败")

                # 如果已达到最大点赞数，退出
                if self.like_count >= self.max_likes:
                    break

                # 滚动页面加载更多内容
                if scroll_round < scroll_count - 1:  # 最后一轮不需要滚动
                    print("🔄 滚动页面加载更多内容...")
                    self.scroll_page()
                    time.sleep(2)

            print(f"\n=== 点赞流程完成 ===")
            print(f"✅ 总共点赞了 {self.like_count} 个帖子")
            return True, f"成功点赞 {self.like_count} 个帖子"

        except Exception as e:
            error_msg = f"自动点赞过程中出现错误: {e}"
            print(f"❌ {error_msg}")
            return False, error_msg

    def scroll_page(self):
        """滚动页面"""
        try:
            # 滚动到页面底部
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # 再滚动回中间位置
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.7);")
            time.sleep(1)

        except Exception as e:
            print(f"⚠️ 滚动页面时出错: {e}")

    def login_and_like(self, username, password, target_url="https://www.instagram.com/?next=%2F", max_likes=10):
        """完整的登录并点赞流程"""
        try:
            print("=== 开始Instagram登录并点赞流程 ===")

            # 1. 执行登录流程
            login_success, login_message = self.auto_login_instagram(username, password)

            if not login_success:
                return False, f"登录失败: {login_message}"

            print("✅ 登录成功，开始点赞流程...")

            # 2. 导航到目标地址
            if not self.navigate_to_target_url(target_url):
                return False, "导航到目标地址失败"

            # 3. 等待页面加载
            time.sleep(3)

            # 4. 开始自动点赞
            like_success, like_message = self.auto_like_posts(max_likes=max_likes)

            if like_success:
                final_message = f"登录并点赞完成！{login_message}，{like_message}"
                print(f"✅ {final_message}")
                return True, final_message
            else:
                return False, f"登录成功但点赞失败: {like_message}"

        except Exception as e:
            error_msg = f"登录并点赞流程出现错误: {e}"
            print(f"❌ {error_msg}")
            return False, error_msg

    def set_like_settings(self, max_likes=10, delay_range=(2, 5)):
        """设置点赞参数"""
        self.max_likes = max_likes
        self.like_delay = delay_range
        print(f"✅ 点赞设置已更新: 最大点赞数={max_likes}, 延迟范围={delay_range}秒")


# 便捷函数
def auto_login_and_like(username, password, target_url="https://www.instagram.com/?next=%2F", max_likes=10):
    """便捷函数：自动登录并点赞"""
    automation = InstagramLikeAutomation()

    try:
        success, message = automation.login_and_like(username, password, target_url, max_likes)

        # 成功时不关闭浏览器，让用户继续操作
        if not success:
            automation.close_browser()

        return success, message

    except Exception as e:
        automation.close_browser()
        return False, f"登录并点赞过程出现异常: {e}"


if __name__ == "__main__":
    # 测试代码
    print("=== Instagram点赞自动化测试 ===")

    # 测试用的用户名和密码
    test_username = "test_user"
    test_password = "test_password"
    target_url = "https://www.instagram.com/?next=%2F"
    max_likes = 5

    success, message = auto_login_and_like(test_username, test_password, target_url, max_likes)

    if success:
        print(f"✅ 测试成功: {message}")
    else:
        print(f"❌ 测试失败: {message}")
