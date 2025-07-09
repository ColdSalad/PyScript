# -*- coding: utf-8 -*-
"""
Instagram 评论自动化
专注于评论功能，可与点赞自动化配合使用
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class InstagramCommentAutomation:
    """Instagram评论自动化类 - 专注于评论功能"""
    
    # 预定义的评论内容列表
    DEFAULT_COMMENTS = [
        "很棒的分享！👍",
        "太赞了！✨",
        "喜欢这个内容！❤️",
        "非常棒！🔥",
        "真不错！👏",
        "很有意思！😊",
        "支持！💪",
        "精彩！🌟",
        "很棒的作品！🎨",
        "继续加油！💯"
    ]

    def __init__(self, driver=None):
        """初始化评论自动化实例
        
        Args:
            driver: 可选的现有WebDriver实例，如果提供则复用，否则创建新的
        """
        self.driver = driver
        self.wait = None
        self.external_driver = driver is not None  # 标记是否使用外部driver
        
        if self.driver:
            self.wait = WebDriverWait(self.driver, 10)
            print("✅ 复用现有浏览器实例")
        else:
            print("⚠️ 未提供浏览器实例，需要单独初始化")
    
    def get_random_comment(self):
        """随机选择一个评论内容
        
        Returns:
            str: 随机选择的评论内容
        """
        return random.choice(self.DEFAULT_COMMENTS)

    def setup_driver(self):
        """设置浏览器驱动（仅在没有外部driver时使用）"""
        if self.is_external_driver:
            print("✅ 使用外部提供的浏览器实例")
            return True
            
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

    def find_comment_button(self, post_element=None):
        """查找评论按钮
        
        Args:
            post_element: 可选的帖子元素，如果提供则在该元素内查找评论按钮
        
        Returns:
            评论按钮元素或None
        """
        try:
            print("🔍 正在查找评论按钮...")
            
            # 如果提供了帖子元素，在其内部查找
            search_context = post_element if post_element else self.driver
            
            # 多种评论按钮选择器
            comment_selectors = [
                # 通过aria-label查找
                'button[aria-label*="评论"]',
                'button[aria-label*="Comment"]',
                'div[role="button"][aria-label*="评论"]',
                'div[role="button"][aria-label*="Comment"]',
                # 通过SVG图标查找
                'section button svg[aria-label*="评论"]',
                'section button svg[aria-label*="Comment"]',
                'section div[role="button"] svg[aria-label*="评论"]',
                'section div[role="button"] svg[aria-label*="Comment"]',
                # 通过位置和结构查找（评论按钮通常在点赞按钮旁边）
                'section div.x78zum5 span:nth-child(2) div div div',
                'section div.x78zum5 span:nth-child(2) button',
            ]
            
            for selector in comment_selectors:
                try:
                    if post_element:
                        elements = post_element.find_elements(By.CSS_SELECTOR, selector)
                    else:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        # 检查元素是否可见
                        if element.is_displayed():
                            # 对于SVG元素，需要找到其按钮父元素
                            if element.tag_name == 'svg':
                                button_element = element.find_element(By.XPATH, './ancestor::button | ./ancestor::div[@role="button"]')
                                if button_element:
                                    print(f"✅ 找到评论按钮: {selector}")
                                    return button_element
                            else:
                                print(f"✅ 找到评论按钮: {selector}")
                                return element
                except Exception as e:
                    continue
            
            # 如果上述方法都失败，使用JavaScript查找
            print("🔄 使用JavaScript方法查找评论按钮...")
            js_script = """
            // 查找评论按钮的JavaScript代码
            const buttons = [];
            
            // 方法1: 通过aria-label查找
            const ariaButtons = document.querySelectorAll('button[aria-label], div[role="button"][aria-label]');
            ariaButtons.forEach(btn => {
                const label = btn.getAttribute('aria-label') || '';
                if ((label.includes('评论') || label.toLowerCase().includes('comment')) && btn.offsetParent !== null) {
                    buttons.push(btn);
                }
            });
            
            // 方法2: 通过SVG查找
            if (buttons.length === 0) {
                const svgs = document.querySelectorAll('svg');
                svgs.forEach(svg => {
                    const label = svg.getAttribute('aria-label') || '';
                    if ((label.includes('评论') || label.toLowerCase().includes('comment'))) {
                        const btn = svg.closest('button, div[role="button"]');
                        if (btn && btn.offsetParent !== null && !buttons.includes(btn)) {
                            buttons.push(btn);
                        }
                    }
                });
            }
            
            // 方法3: 通过结构位置查找（评论按钮通常在点赞按钮后面）
            if (buttons.length === 0) {
                const articles = document.querySelectorAll('article');
                articles.forEach(article => {
                    const sections = article.querySelectorAll('section');
                    sections.forEach(section => {
                        const spans = section.querySelectorAll('span');
                        if (spans.length >= 2) {
                            // 第二个span通常是评论按钮
                            const commentSpan = spans[1];
                            const btn = commentSpan.querySelector('button, div[role="button"]');
                            if (btn && btn.offsetParent !== null && !buttons.includes(btn)) {
                                buttons.push(btn);
                            }
                        }
                    });
                });
            }
            
            return buttons.length > 0 ? buttons[0] : null;
            """
            
            comment_button = self.driver.execute_script(js_script)
            if comment_button:
                print("✅ 使用JavaScript找到评论按钮")
                return comment_button
            
            print("❌ 未找到评论按钮")
            return None
            
        except Exception as e:
            print(f"❌ 查找评论按钮失败: {e}")
            return None

    def click_comment_button(self, comment_button):
        """点击评论按钮
        
        Args:
            comment_button: 评论按钮元素
        
        Returns:
            bool: 是否成功点击
        """
        try:
            print("🖱️ 正在点击评论按钮...")
            
            # 滚动到按钮位置
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", comment_button)
            time.sleep(1)
            
            # 尝试多种点击方式
            try:
                # 方式1: 直接点击
                comment_button.click()
                print("✅ 直接点击成功")
            except Exception:
                try:
                    # 方式2: JavaScript点击
                    self.driver.execute_script("arguments[0].click();", comment_button)
                    print("✅ JavaScript点击成功")
                except Exception:
                    # 方式3: 模拟鼠标点击
                    from selenium.webdriver.common.action_chains import ActionChains
                    ActionChains(self.driver).move_to_element(comment_button).click().perform()
                    print("✅ ActionChains点击成功")
            
            # 等待评论框出现
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"❌ 点击评论按钮失败: {e}")
            return False

    def find_comment_input(self):
        """查找评论输入框
        
        Returns:
            评论输入框元素或None
        """
        try:
            print("🔍 正在查找评论输入框...")
            
            # 多种评论输入框选择器
            input_selectors = [
                # 通过placeholder查找
                'textarea[placeholder*="添加评论"]',
                'textarea[placeholder*="Add a comment"]',
                'input[placeholder*="添加评论"]',
                'input[placeholder*="Add a comment"]',
                # 通过aria-label查找
                'textarea[aria-label*="添加评论"]',
                'textarea[aria-label*="Add a comment"]',
                'input[aria-label*="添加评论"]',
                'input[aria-label*="Add a comment"]',
                # 通用选择器
                'textarea[data-testid="add-comment-textbox"]',
                'form textarea',
                'form input[type="text"]',
                # 更通用的选择器
                'textarea',
                'input[type="text"]'
            ]
            
            for selector in input_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            # 检查是否是评论输入框
                            placeholder = element.get_attribute('placeholder') or ''
                            aria_label = element.get_attribute('aria-label') or ''
                            
                            if ('评论' in placeholder or 'comment' in placeholder.lower() or
                                '评论' in aria_label or 'comment' in aria_label.lower()):
                                print(f"✅ 找到评论输入框: {selector}")
                                return element
                            
                            # 如果没有明确的评论标识，但是可见的输入框，也尝试使用
                            if selector in ['textarea', 'input[type="text"]']:
                                print(f"✅ 找到可能的评论输入框: {selector}")
                                return element
                                
                except Exception:
                    continue
            
            # 使用JavaScript查找
            print("🔄 使用JavaScript方法查找评论输入框...")
            js_script = """
            // 查找评论输入框
            const inputs = [];
            
            // 查找所有可能的输入元素
            const textareas = document.querySelectorAll('textarea');
            const textInputs = document.querySelectorAll('input[type="text"]');
            
            [...textareas, ...textInputs].forEach(input => {
                if (input.offsetParent !== null) {
                    const placeholder = input.getAttribute('placeholder') || '';
                    const ariaLabel = input.getAttribute('aria-label') || '';
                    
                    if (placeholder.includes('评论') || placeholder.toLowerCase().includes('comment') ||
                        ariaLabel.includes('评论') || ariaLabel.toLowerCase().includes('comment')) {
                        inputs.push(input);
                    }
                }
            });
            
            // 如果没找到明确的评论输入框，返回第一个可见的textarea或text input
            if (inputs.length === 0) {
                const visibleInputs = [...textareas, ...textInputs].filter(input => 
                    input.offsetParent !== null && !input.disabled
                );
                if (visibleInputs.length > 0) {
                    inputs.push(visibleInputs[0]);
                }
            }
            
            return inputs.length > 0 ? inputs[0] : null;
            """
            
            comment_input = self.driver.execute_script(js_script)
            if comment_input:
                print("✅ 使用JavaScript找到评论输入框")
                return comment_input
            
            print("❌ 未找到评论输入框")
            return None
            
        except Exception as e:
            print(f"❌ 查找评论输入框失败: {e}")
            return None

    def input_comment(self, comment_input, comment_text):
        """输入评论内容
        
        Args:
            comment_input: 评论输入框元素
            comment_text: 要输入的评论内容
        
        Returns:
            bool: 是否成功输入
        """
        try:
            print(f"⌨️ 正在输入评论: {comment_text}")
            
            # 清空输入框
            comment_input.clear()
            time.sleep(0.5)
            
            # 点击输入框确保焦点
            comment_input.click()
            time.sleep(0.5)
            
            # 输入评论内容
            comment_input.send_keys(comment_text)
            time.sleep(1)
            
            print("✅ 评论内容输入成功")
            return True
            
        except Exception as e:
            print(f"❌ 输入评论内容失败: {e}")
            return False

    def submit_comment(self, comment_input):
        """提交评论
        
        Args:
            comment_input: 评论输入框元素
        
        Returns:
            bool: 是否成功提交
        """
        try:
            print("📤 正在提交评论...")
            
            # 方法1: 查找发送按钮
            send_button = None
            send_selectors = [
                'button[type="submit"]',
                'button:contains("发布")',
                'button:contains("Post")',
                'div[role="button"]:contains("发布")',
                'div[role="button"]:contains("Post")',
                # 通过位置查找（发送按钮通常在输入框附近）
                'form button',
                'button'
            ]
            
            for selector in send_selectors:
                try:
                    if ':contains(' in selector:
                        # 使用XPath处理包含文本的选择器
                        text = selector.split(':contains("')[1].split('")')[0]
                        xpath = f"//button[contains(text(), '{text}')] | //div[@role='button'][contains(text(), '{text}')]"
                        elements = self.driver.find_elements(By.XPATH, xpath)
                    else:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            send_button = element
                            break
                    
                    if send_button:
                        break
                        
                except Exception:
                    continue
            
            # 如果找到发送按钮，点击它
            if send_button:
                try:
                    send_button.click()
                    print("✅ 点击发送按钮成功")
                    return True
                except Exception:
                    try:
                        self.driver.execute_script("arguments[0].click();", send_button)
                        print("✅ JavaScript点击发送按钮成功")
                        return True
                    except Exception:
                        pass
            
            # 方法2: 使用回车键提交
            try:
                comment_input.send_keys(Keys.RETURN)
                print("✅ 使用回车键提交成功")
                return True
            except Exception:
                pass
            
            # 方法3: 使用Ctrl+Enter提交
            try:
                comment_input.send_keys(Keys.CONTROL + Keys.RETURN)
                print("✅ 使用Ctrl+Enter提交成功")
                return True
            except Exception:
                pass
            
            print("❌ 所有提交方法都失败")
            return False
            
        except Exception as e:
            print(f"❌ 提交评论失败: {e}")
            return False

    def add_comment_to_post(self, comment_text=None, post_element=None):
        """为帖子添加评论
        
        Args:
            comment_text: 评论内容，如果为空则使用随机评论
            post_element: 可选的帖子元素，如果提供则为该帖子添加评论
        
        Returns:
            bool: 是否成功添加评论
        """
        try:
            # 如果没有提供评论内容或使用默认内容，则随机选择
            if not comment_text or comment_text == "很棒的分享！👍":
                comment_text = self.get_random_comment()
                print(f"🎲 使用随机评论: {comment_text}")
            else:
                print(f"💬 使用指定评论: {comment_text}")
            
            # 1. 查找评论按钮
            comment_button = self.find_comment_button(post_element)
            if not comment_button:
                return False
            
            # 2. 点击评论按钮
            if not self.click_comment_button(comment_button):
                return False
            
            # 3. 查找评论输入框
            comment_input = self.find_comment_input()
            if not comment_input:
                return False
            
            # 4. 输入评论内容
            if not self.input_comment(comment_input, comment_text):
                return False
            
            # 5. 提交评论
            if not self.submit_comment(comment_input):
                return False
            
            # 等待评论提交完成
            time.sleep(2)
            
            print("✅ 评论添加成功")
            return True
            
        except Exception as e:
            print(f"❌ 添加评论失败: {e}")
            return False

    def add_comments_to_multiple_posts(self, comment_texts, max_comments=5):
        """为多个帖子添加评论
        
        Args:
            comment_texts: 评论内容列表
            max_comments: 最大评论数量
        
        Returns:
            tuple: (成功数量, 总尝试数量)
        """
        try:
            print(f"💬 开始批量评论，最大评论数: {max_comments}")
            
            if not comment_texts:
                comment_texts = ["很棒的分享！👍", "喜欢这个内容！❤️", "太有趣了！😊"]
            
            success_count = 0
            attempt_count = 0
            
            # 查找页面上的所有帖子
            articles = self.driver.find_elements(By.CSS_SELECTOR, 'article')
            print(f"📍 找到 {len(articles)} 个帖子")
            
            for i, article in enumerate(articles):
                if attempt_count >= max_comments:
                    break
                
                try:
                    print(f"\n🔄 处理第 {i+1} 个帖子...")
                    
                    # 滚动到帖子位置
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", article)
                    time.sleep(2)
                    
                    # 随机选择评论内容
                    comment_text = random.choice(comment_texts)
                    
                    # 为当前帖子添加评论
                    if self.add_comment_to_post(comment_text, article):
                        success_count += 1
                        print(f"✅ 第 {attempt_count + 1} 条评论成功")
                    else:
                        print(f"❌ 第 {attempt_count + 1} 条评论失败")
                    
                    attempt_count += 1
                    
                    # 随机延迟，模拟人类行为
                    delay = random.uniform(3, 8)
                    print(f"⏳ 等待 {delay:.1f} 秒...")
                    time.sleep(delay)
                    
                except Exception as e:
                    print(f"⚠️ 处理第 {i+1} 个帖子时出错: {e}")
                    attempt_count += 1
                    continue
            
            print(f"\n🎉 批量评论完成！成功 {success_count}/{attempt_count} 条评论")
            return success_count, attempt_count
            
        except Exception as e:
            print(f"❌ 批量评论失败: {e}")
            return 0, 0

    def close_browser(self):
        """关闭浏览器（仅在非外部driver时）"""
        try:
            if self.driver and not self.external_driver:
                self.driver.quit()
                print("✅ 浏览器已关闭")
            elif self.external_driver:
                print("ℹ️ 使用外部浏览器实例，不关闭浏览器")
        except Exception as e:
            print(f"⚠️ 关闭浏览器时出现错误: {e}")


def main():
    """测试主函数"""
    automation = InstagramCommentAutomation()
    
    try:
        # 设置浏览器
        if not automation.setup_driver():
            print("❌ 浏览器初始化失败")
            return
        
        # 这里需要先登录Instagram（可以手动登录或集成登录功能）
        print("请手动登录Instagram，然后按回车继续...")
        input()
        
        # 测试评论功能
        comment_texts = ["很棒的分享！👍", "喜欢这个内容！❤️", "太有趣了！😊", "感谢分享！🙏"]
        max_comments = int(input("请输入最大评论数 (默认3): ") or "3")
        
        success_count, total_count = automation.add_comments_to_multiple_posts(comment_texts, max_comments)
        
        if success_count > 0:
            print(f"✅ 评论测试完成！成功 {success_count}/{total_count} 条评论")
        else:
            print(f"❌ 评论测试失败")
            
    except KeyboardInterrupt:
        print("\n操作被用户中断")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    finally:
        automation.close_browser()


if __name__ == "__main__":
    main()