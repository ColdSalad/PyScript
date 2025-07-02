#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram 点赞自动化
专注于点赞功能，复用现有的登录和页面打开功能
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 导入现有的网页自动化模块
try:
    from src.main.pythn.method.web_automation import InstagramWebAutomation
    WEB_AUTOMATION_AVAILABLE = True
except ImportError:
    WEB_AUTOMATION_AVAILABLE = False
    print("⚠️ web_automation模块不可用，将使用内置登录功能")

# 导入评论自动化模块
try:
    from src.main.pythn.method.instagram_comment_automation import InstagramCommentAutomation
    COMMENT_AUTOMATION_AVAILABLE = True
except ImportError:
    COMMENT_AUTOMATION_AVAILABLE = False
    print("⚠️ instagram_comment_automation模块不可用，将跳过评论功能")


class InstagramLikeAutomation:
    """Instagram点赞自动化类 - 专注于点赞功能"""

    def __init__(self):
        """初始化自动化实例"""
        self.driver = None
        self.wait = None
        self.web_automation = None
        self.comment_automation = None

    def setup_driver(self):
        """设置浏览器驱动"""
        try:
            options = EdgeOptions()
            # 禁用自动化检测
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

            # 设置用户代理
            options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0")

            self.driver = webdriver.Edge(options=options)

            # 执行脚本隐藏webdriver属性
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            # 设置等待
            self.wait = WebDriverWait(self.driver, 10)

            print("✅ Edge浏览器驱动初始化成功")
            return True
        except Exception as e:
            print(f"❌ 浏览器驱动初始化失败: {e}")
            return False

    def login_with_existing_automation(self, username, password):
        """使用现有的网页自动化模块进行登录"""
        try:
            if WEB_AUTOMATION_AVAILABLE:
                print("🔄 使用现有自动化模块进行登录...")

                # 创建web_automation实例
                self.web_automation = InstagramWebAutomation()

                # 强制使用我们已有的driver，避免创建新浏览器
                self.web_automation.driver = self.driver
                self.web_automation.wait = WebDriverWait(self.driver, 10)

                # 先打开Instagram页面
                print("🔄 打开Instagram登录页面...")
                if not self.web_automation.open_instagram():
                    return False, "打开Instagram页面失败"

                # 分步调用登录流程，跳过驱动初始化
                print("⏳ 等待登录表单加载...")
                if not self.web_automation.wait_for_login_form():
                    return False, "登录表单加载失败"

                print("📝 填充登录表单...")
                if not self.web_automation.fill_login_form(username, password):
                    return False, "填充登录表单失败"

                print("🖱️ 点击登录按钮...")
                if not self.web_automation.click_login_button():
                    return False, "点击登录按钮失败"

                print("🔍 检查登录结果...")
                login_success, result_message = self.web_automation.check_login_result()

                if login_success is True:
                    return True, f"登录成功！{result_message}"
                elif login_success is False:
                    return False, f"登录失败: {result_message}"
                else:
                    # 登录状态未知，但继续尝试
                    return True, f"已完成登录尝试，{result_message}"

            else:
                return False, "网页自动化模块不可用"
        except Exception as e:
            print(f"❌ 使用现有自动化模块登录失败: {e}")
            return False, f"登录失败: {e}"

    def find_like_buttons(self):
        """查找点赞按钮 - 直接使用测试成功的选择器"""
        try:
            print("🔍 正在查找点赞按钮...")

            # 使用更新的成功选择器（Instagram动态生成ID）
            latest_selector = "#mount_0_0_jO > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x15mokao.x1ga7v0g.x16uus16.xbiv7yw.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.xvc5jky.xh8yej3.x10o80wk.x14k21rp.x17snn68.x6osk4m.x1porb0y.x8vgawa > section > main > div.x1qjc9v5.x78zum5.x1q0g3np.xl56j7k.xh8yej3.xyinxu5 > div > div > div.x9f619.xjbqb8w.x78zum5.x15mokao.x1ga7v0g.x16uus16.xbiv7yw.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x6s0dn4.x1oa3qoh.x1nhvcw1 > div > div:nth-child(1) > div > article:nth-child(1) > div > div.x1lliihq.x1n2onr6 > div > div > section.x6s0dn4.xrvj5dj.x1o61qjw.x12nagc.x1gslohp > div.x78zum5 > span.x1qfufaz > div > div > div"

            # 创建多个选择器版本以应对动态ID变化
            selectors_to_try = [
                latest_selector,  # 最新的选择器
                "#mount_0_0_VH > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x15mokao.x1ga7v0g.x16uus16.xbiv7yw.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.xvc5jky.xh8yej3.x10o80wk.x14k21rp.x17snn68.x6osk4m.x1porb0y.x8vgawa > section > main > div.x1qjc9v5.x78zum5.x1q0g3np.xl56j7k.xh8yej3.xyinxu5 > div > div > div.x9f619.xjbqb8w.x78zum5.x15mokao.x1ga7v0g.x16uus16.xbiv7yw.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x6s0dn4.x1oa3qoh.x1nhvcw1 > div > div:nth-child(1) > div > article:nth-child(1) > div > div.x1lliihq.x1n2onr6 > div > div > section.x6s0dn4.xrvj5dj.x1o61qjw.x12nagc.x1gslohp > div.x78zum5 > span.x1qfufaz > div > div > div",  # 之前的选择器
                # 通用的动态选择器模式
                '[id^="mount_"] section main article section div.x78zum5 span.x1qfufaz div div div'
            ]

            like_buttons = []

            # 使用JavaScript直接查找
            js_script = f"""
            // 使用多个选择器查找点赞按钮
            const selectorsToTry = {selectors_to_try};
            const buttons = [];
            
            try {{
                console.log('开始查找点赞按钮...');
                console.log('将尝试', selectorsToTry.length, '个选择器');
                
                // 方法1: 使用具体的成功选择器
                let foundWithSpecificSelector = false;
                for (let i = 0; i < selectorsToTry.length; i++) {{
                    const selector = selectorsToTry[i];
                    console.log(`尝试选择器 ${{i + 1}}: ${{selector.substring(0, 50)}}...`);
                    
                    try {{
                        const elements = document.querySelectorAll(selector);
                        console.log(`选择器 ${{i + 1}} 找到元素数量:`, elements.length);
                        
                        if (elements.length > 0) {{
                            elements.forEach((element, index) => {{
                                // 查找可点击的父元素
                                let clickableParent = element.closest('button, div[role="button"]');
                                if (clickableParent && clickableParent.offsetParent !== null) {{
                                    buttons.push(clickableParent);
                                    console.log(`找到可点击父元素 ${{index + 1}}:`, clickableParent.getAttribute('aria-label'));
                                    foundWithSpecificSelector = true;
                                }}
                            }});
                            
                            if (foundWithSpecificSelector) {{
                                console.log(`选择器 ${{i + 1}} 成功找到按钮，停止尝试其他选择器`);
                                break;
                            }}
                        }}
                    }} catch(e) {{
                        console.log(`选择器 ${{i + 1}} 失败:`, e.message);
                    }}
                }}
                
                // 方法2: 如果具体选择器没找到，使用通用方法查找所有文章中的点赞按钮
                if (buttons.length === 0) {{
                    console.log('使用通用方法查找点赞按钮...');
                    const articles = document.querySelectorAll('article');
                    console.log('找到文章数量:', articles.length);
                    
                    articles.forEach((article, index) => {{
                        console.log(`处理第${{index + 1}}篇文章...`);
                        
                        // 查找点赞按钮的多种可能选择器
                        const selectors = [
                            'button[aria-label*="赞"]',
                            'button[aria-label*="Like"]', 
                            'div[role="button"][aria-label*="赞"]',
                            'div[role="button"][aria-label*="Like"]',
                            'section button svg',
                            'section div[role="button"] svg'
                        ];
                        
                        selectors.forEach(selector => {{
                            const likeBtns = article.querySelectorAll(selector);
                            likeBtns.forEach(btn => {{
                                if (btn.offsetParent !== null) {{
                                    // 对于SVG元素，需要找到其按钮父元素
                                    let buttonElement = btn;
                                    if (btn.tagName === 'SVG') {{
                                        buttonElement = btn.closest('button, div[role="button"]');
                                    }}
                                    
                                    if (buttonElement && !buttons.includes(buttonElement)) {{
                                        const ariaLabel = buttonElement.getAttribute('aria-label') || '';
                                        if (ariaLabel.includes('赞') || ariaLabel.toLowerCase().includes('like')) {{
                                            buttons.push(buttonElement);
                                            console.log('找到点赞按钮:', ariaLabel);
                                        }}
                                    }}
                                }}
                            }});
                        }});
                    }});
                }}
                
                // 方法3: 最后的备用方法 - 查找所有可能的点赞按钮
                if (buttons.length === 0) {{
                    console.log('使用最后备用方法...');
                    const allButtons = document.querySelectorAll('button, div[role="button"]');
                    allButtons.forEach(btn => {{
                        const ariaLabel = btn.getAttribute('aria-label') || '';
                        const hasHeartSvg = btn.querySelector('svg') !== null;
                        
                        if ((ariaLabel.includes('赞') || ariaLabel.toLowerCase().includes('like')) && 
                            hasHeartSvg && btn.offsetParent !== null) {{
                            buttons.push(btn);
                            console.log('备用方法找到按钮:', ariaLabel);
                        }}
                    }});
                }}
                
            }} catch(e) {{
                console.log('查找过程出错:', e);
            }}
            
            // 去重
            const uniqueButtons = [...new Set(buttons)];
            console.log('最终找到按钮数量:', uniqueButtons.length);
            return uniqueButtons;
            """

            like_buttons = self.driver.execute_script(js_script)
            print(f"🎯 使用JavaScript找到 {len(like_buttons)} 个点赞按钮")

            return like_buttons

        except Exception as e:
            print(f"❌ 查找点赞按钮失败: {e}")
            return []



    def auto_comment_after_like(self, comment_text="很棒的分享！👍"):
        """点赞后自动评论

        Args:
            comment_text: 评论内容

        Returns:
            bool: 是否成功评论
        """
        try:
            if not COMMENT_AUTOMATION_AVAILABLE:
                print("⚠️ 评论自动化模块不可用，跳过评论")
                return False

            print(f"💬 开始自动评论: {comment_text}")

            # 初始化评论自动化实例（复用当前driver）
            if not self.comment_automation:
                self.comment_automation = InstagramCommentAutomation(self.driver)

            # 为当前帖子添加评论
            success = self.comment_automation.add_comment_to_post(comment_text)

            if success:
                print("✅ 自动评论成功")
                return True
            else:
                print("❌ 自动评论失败")
                return False

        except Exception as e:
            print(f"❌ 自动评论过程中出错: {e}")
            return False

    def perform_likes(self, max_likes=10, enable_comment=False, comment_text="很棒的分享！👍"):
        """执行点赞操作"""
        try:
            print(f"🎯 开始执行点赞操作，最大点赞数: {max_likes}")

            liked_count = 0
            scroll_attempts = 0
            max_scroll_attempts = 5

            # 等待页面加载完成
            time.sleep(3)

            while liked_count < max_likes and scroll_attempts < max_scroll_attempts:
                # 查找当前页面的点赞按钮
                like_buttons = self.find_like_buttons()

                if not like_buttons:
                    print("⚠️ 未找到点赞按钮，尝试滚动页面...")
                    self.scroll_page()
                    scroll_attempts += 1
                    time.sleep(3)
                    continue

                print(f"📍 找到 {len(like_buttons)} 个点赞按钮")

                # 对找到的按钮进行点赞
                processed_buttons = 0
                for button in like_buttons:
                    if liked_count >= max_likes:
                        break

                    try:
                        # 检查按钮状态
                        aria_label = button.get_attribute("aria-label") or ""
                        print(f"🔍 检查按钮状态: {aria_label}")

                        # 只点击未点赞的按钮
                        if 'unlike' not in aria_label.lower() and '取消赞' not in aria_label and 'unlik' not in aria_label.lower():
                            # 滚动到按钮位置
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                            time.sleep(1)

                            # 记录点击前状态
                            before_aria = aria_label

                            # 点击按钮
                            self.driver.execute_script("arguments[0].click();", button)
                            liked_count += 1
                            processed_buttons += 1

                            print(f"✅ 第 {liked_count} 个点赞完成 - {before_aria}")

                            # 如果启用了评论功能，在点赞后自动评论
                            if enable_comment:
                                comment_success = self.auto_comment_after_like(comment_text)
                                if comment_success:
                                    print(f"💬 第 {liked_count} 个内容评论完成")
                                else:
                                    print(f"⚠️ 第 {liked_count} 个内容评论失败")

                            # 随机延迟，模拟人类行为
                            delay = random.uniform(3, 6) if enable_comment else random.uniform(2, 5)
                            time.sleep(delay)

                            # 检查点击后的状态变化
                            try:
                                after_aria = button.get_attribute("aria-label") or ""
                                if after_aria != before_aria:
                                    print(f"   状态已更新: {after_aria}")
                            except:
                                pass

                        else:
                            print(f"⏭️ 跳过已点赞的内容: {aria_label}")
                            processed_buttons += 1

                    except Exception as e:
                        print(f"⚠️ 点赞操作失败: {e}")
                        processed_buttons += 1
                        continue

                # 如果处理了所有按钮但还没达到目标数量，滚动页面加载更多内容
                if liked_count < max_likes and processed_buttons > 0:
                    print("🔄 滚动页面加载更多内容...")
                    self.scroll_page()
                    scroll_attempts += 1
                    time.sleep(3)
                elif processed_buttons == 0:
                    # 如果没有处理任何按钮，也尝试滚动
                    print("🔄 没有找到可处理的按钮，尝试滚动...")
                    self.scroll_page()
                    scroll_attempts += 1
                    time.sleep(3)

            print(f"🎉 点赞操作完成！总共点赞了 {liked_count} 个内容")

            if liked_count > 0:
                return True, f"成功点赞 {liked_count} 个内容"
            else:
                return False, "未能完成任何点赞操作"

        except Exception as e:
            print(f"❌ 执行点赞操作失败: {e}")
            return False, f"点赞操作失败: {e}"

    def scroll_page(self):
        """滚动页面"""
        try:
            # 滚动到页面底部
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            # 再滚动回一点，确保加载新内容
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 1000);")
        except Exception as e:
            print(f"⚠️ 滚动页面失败: {e}")

    def login_and_like(self, username, password, target_url="https://www.instagram.com/?next=%2F", max_likes=10, enable_comment=False, comment_text="很棒的分享！👍"):
        """完整的登录和点赞流程 - 复用现有登录功能"""
        try:
            print("=== Instagram 自动登录和点赞 ===")

            # 1. 设置浏览器
            if not self.setup_driver():
                return False, "浏览器初始化失败"

            # 2. 使用现有自动化模块进行登录
            success, message = self.login_with_existing_automation(username, password)
            if not success:
                return False, f"登录失败: {message}"

            print("✅ 登录成功，准备导航到目标页面...")

            # 3. 等待登录完成并导航到指定页面
            try:
                print("⏳ 等待登录完成...")
                time.sleep(3)

                # 检查当前页面状态
                current_url = self.driver.current_url
                print(f"📍 当前页面: {current_url}")

                # 强制导航到目标页面
                print(f"🔄 导航到目标页面: {target_url}")
                self.driver.get(target_url)

                # 等待页面加载
                time.sleep(5)

                # 验证导航是否成功
                final_url = self.driver.current_url
                print(f"📍 导航后页面: {final_url}")

                if "instagram.com" in final_url and "login" not in final_url.lower():
                    print("✅ 成功导航到目标页面")
                else:
                    print("⚠️ 可能还在登录页面，但尝试继续操作")

            except Exception as e:
                print(f"⚠️ 导航过程中出现问题: {e}，尝试继续在当前页面点赞")

            # 4. 执行点赞操作
            success, message = self.perform_likes(max_likes, enable_comment, comment_text)

            if success:
                return True, f"登录和点赞操作成功完成！{message}"
            else:
                return False, f"点赞操作失败: {message}"

        except Exception as e:
            print(f"❌ 完整流程执行失败: {e}")
            return False, f"操作失败: {e}"

    def close_browser(self):
        """关闭浏览器"""
        try:
            if self.driver:
                self.driver.quit()
                print("✅ 浏览器已关闭")
        except Exception as e:
            print(f"⚠️ 关闭浏览器时出现错误: {e}")


def main():
    """测试主函数"""
    automation = InstagramLikeAutomation()

    try:
        # 测试登录和点赞
        username = input("请输入用户名: ")
        password = input("请输入密码: ")
        max_likes = int(input("请输入最大点赞数 (默认10): ") or "10")

        success, message = automation.login_and_like(username, password, max_likes=max_likes)

        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")

    except KeyboardInterrupt:
        print("\n操作被用户中断")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    finally:
        automation.close_browser()


if __name__ == "__main__":
    main()
