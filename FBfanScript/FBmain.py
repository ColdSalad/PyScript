import asyncio
import random
import time
import json
import base64
import platform
import os
import winreg  # 仅适用于Windows
import shutil  # 适用于Linux和macOS

import aiohttp
import requests
from PyQt5.QtWidgets import QApplication
from FB_loginwin import win_main
from playwright.async_api import async_playwright

class Crawler:
    def __init__(self, cookies,data,users,start_position,content1):
        self.username = None
        self.password = None
        self.browser = None
        self.page = None
        self.cookies = cookies
        self.delay = 25
        self.is_logged_in = False
        self.browser_path = get_chrome_path()
        self.message_pic = parse_bool(data["SendData"]["SendConfigs"]["IsSendPic"])#是否发送图片
        self.leavetext_messags = str(data["SendData"]["SendText"]).split("\n\n\n")  # 留言内容
        self.new_user_Tracking_num = 0
        self.new_fans_num = 0
        self.pic_path = None
        self.init = data
        self.status_window = None  # 状态窗口引用
        self.UsersLists = users
        self.Start_Position = start_position
        self.User_Id = content1

    def update_status(self, text):
        """更新状态窗口"""
        if self.status_window:
            # 确保在主线程更新UI
            self.status_window.update_signal.emit(text)
            # 立即处理事件队列
            QApplication.processEvents()

    async def start(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=False, executable_path=self.browser_path)
        context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )

        if self.cookies:
            await context.add_cookies(self.cookies)

        self.page = await context.new_page()
        await self.page.goto(url="https://www.facebook.com/", wait_until='load')
        await asyncio.sleep(10)

        num_posts = 6
        print(f"准备与 {num_posts} 个帖子互动")

        for i in range(1, num_posts + 1):

            selector = f'//div[@class="x1hc1fzr x1unhpq9 x6o7n8i"]/div/div/div[{i}]'
            element = await self.page.wait_for_selector(selector, timeout=10000)
            if element:
                await element.scroll_into_view_if_needed()
                print(f"第 {i} 个帖子")
            try:
                # 点赞
                if await self.like_post(i):
                    print(f"第 {i} 个帖子点赞成功")

                a = True
                if a:
                    comments = self.leavetext_messags
                    if await self.comment_post(i, random.choice(comments)):
                        print(f"第 {i} 个帖子留言成功")


                await asyncio.sleep(random.uniform(5, 10))

            except Exception as e:
                print(f"处理第 {i} 个帖子时出错: {str(e)}")
        await self.Usersmissing()  # 用户个人主页留言
        print("任务完成")

    async def like_post(self, index):
        """封装点赞功能"""
        try:
            selector = f'//div[@class="x1hc1fzr x1unhpq9 x6o7n8i"]/div/div/div[{index}]//div[@aria-label="讚" or @aria-label="赞"]'
            element = await self.page.wait_for_selector(selector, timeout=10000)

            if element:
                await element.scroll_into_view_if_needed()
                await asyncio.sleep(1)
                await element.hover()
                await asyncio.sleep(2)

                target_emotion = 1
                target_emotion_list = ["赞", "大心", "加油", "哈", "哇", "嗚", "怒"]
                emotion_selector = f'//div[@role="button" and @aria-label="{target_emotion_list[target_emotion]}"]'

                try:
                    emotion_button = await self.page.wait_for_selector(emotion_selector, timeout=5000)
                    if emotion_button:
                        await emotion_button.click()
                        print(f"点击了表情: {target_emotion_list[target_emotion]}")
                    else:
                        print("未找到表情按钮，执行默认点赞")
                        await element.click()
                except Exception as e:
                    print(f"表情点击失败: {str(e)}")
                    await element.click()
            return True
        except Exception as e:
            print(f"点赞失败: {str(e)}")
            return False

    async def comment_post(self, index, comment_text="你好"):
        """封装留言功能"""
        try:
            # 点击留言按钮
            selector = f'//div[@class="x1hc1fzr x1unhpq9 x6o7n8i"]/div/div/div[{index}]//div[contains(@aria-label, "发表评论") or contains(@aria-label, "留言")]'
            element = await self.page.wait_for_selector(selector, timeout=10000)

            if element:
                await element.scroll_into_view_if_needed()
                await asyncio.sleep(1)
                await element.click()
                await asyncio.sleep(2)
                # 定位留言输入框
                input_selector = '//div[@role="dialog"]//div[@role="textbox" and contains(@aria-label, "留言")]'
                input_element = await self.page.wait_for_selector(input_selector, timeout=10000)

                if input_element:
                    await input_element.scroll_into_view_if_needed()
                    aria_label = await input_element.get_attribute('aria-label')
                    print(f"获取到的 aria-label 为: {aria_label}")
                    if "送出" in aria_label or "回答" in aria_label:
                        submit_cloes = '//div[@role="dialog"]//div[@aria-label="關閉"]'
                        submit_cloes_button = await self.page.wait_for_selector(submit_cloes, timeout=10000)
                        if submit_cloes_button:
                            await submit_cloes_button.scroll_into_view_if_needed()
                            await asyncio.sleep(1)
                            await submit_cloes_button.click()
                            print(f"彈窗關閉！")
                    else:
                        await asyncio.sleep(1)
                        await input_element.click()
                        await input_element.type(comment_text, delay=random.randint(50, 150))
                        await asyncio.sleep(2)
                        try:
                            if self.message_pic:
                                self.pic_path = await GetHtmlpic(self.init)
                                await asyncio.sleep(2)
                                if self.pic_path is not None:
                                    await asyncio.sleep(2)
                                    # 使用文件选择器
                                    file_input = await self.page.query_selector('input[type="file"]')
                                    if file_input:
                                        await file_input.set_input_files(self.pic_path)
                                        self.update_status("通过文件选择器上传图片")

                                print(f"已输入图片地址: {self.pic_path}")
                        except Exception as e:
                            print("没有图片或下载图片失败")
                        # 等待发送按钮出现
                        await asyncio.sleep(2)
                        # 提交留言
                        submit_selector = '//div[@role="dialog"]//div[@id="focused-state-composer-submit"]'
                        submit_button = await self.page.wait_for_selector(submit_selector, timeout=10000)

                        if submit_button:
                            await submit_button.scroll_into_view_if_needed()
                            await asyncio.sleep(1)
                            await submit_button.click()
                            print(f"成功留言: {comment_text}")
                            await asyncio.sleep(random.randint(8, 12))
                            submit_cloes = '//div[@role="dialog"]//div[@aria-label="關閉"]'
                            submit_cloes_button = await self.page.wait_for_selector(submit_cloes, timeout=10000)
                            if submit_cloes_button:
                                await submit_cloes_button.scroll_into_view_if_needed()
                                await asyncio.sleep(1)
                                await submit_cloes_button.click()
                                print(f"彈窗關閉！")
                            return True
            return False
        except Exception as e:
            print(f"留言失败: {str(e)}")
            submit_cloes = '//div[@role="dialog"]//div[@aria-label="關閉"]'
            submit_cloes_button = await self.page.wait_for_selector(submit_cloes, timeout=10000)
            if submit_cloes_button:
                await submit_cloes_button.scroll_into_view_if_needed()
                await asyncio.sleep(1)
                await submit_cloes_button.click()
                print(f"彈窗關閉！")
            return False
    async def check_cookies_valid(self):
        """检查cookies是否有效"""
        try:
            c_user = next((c for c in self.cookies if c["name"] == "c_user"), None)
            xs = next((c for c in self.cookies if c["name"] == "xs"), None)
            current_time = time.time()
            return c_user and xs and xs["expires"] > current_time
        except:
            return False

    async def login_with_gui(self):
        """通过GUI获取凭证并登录"""
        try:
            credentials = win_main()
            if not credentials:
                raise Exception("用户取消登录")

            self.username = credentials["username"]
            self.password = credentials["password"]
            await self.perform_browser_login()
        except Exception as e:
            print(f"GUI登录失败: {str(e)}")
            self.is_logged_in = False

    async def perform_browser_login(self):
        """使用浏览器执行登录"""
        try:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
                headless=False,
                executable_path=self.browser_path
            )
            page = await self.browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
            await page.goto(url="https://www.facebook.com/login", wait_until='load')

            await asyncio.sleep(random.uniform(1.5, 3.5))

            # 模拟人类输入速度
            await page.locator("//input[@id='email']").first.fill(self.username, delay=random.randint(2, 10))
            await asyncio.sleep(random.uniform(0.5, 1.2))
            await page.locator("//input[@id='pass']").fill(self.password, delay=random.randint(3, 8))
            await asyncio.sleep(random.uniform(0.8, 1.5))

            # 点击登录
            await page.click("//button[@id='loginbutton']")

            # 检查登录是否成功
            try:
                await page.wait_for_url("https://www.facebook.com/?lsrc=lb", timeout=120000)
                self.is_logged_in = True
            except:
                current_url = await page.evaluate("() => window.location.href")
                if "login" in current_url or "authentication" in current_url or "checkpoint" in current_url:
                    print(f"登录失败，当前URL: {current_url}")
                    self.is_logged_in = False
                    await self.browser.close()
                    raise Exception("登录失败，请检查用户名和密码")

            # 登录成功处理
            self.cookies = await page.context.cookies()
            with open("FB.json", "w") as f:
                json.dump(self.cookies, f, indent=4)

            print('登录成功')
            self.is_logged_in = True
            await self.browser.close()
        except Exception as e:
            print(f"浏览器登录过程中发生错误: {str(e)}")
            self.is_logged_in = False
            if self.browser:
                await self.browser.close()
            raise Exception(f"登录失败: {str(e)}")

    # 获取请求Auth签名
    def getBearerAuth(self):
        ds_user_id = next((cookie for cookie in self.cookies if cookie['name'] == "ds_user_id"), None)
        sessionid = next((cookie for cookie in self.cookies if cookie['name'] == "sessionid"), None)
        auth_str = "{\"ds_user_id\":\"" + ds_user_id['value'] + "\",\"sessionid\":\"" + sessionid['value'] + "\"}"
        auth_bytes = auth_str.encode('utf-8')
        auth_str = base64.b64encode(auth_bytes)
        return "Bearer IGT:2:" + auth_str.decode('utf-8')

    async def Usersmissing(self):
        # 处理用户列表（从保存的位置开始）
        print(f"从位置 {self.Start_Position} 开始处理")
        for i in range(self.Start_Position, len(self.UsersLists)):
            user_id = self.UsersLists[i]
            print("处理用户ID:", user_id)

            await self.page.goto(url="https://www.facebook.com/"+user_id, wait_until='load')

            await asyncio.sleep(random.uniform(10.5, 13.5))

            # 更新进度
            current_position = i + 1
            save_progress(self.User_Id, self.UsersLists, current_position)

            # 每处理一个用户等待3秒
            await asyncio.sleep(3)

        # 处理完成后清除进度
        clear_progress(self.User_Id)
        print("所有用户处理完成!")

    # 添加新的辅助方法
    def minimize_browser_window(self):
        """最小化浏览器窗口（平台特定实现）"""
        try:
            system = platform.system()
            if system == "Windows":
                import win32gui, win32con
                # 获取浏览器窗口句柄
                time.sleep(1)  # 等待窗口创建
                hwnd = win32gui.GetForegroundWindow()
                if hwnd:
                    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            elif system == "Darwin":  # macOS
                import subprocess
                subprocess.run(["osascript", "-e",
                                'tell application "System Events" to set visible of process "Google Chrome" to false'])
            # Linux 系统需要额外的窗口管理器支持，这里暂不处理
        except Exception as e:
            print(f"最小化窗口失败: {e}")

    async def force_minimize_browser(self):
        """强制最小化浏览器窗口"""
        # 先尝试通过Playwright的方式
        try:
            if self.browser:
                # 获取所有页面
                pages = self.browser.contexts[0].pages if self.browser.contexts else []
                for page in pages:
                    # 尝试最小化窗口
                    await page.evaluate("""() => {
                        if (window.moveTo && window.resizeTo) {
                            window.moveTo(-2000, -2000);
                            window.resizeTo(1, 1);
                        }
                    }""")
        except:
            pass

        # 再使用平台特定的方法
        self.minimize_browser_window()

def parse_bool(type_data):
    type_data = str(type_data).lower().strip()
    return type_data in ('true', '1', 'yes', 'yes')

def save_progress(account, users, position):
    """保存当前处理进度到文件"""
    progress_data = {
        "users": users,
        "position": position
    }
    filename = f"{account}_progress.json"
    with open(filename, 'w') as f:
        json.dump(progress_data, f)
    print(f"保存进度到 {filename}: 位置 {position}/{len(users)}")

def clear_progress(account):
    """清除进度文件"""
    filename = f"{account}_progress.json"
    if os.path.exists(filename):
        os.remove(filename)
        print(f"已清除进度文件 {filename}")

async def GetHtmlpic(data):
    if not data["SendData"]["SendPicList"]:
        return None

    random_test = random.randint(0, len(data["SendData"]["SendPicList"]) - 1)
    url = data["SendData"]["SendPicList"][random_test]

    if not os.path.exists('img'):
        os.makedirs('img')

    img_path = os.path.join('img', 'image.png')

    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=30) as response:
            if response.status == 200:
                with open(img_path, 'wb') as file:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        file.write(chunk)
                return os.path.abspath(img_path)

    return None

def get_chrome_path():
    system = platform.system()

    if system == "Windows":
        # 尝试通过注册表获取安装路径
        try:
            reg_path = r"SOFTWARE\Google\Chrome\BLBeacon"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path) as key:
                install_path = winreg.QueryValueEx(key, "InstallPath")[0]
                chrome_path = os.path.join(install_path, "chrome.exe")
                if os.path.exists(chrome_path):
                    return chrome_path
        except FileNotFoundError:
            pass  # 继续检查默认路径

        # 检查常见的默认安装路径
        possible_paths = [
            os.path.expandvars(r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None

    elif system == "Darwin":
        # macOS的默认安装路径
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        return chrome_path if os.path.exists(chrome_path) else None

    elif system == "Linux":
        # 使用which命令查找或检查常见路径
        chrome_path = shutil.which("google-chrome") or "/usr/bin/google-chrome"
        return chrome_path if os.path.exists(chrome_path) else None

    else:
        return None