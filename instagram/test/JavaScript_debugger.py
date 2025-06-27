#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram JavaScript选择器调试
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions


class InstagramJSDebugger:
    """Instagram JavaScript选择器调试器"""

    def __init__(self):
        """初始化调试器"""
        self.driver = None

    def setup_driver(self):
        """设置浏览器驱动"""
        try:
            options = EdgeOptions()
            options.add_argument("--disable-blink-features=AutomationControlled")
            self.driver = webdriver.Edge(options=options)
            print("✅ Edge浏览器驱动初始化成功")
            return True
        except Exception as e:
            print(f"❌ 浏览器驱动初始化失败: {e}")
            return False

    def open_instagram(self):
        """打开Instagram页面"""
        try:
            self.driver.get("https://www.instagram.com/")
            print("✅ 成功打开Instagram页面")
            time.sleep(3)
            return True
        except Exception as e:
            print(f"❌ 打开页面失败: {e}")
            return False

    def auto_login(self, username, password):
        """自动登录Instagram"""
        try:
            print("🔄 正在尝试自动登录...")

            # 等待登录表单加载
            time.sleep(3)

            # 查找用户名输入框
            username_selectors = [
                'input[name="username"]',
                'input[aria-label="手机号、用户名或邮箱"]',
                'input[aria-label="Phone number, username, or email"]'
            ]

            username_input = None
            for selector in username_selectors:
                try:
                    username_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue

            if not username_input:
                print("❌ 未找到用户名输入框")
                return False

            # 查找密码输入框
            password_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')

            # 清空并填入登录信息
            username_input.clear()
            username_input.send_keys(username)
            print(f"✅ 已填入用户名: {username}")

            password_input.clear()
            password_input.send_keys(password)
            print("✅ 已填入密码")

            # 查找并点击登录按钮
            login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            login_button.click()
            print("✅ 已点击登录按钮")

            # 等待登录完成
            print("⏳ 等待登录完成...")
            time.sleep(5)

            # 检查是否登录成功
            current_url = self.driver.current_url
            if 'accounts/login' not in current_url:
                print("✅ 登录成功！")

                # 导航到目标页面
                self.driver.get("https://www.instagram.com/?next=%2F")
                time.sleep(3)

                return True
            else:
                print("❌ 登录可能失败，请检查用户名和密码")
                return False

        except Exception as e:
            print(f"❌ 自动登录失败: {e}")
            return False

    def analyze_page_structure(self):
        """分析页面结构"""
        print("\n=== 分析页面结构 ===")

        try:
            # 查找所有按钮
            all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
            print(f"页面总按钮数: {len(all_buttons)}")

            # 查找所有带SVG的按钮
            svg_buttons = self.driver.find_elements(By.XPATH, "//button[.//svg]")
            print(f"带SVG的按钮数: {len(svg_buttons)}")

            # 查找所有文章
            articles = self.driver.find_elements(By.TAG_NAME, "article")
            print(f"文章数量: {len(articles)}")

            # 分析可能的点赞按钮
            print("\n--- 可能的点赞按钮分析 ---")
            potential_like_buttons = []

            for i, button in enumerate(svg_buttons[:10]):  # 只分析前10个
                try:
                    aria_label = button.get_attribute("aria-label") or ""
                    if "like" in aria_label.lower() or "赞" in aria_label:
                        potential_like_buttons.append(button)
                        print(f"可能的点赞按钮 {len(potential_like_buttons)}: aria-label='{aria_label}'")

                except Exception as e:
                    continue

            print(f"\n找到 {len(potential_like_buttons)} 个可能的点赞按钮")

        except Exception as e:
            print(f"❌ 分析页面结构失败: {e}")

    def interactive_js_test(self):
        """交互式JavaScript选择器测试"""
        print("\n=== JavaScript选择器测试 ===")
        print("输入JavaScript选择器表达式进行测试，输入'quit'退出")

        while True:
            try:
                js_code = input("\n请输入JavaScript选择器: ").strip()

                if js_code.lower() in ['quit', 'exit', 'q']:
                    break

                if not js_code:
                    continue

                # 如果用户只输入了CSS选择器，自动包装为querySelectorAll
                if not js_code.startswith('document.'):
                    js_code = f"document.querySelectorAll('{js_code}')"

                # 执行JavaScript代码
                elements = self.driver.execute_script(f"return Array.from({js_code});")
                count = len(elements) if elements else 0

                if count > 0:
                    print(f"✅ 找到 {count} 个元素")

                    # 显示所有元素信息
                    clickable_elements = []
                    for i, element in enumerate(elements[:10]):  # 显示前10个元素
                        try:
                            aria_label = element.get_attribute("aria-label") or "无"
                            tag_name = element.tag_name
                            is_displayed = element.is_displayed()
                            is_enabled = element.is_enabled()

                            print(
                                f"   元素{i + 1}: {tag_name}, aria-label='{aria_label}', 可见={is_displayed}, 可点击={is_enabled}")

                            # 只收集可见且可点击的元素
                            if is_displayed and is_enabled:
                                clickable_elements.append((i + 1, element))

                        except Exception as e:
                            print(f"   元素{i + 1}: 操作失败 - {e}")

                    # 如果有可点击的元素，询问用户要点击哪个
                    if clickable_elements:
                        print(f"\n可点击的元素: {[str(idx) for idx, _ in clickable_elements]}")
                        choice = input("请选择要点击的元素编号 (直接回车跳过): ").strip()

                        if choice.isdigit():
                            choice_num = int(choice)
                            # 找到对应的元素
                            selected_element = None
                            for idx, element in clickable_elements:
                                if idx == choice_num:
                                    selected_element = element
                                    break

                            if selected_element:
                                print(f"🔄 正在点击元素{choice_num}...")
                                try:
                                    # 记录点击前的状态
                                    before_aria = selected_element.get_attribute("aria-label") or "无"
                                    print(f"   点击前状态: {before_aria}")

                                    # 点击元素
                                    selected_element.click()
                                    selected_element.click()
                                    time.sleep(3)  # 等待状态更新

                                    # 检查点击后的状态
                                    try:
                                        after_aria = selected_element.get_attribute("aria-label") or "无"
                                        print("   点击完成")

                                        if before_aria != after_aria:
                                            print(f"   ✅ 点击成功！状态已改变")
                                        else:
                                            print(f"   ✅ 点击完成（状态未改变）")
                                    except:
                                        print(f"   ✅ 点击完成（无法检查状态变化）")

                                except Exception as e:
                                    print(f"   ❌ 点击失败: {e}")
                            else:
                                print(f"❌ 未找到编号为{choice_num}的可点击元素")
                    else:
                        print("⚠️ 没有可点击的元素")
                else:
                    print("❌ 未找到元素")

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ 测试出错: {e}")

    def close_browser(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            print("✅ 浏览器已关闭")

    def get_login_credentials(self):
        """获取登录凭据"""
        print("\n=== 请输入Instagram登录信息 ===")

        username = input("用户名: ").strip()
        password = input("密码: ").strip()

        if not username or not password:
            print("❌ 用户名和密码不能为空")
            return None, None

        return username, password

    def run_debug(self):
        """运行完整的调试流程"""
        print("=== Instagram JavaScript选择器调试器 ===")

        # 1. 设置浏览器
        if not self.setup_driver():
            return

        # 2. 打开Instagram
        if not self.open_instagram():
            self.close_browser()
            return

        # 3. 获取登录凭据
        username, password = self.get_login_credentials()
        if not username or not password:
            print("❌ 登录信息无效，退出程序")
            self.close_browser()
            return

        # 4. 自动登录
        if not self.auto_login(username, password):
            print("❌ 自动登录失败")
            manual_login = input("是否手动登录? (y/n): ").strip().lower()
            if manual_login == 'y':
                print("请在浏览器中手动登录，然后按回车继续...")
                input()
            else:
                self.close_browser()
                return

        # 5. 分析页面结构
        self.analyze_page_structure()

        # 6. 直接进入JavaScript交互式测试
        self.interactive_js_test()

        # 7. 关闭浏览器
        close_browser = input("\n是否关闭浏览器? (y/n): ").strip().lower()
        if close_browser == 'y':
            self.close_browser()
        else:
            print("浏览器保持打开状态，您可以继续手动测试")


def main():
    """主函数"""
    debugger = InstagramJSDebugger()

    try:
        debugger.run_debug()
    except KeyboardInterrupt:
        print("\n\n调试被用户中断")
        debugger.close_browser()
    except Exception as e:
        print(f"\n❌ 调试过程中出现错误: {e}")
        debugger.close_browser()


if __name__ == "__main__":
    main()
