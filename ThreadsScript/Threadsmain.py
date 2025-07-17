import asyncio
import random
import time
import json
import base64
import platform
import os
import winreg  # 仅适用于Windows
import shutil  # 适用于Linux和macOS

import requests
from PyQt5.QtWidgets import QApplication
from Threads_loginwin import win_main
from playwright.async_api import async_playwright

class Crawler:
    def __init__(self, cookies,data,userslists):
        self.username = None
        self.password = None
        self.browser = None
        self.page = None
        self.cookies = cookies
        self.delay = 25
        self.is_logged_in = False
        self.browser_path = get_chrome_path()
        self.home_Browse = parse_bool(data["SendData"]["ConfigDatas"]["Home_IsEnableBrowse"])  # 是否主頁留言
        self.home_like = parse_bool(data["SendData"]["ConfigDatas"]["Home_IsEnableLike"])#主頁點贊
        self.home_comment = parse_bool(data["SendData"]["ConfigDatas"]["Home_IsEnableLeave"])#主頁留言
        self.message_limit = int(data["SendData"]["ConfigDatas"]["Home_HomeBrowseCount"])  # 主頁發送數
        self.user_Tracking = parse_bool(data["SendData"]["ConfigDatas"]["IsTracking"])  # 是否用户追踪
        self.user_Tracking_num = int(data["SendData"]["ConfigDatas"]["Tracking_UserCount"])  # 追踪数
        self.IsKey = parse_bool(data["SendData"]["ConfigDatas"]["IsKey"])  # 是否关键字
        self.Key = str(data["SendData"]["ConfigDatas"]["Key"]).split("#")  # 关键字
        self.Key_num = int(data["SendData"]["ConfigDatas"]["Key_LeaveCount"])  # 关键字发送贴文数
        self.Like = parse_bool(data["SendData"]["ConfigDatas"]["IsLike"])  # 点赞
        self.Leave = parse_bool(data["SendData"]["ConfigDatas"]["IsLeave"])  # 留言
        self.is_message = parse_bool(data["SendData"]["ConfigDatas"]["IsPersonalSend"])  # 是否发文
        self.message_pic = parse_bool(data["SendData"]["ConfigDatas"]["IsAddPic"])  # 发送图片
        self.fans = parse_bool(data["SendData"]["ConfigDatas"]["IsAtFans"])  # 是否@粉丝
        self.fans_num = int(data["SendData"]["ConfigDatas"]["AtFansCount"])  # @粉丝数
        self.leave_text = str(data["SendData"]["ConfigDatas"]["MsgText"]).split("\n\n\n")  # 发文内容
        self.leavetext_messags = str(data["SendData"]["LeaveText"]).split("\n\n\n")  # 留言内容
        self.UsersLists = userslists
        self.new_user_Tracking_num = 0
        self.new_fans_num = 0
        self.init = data
        self.pic_path = None
        self.status_window = None  # 状态窗口引用

    def update_status(self, text):
        """更新状态窗口"""
        if self.status_window:
            # 确保在主线程更新UI
            self.status_window.update_signal.emit(text)
            # 立即处理事件队列
            QApplication.processEvents()

    async def start(self):
        self.update_status("啟動瀏覽器...")
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=False, executable_path=self.browser_path,
                                                        args=['--start-minimized'],
        ignore_default_args=["--enable-automation"])
        context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )

        # 应用cookies到上下文
        if self.cookies:
            await context.add_cookies(self.cookies)
            print("已应用cookies到浏览器上下文")
        print("已确认登录状态，开始执行任务...")
        self.page = await context.new_page()
        # await self.force_minimize_browser()
        if self.home_Browse :
            self.update_status("開始主頁留言...")
            await self.automate_clicks()#个人主页留言

        if self.IsKey :
            self.update_status("開始關鍵字留言...")
            print("关键字")#关键字
            await self.message_key()

        if self.is_message :
            self.update_status("開始個人發文...")
            print("个人发文")#个人发文
            await self.Personal_is_message()
            htmljsinput = '//div[@contenteditable="true" and @aria-placeholder="有什麼新鮮事？"or @contenteditable="true" and @aria-placeholder="有什麼新鮮事嗎？" or @contenteditable="true" and @aria-placeholder="有什么新鲜事？" or @contenteditable="true" and @aria-placeholder="有什么新鲜事吗？"]/p'
            # htmljsbut = '//div[text()="發佈" or text()="发布"]'
            htmljsbut = '//div[@role="dialog"]//div[text()="發佈" or text()="发布"]'
            await self.Personal_post(htmljsinput, htmljsbut)

        await self.Usersmissing()  # 用户个人主页留言

    async def automate_clicks(self):
        await self.page.goto(url="https://www.threads.com/", wait_until='load')
        await self.force_minimize_browser()
        await asyncio.sleep(8)
        """执行自动化点击操作"""
        print("开始执行自动化点击...")
        out_count = 0
        for i in range(1, self.message_limit + 1):
            try:

                base_selector = "#barcelona-page-layout > div > div > div.xb57i2i.x1q594ok.x5lxg6s.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.x1l7klhg.xs83m0k.x2lwn1j.xx8ngbg.xwo3gff.x1oyok0e.x1odjw0f.x1n2onr6.xq1qtft.xz401s1.x195bbgf.xgb0k9h.x1l19134.xgjo3nb.x1ga7v0g.x15mokao.x18b5jzi.x1q0q8m5.x1t7ytsu.x1ejq31n.xt8cgyo.x128c8uf.x1co6499.xc5fred.x1ma7e2m.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x6ikm8r.xy5w88m.xh8yej3.xbwb3hm.xgh35ic.x19xvnzb.x87ppg5.xev1tu8.xpr2fh2.xgzc8be.x1y1aw1k > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div.x1c1b4dv.x13dflua.x11xpdln > div > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div:nth-child({}) > div > div > div > div > div.x1xdureb.xkbb5z.x13vxnyz > div > div.x4vbgl9.x1qfufaz.x1k70j0n > div"
                # 定位帖子元素
                post_selector = base_selector.format(i)
                element = await self.page.wait_for_selector(post_selector, timeout=10000)
                if element:
                    await element.scroll_into_view_if_needed()
                    await asyncio.sleep(1)
                    if self.home_like:#點贊
                        like_selector = post_selector + " > div:nth-child(1) > div"
                        like_btn = await self.page.wait_for_selector(like_selector, timeout=5000)
                        if like_btn:
                            await like_btn.click()
                            self.update_status(f"成功點讚第 {i} 個帖子...")
                            print(f"成功点赞第 {i} 个帖子")
                            await asyncio.sleep(2)

                    await asyncio.sleep(5)

                    if self.home_comment:#留言
                        comment_selector = post_selector + " > div:nth-child(2) > div"
                        comment_btn = await self.page.wait_for_selector(comment_selector, timeout=5000)
                        if comment_btn:
                            await comment_btn.click()
                            print(f"成功点击留言按钮第 {i} 个帖子")

                            # 等待留言框出现
                            await asyncio.sleep(2)
                            comment_box = None
                            try:
                                # 原始选择器
                                comment_box_selector = "#barcelona-page-layout > div > div > div.xb57i2i.x1q594ok.x5lxg6s.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.x1l7klhg.xs83m0k.x2lwn1j.xx8ngbg.xwo3gff.x1oyok0e.x1odjw0f.x1n2onr6.xq1qtft.xz401s1.x195bbgf.xgb0k9h.x1l19134.xgjo3nb.x1ga7v0g.x15mokao.x18b5jzi.x1q0q8m5.x1t7ytsu.x1ejq31n.xt8cgyo.x128c8uf.x1co6499.xc5fred.x1ma7e2m.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x6ikm8r.xy5w88m.xh8yej3.xbwb3hm.xgh35ic.x19xvnzb.x87ppg5.xev1tu8.xpr2fh2.xgzc8be.x1y1aw1k > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div.x1c1b4dv.x13dflua.x11xpdln > div > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div:nth-child({}) > div > div > div > div > div.x49hn82.xcrlgei.xz9dl7a.xsag5q8 > div > div > div.x78zum5.xdt5ytf.xfp3qos.xh8yej3 > div.x78zum5.xh8yej3 > div.x78zum5.x1cvoeml.xdt5ytf.xh8yej3 > div.x1ed109x.x7r5mf7.xh8yej3 > div > div.xzsf02u.xw2csxc.x1odjw0f.x1n2onr6.x1hnll1o.xpqswwc.notranslate".format(
                                    i)
                                comment_box = await self.page.wait_for_selector(comment_box_selector, timeout=3000)
                            except Exception as e:
                                print(f"原始留言框选择器失败: {str(e)}")
                            # 如果原始选择器失败，尝试备用选择器
                            if not comment_box:
                                try:
                                    backup_selector = '//div[@role="dialog"]//div[@aria-label="文本栏为空白。请输入内容，撰写新帖子。" or @aria-label="文字欄位空白。請輸入內容以撰寫新貼文。"]'
                                    comment_box = await self.page.wait_for_selector(backup_selector, timeout=3000)
                                    if comment_box:
                                        print(f"使用备用选择器找到留言框")
                                except Exception as e:
                                    print(f"备用留言框选择器也失败: {str(e)}")
                            if comment_box:
                                # 输入留言内容
                                await comment_box.click()

                                random_test = random.randint(0, len(self.leavetext_messags) - 1)

                                await comment_box.fill(self.leavetext_messags[random_test])
                                self.update_status(f"留言內容: {self.leavetext_messags[random_test]}")
                                print(f"已输入留言内容: {self.leavetext_messags[random_test]}")

                                # 等待发送按钮出现
                                await asyncio.sleep(2)
                                send_button = None
                                try:
                                    # 定位并点击发送按钮
                                    send_button_selector = "#barcelona-page-layout > div > div > div.xb57i2i.x1q594ok.x5lxg6s.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.x1l7klhg.xs83m0k.x2lwn1j.xx8ngbg.xwo3gff.x1oyok0e.x1odjw0f.x1n2onr6.xq1qtft.xz401s1.x195bbgf.xgb0k9h.x1l19134.xgjo3nb.x1ga7v0g.x15mokao.x18b5jzi.x1q0q8m5.x1t7ytsu.x1ejq31n.xt8cgyo.x128c8uf.x1co6499.xc5fred.x1ma7e2m.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x6ikm8r.xy5w88m.xh8yej3.xbwb3hm.xgh35ic.x19xvnzb.x87ppg5.xev1tu8.xpr2fh2.xgzc8be.x1y1aw1k > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div.x1c1b4dv.x13dflua.x11xpdln > div > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div:nth-child({}) > div > div > div > div > div.x49hn82.xcrlgei.xz9dl7a.xsag5q8 > div > div > div.x78zum5.xdt5ytf.xfp3qos.xh8yej3 > div.x78zum5.xh8yej3 > div.xuk3077.x78zum5.xdt5ytf.x1qughib.x1yrsyyn > div > div.x1i10hfl.xjqpnuy.xc5r6h4.xqeqjp1.x1phubyo.x13fuv20.x18b5jzi.x1q0q8m5.x1t7ytsu.x972fbf.x10w94by.x1qhh985.x14e42zd.x1ypdohk.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x14z9mp.xat24cr.x1lziwak.x2lwn1j.xeuugli.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x1lku1pv.x1a2a7pz.x6s0dn4.x9f619.x3nfvp2.x1s688f.xl56j7k.x87ps6o.xuxw1ft.x111bo7f.x1c9tyrk.xeusxvb.x1pahc9y.x1ertn4p.x10w6t97.xx6bhzk.x12w9bfk.x11xpdln.x1td3qas.xd3so5o.x1lcra6a".format(
                                        i)
                                    send_button = await self.page.wait_for_selector(send_button_selector, timeout=5000)
                                except Exception as e:
                                    print(f"原始发送按钮选择器失败: {str(e)}")
                                # 如果原始选择器失败，尝试备用选择器
                                if not send_button:
                                    try:
                                        backup_selector = '//div[@role="dialog"]//div[text()="發佈" or text()="发布"]'
                                        send_button = await self.page.wait_for_selector(backup_selector,
                                                                                        timeout=3000)
                                        if send_button:
                                            print(f"使用备用选择器找到发送按钮")
                                    except Exception as e:
                                        print(f"备用發送按钮选择器也失败: {str(e)}")
                                if send_button:
                                    await send_button.click()
                                    self.update_status(f"成功留言第 {i} 個帖子...")
                                    print(f"成功发送留言第 {i} 个帖子")
                                    # 等待留言发送完成
                                    await asyncio.sleep(2)
                                else:
                                    print(f"发送按钮未找到，第 {i} 个帖子")
                            else:
                                print(f"留言框未找到，第 {i} 个帖子")
                                continue  # 跳过当前帖子的剩余操作
                await asyncio.sleep(8)
            except Exception as e:
                print(f"使用完整路径选择器也失败: {str(e)}")
                out_count += 1
                if out_count == 3:
                    break
                continue

    async def check_cookies_valid(self):
        """检查cookies是否有效"""
        try:
            ds_user_id = next((c for c in self.cookies if c['name'] == "ds_user_id"), None)
            sessionid = next((c for c in self.cookies if c['name'] == "sessionid"), None)
            return ds_user_id and sessionid and sessionid['expires'] > time.time()
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
                executable_path=self.browser_path,
                args=['--start-minimized']  # 确保浏览器启动时最小化
            )
            page = await self.browser.new_page()
            await page.goto(url="https://www.threads.net/login", wait_until='load')
            await asyncio.sleep(1)

            # 输入凭证
            await page.locator("form input").first.fill(self.username)
            await page.locator("form input").nth(1).fill(self.password)
            await page.click("form div[role='button']")

            # 检查登录是否成功
            try:
                await page.wait_for_url("https://www.threads.net/?login_success=true", timeout=25000)
                self.is_logged_in = True
            except:
                current_url = await page.evaluate("() => window.location.href")
                if "login" in current_url or "challenge" in current_url:
                    print(f"登录失败，当前URL: {current_url}")
                    self.is_logged_in = False
                    await self.browser.close()
                    raise Exception("登录失败，请检查用户名和密码")

            # 登录成功处理
            self.cookies = await page.context.cookies()
            with open("threads.json", "w") as f:
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

    # 模拟登录
    async def login(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=False, executable_path=self.browser_path)
        self.page = await self.browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )

        await self.page.goto(url="https://www.threads.net/login", wait_until='load')
        await asyncio.sleep(1)

        username_input = self.page.locator("form input").first
        password_input = self.page.locator("form input").nth(1)
        await username_input.fill(self.username)
        await asyncio.sleep(1)
        await password_input.fill(self.password)
        await asyncio.sleep(1)
        await self.page.click("form div[role='button']")

        await self.page.wait_for_url("https://www.threads.net/?login_success=true")
        await asyncio.sleep(10)

        self.cookies = await self.page.context.cookies()

        with open("threads.json", "w") as f:
            json.dump(self.cookies, f, indent=4)

        if "login" in self.page.url or "challenge" in self.page.url:
            raise Exception("登录失败，请检查用户名和密码")
        else:
            print('登陆成功1')

    # 获取请求Auth签名
    def getBearerAuth(self):
        ds_user_id = next((cookie for cookie in self.cookies if cookie['name'] == "ds_user_id"), None)
        sessionid = next((cookie for cookie in self.cookies if cookie['name'] == "sessionid"), None)
        auth_str = "{\"ds_user_id\":\"" + ds_user_id['value'] + "\",\"sessionid\":\"" + sessionid['value'] + "\"}"
        auth_bytes = auth_str.encode('utf-8')
        auth_str = base64.b64encode(auth_bytes)
        return "Bearer IGT:2:" + auth_str.decode('utf-8')

    async def Usersmissing(self):
        self.update_status("開始用戶個人主頁留言...")
        for i in range(len(self.UsersLists)):
            self.update_status(f"打開用戶：@{self.UsersLists[i]} 主頁")
            await self.page.goto(url="https://www.threads.com/@"+str(self.UsersLists[i]), wait_until='load')
            await self.force_minimize_browser()
            await asyncio.sleep(8)

            if self.user_Tracking and self.new_user_Tracking_num < self.user_Tracking_num:
                self.update_status("用戶追蹤...")
                print("追踪")
                await self.UsersTracking()
            if self.fans and self.new_fans_num < self.fans_num:
                self.update_status("@粉絲發送信息...")
                print("@粉丝")
                await self.UsersFans()
                htmljsinput = '//div[@contenteditable="true" and @aria-placeholder="有什麼新鮮事？"or @contenteditable="true" and @aria-placeholder="有什麼新鮮事嗎？" or @contenteditable="true" and @aria-placeholder="有什么新鲜事？" or @contenteditable="true" and @aria-placeholder="有什么新鲜事吗？"]/p/span[2]'
                htmljsbut = '//div[text()="發佈" or text()="发布"]'
                await self.Personal_post(htmljsinput, htmljsbut)
            if self.Like:
                self.update_status("個人主頁點讚...")
                print("点赞")
                number = 1
                htmljs = "#barcelona-page-layout > div > div > div.xb57i2i.x1q594ok.x5lxg6s.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.x1l7klhg.xs83m0k.x2lwn1j.xx8ngbg.xwo3gff.x1oyok0e.x1odjw0f.x1n2onr6.xq1qtft.xz401s1.x195bbgf.xgb0k9h.x1l19134.xgjo3nb.x1ga7v0g.x15mokao.x18b5jzi.x1q0q8m5.x1t7ytsu.x1ejq31n.xt8cgyo.x128c8uf.x1co6499.xc5fred.x1ma7e2m.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x6ikm8r.xy5w88m.xh8yej3.xbwb3hm.xgh35ic.x19xvnzb.x87ppg5.xev1tu8.xpr2fh2.xgzc8be.x1iorvi4 > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div.x1c1b4dv.x13dflua.x11xpdln > div > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div:nth-child({}) > div > div > div > div > div.x1xdureb.xkbb5z.x13vxnyz > div > div.x4vbgl9.x1qfufaz.x1k70j0n > div "
                await self.UsersLike(number, htmljs)

            if self.Leave:
                self.update_status("個人主頁留言...")
                print("留言")
                number = 1
                htmljs = "#barcelona-page-layout > div > div > div.xb57i2i.x1q594ok.x5lxg6s.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.x1l7klhg.xs83m0k.x2lwn1j.xx8ngbg.xwo3gff.x1oyok0e.x1odjw0f.x1n2onr6.xq1qtft.xz401s1.x195bbgf.xgb0k9h.x1l19134.xgjo3nb.x1ga7v0g.x15mokao.x18b5jzi.x1q0q8m5.x1t7ytsu.x1ejq31n.xt8cgyo.x128c8uf.x1co6499.xc5fred.x1ma7e2m.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x6ikm8r.xy5w88m.xh8yej3.xbwb3hm.xgh35ic.x19xvnzb.x87ppg5.xev1tu8.xpr2fh2.xgzc8be.x1iorvi4 > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div.x1c1b4dv.x13dflua.x11xpdln > div > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div:nth-child({}) > div > div > div > div > div.x1xdureb.xkbb5z.x13vxnyz > div > div.x4vbgl9.x1qfufaz.x1k70j0n > div "
                htmljsinput = "#barcelona-page-layout > div > div > div.xb57i2i.x1q594ok.x5lxg6s.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.x1l7klhg.xs83m0k.x2lwn1j.xx8ngbg.xwo3gff.x1oyok0e.x1odjw0f.x1n2onr6.xq1qtft.xz401s1.x195bbgf.xgb0k9h.x1l19134.xgjo3nb.x1ga7v0g.x15mokao.x18b5jzi.x1q0q8m5.x1t7ytsu.x1ejq31n.xt8cgyo.x128c8uf.x1co6499.xc5fred.x1ma7e2m.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x6ikm8r.xy5w88m.xh8yej3.xbwb3hm.xgh35ic.x19xvnzb.x87ppg5.xev1tu8.xpr2fh2.xgzc8be.x1iorvi4 > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div.x1c1b4dv.x13dflua.x11xpdln > div > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div:nth-child({}) > div > div > div > div > div.x49hn82.xcrlgei.xz9dl7a.xsag5q8 > div > div > div.x78zum5.xdt5ytf.xfp3qos.xh8yej3 > div > div.x78zum5.x1cvoeml.xdt5ytf.xh8yej3 > div.x1ed109x.x7r5mf7.xh8yej3 > div > div.xzsf02u.xw2csxc.x1odjw0f.x1n2onr6.x1hnll1o.xpqswwc.notranslate"
                htmljsbut = "#barcelona-page-layout > div > div > div.xb57i2i.x1q594ok.x5lxg6s.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.x1l7klhg.xs83m0k.x2lwn1j.xx8ngbg.xwo3gff.x1oyok0e.x1odjw0f.x1n2onr6.xq1qtft.xz401s1.x195bbgf.xgb0k9h.x1l19134.xgjo3nb.x1ga7v0g.x15mokao.x18b5jzi.x1q0q8m5.x1t7ytsu.x1ejq31n.xt8cgyo.x128c8uf.x1co6499.xc5fred.x1ma7e2m.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x6ikm8r.xy5w88m.xh8yej3.xbwb3hm.xgh35ic.x19xvnzb.x87ppg5.xev1tu8.xpr2fh2.xgzc8be.x1iorvi4 > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div.x1c1b4dv.x13dflua.x11xpdln > div > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div:nth-child({}) > div > div > div > div > div.x49hn82.xcrlgei.xz9dl7a.xsag5q8 > div > div > div.x78zum5.xdt5ytf.xfp3qos.xh8yej3 > div > div.xuk3077.x78zum5.xdt5ytf.x1qughib.x1yrsyyn > div > div.x1i10hfl.xjqpnuy.xc5r6h4.xqeqjp1.x1phubyo.x13fuv20.x18b5jzi.x1q0q8m5.x1t7ytsu.x972fbf.x10w94by.x1qhh985.x14e42zd.x1ypdohk.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x14z9mp.xat24cr.x1lziwak.x2lwn1j.xeuugli.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x1lku1pv.x1a2a7pz.x6s0dn4.x9f619.x3nfvp2.x1s688f.xl56j7k.x87ps6o.xuxw1ft.x111bo7f.x1c9tyrk.xeusxvb.x1pahc9y.x1ertn4p.x10w6t97.xx6bhzk.x12w9bfk.x11xpdln.x1td3qas.xd3so5o.x1lcra6a"
                await self.UsersLeave(number, htmljs, htmljsinput, htmljsbut)

    async def UsersTracking(self):
        try:
            base_selector = "#barcelona-page-layout > div > div > div.xb57i2i.x1q594ok.x5lxg6s.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.x1l7klhg.xs83m0k.x2lwn1j.xx8ngbg.xwo3gff.x1oyok0e.x1odjw0f.x1n2onr6.xq1qtft.xz401s1.x195bbgf.xgb0k9h.x1l19134.xgjo3nb.x1ga7v0g.x15mokao.x18b5jzi.x1q0q8m5.x1t7ytsu.x1ejq31n.xt8cgyo.x128c8uf.x1co6499.xc5fred.x1ma7e2m.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x6ikm8r.xy5w88m.xh8yej3.xbwb3hm.xgh35ic.x19xvnzb.x87ppg5.xev1tu8.xpr2fh2.xgzc8be.x1iorvi4 > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div:nth-child(2) > div > div:nth-child(1)"
            element = await self.page.wait_for_selector(base_selector, timeout=10000)
            text = await self.page.locator(base_selector).inner_text()
            print("获取的文本：", text)
            if text =="已关注" or text =="追蹤中":
                self.update_status("已經追蹤跳過...")
                return
            if element:
                await element.scroll_into_view_if_needed()
                await asyncio.sleep(1)
                await element.click()
                print(f"成功点击追踪")
                self.new_user_Tracking_num += 1
            await asyncio.sleep(8)
        except Exception as e:
            print(f"使用完整路径选择器也失败: {str(e)}")
            return

    async def UsersFans(self):
        try:
            base_selector = "#barcelona-page-layout > div > div > div.xb57i2i.x1q594ok.x5lxg6s.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.x1l7klhg.xs83m0k.x2lwn1j.xx8ngbg.xwo3gff.x1oyok0e.x1odjw0f.x1n2onr6.xq1qtft.xz401s1.x195bbgf.xgb0k9h.x1l19134.xgjo3nb.x1ga7v0g.x15mokao.x18b5jzi.x1q0q8m5.x1t7ytsu.x1ejq31n.xt8cgyo.x128c8uf.x1co6499.xc5fred.x1ma7e2m.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x6ikm8r.xy5w88m.xh8yej3.xbwb3hm.xgh35ic.x19xvnzb.x87ppg5.xev1tu8.xpr2fh2.xgzc8be.x1iorvi4 > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div:nth-child(2) > div > div:nth-child(2)"
            element = await self.page.wait_for_selector(base_selector, timeout=10000)
            if element:
                await element.scroll_into_view_if_needed()
                await asyncio.sleep(1)
                await element.click()
                print(f"成功点击提及")
                self.new_fans_num += 1
            await asyncio.sleep(5)
        except Exception as e:
            print(f"使用完整路径选择器也失败: {str(e)}")
            return

    async def UsersLike(self,number,htmljs):
        out_count = 0
        self.message_limit = number
        for i in range(1, self.message_limit + 1):
            try:
                base_selector = htmljs
                # 定位帖子元素
                post_selector = base_selector.format(i)
                element = await self.page.wait_for_selector(post_selector, timeout=10000)
                if element:
                    await element.scroll_into_view_if_needed()
                    await asyncio.sleep(1)
                    if self.home_like:  # 點贊
                        like_selector = post_selector + " > div:nth-child(1) > div"
                        like_btn = await self.page.wait_for_selector(like_selector, timeout=5000)
                        if like_btn:
                            await like_btn.click()
                            print(f"成功点赞第 {i} 个帖子")
                            await asyncio.sleep(2)

                await asyncio.sleep(8)
            except Exception as e:
                print(f"使用完整路径选择器也失败: {str(e)}")
                out_count += 1
                if out_count == 3:
                    break
                continue
    async def UsersLeave(self,number,htmljs,htmljsinput,htmljsbut):
        out_count = 0
        self.message_limit = number
        for i in range(1, self.message_limit + 1):
            try:
                base_selector = htmljs
                # 定位帖子元素
                post_selector = base_selector.format(i)
                element = await self.page.wait_for_selector(post_selector, timeout=10000)
                if element:
                    await element.scroll_into_view_if_needed()
                    await asyncio.sleep(1)

                    if self.home_comment:  # 留言
                        comment_selector = post_selector + " > div:nth-child(2) > div"
                        comment_btn = await self.page.wait_for_selector(comment_selector, timeout=5000)
                        if comment_btn:
                            await comment_btn.click()
                            print(f"成功点击留言按钮第 {i} 个帖子")

                            # 等待留言框出现
                            await asyncio.sleep(2)
                            comment_box = None
                            try:
                                # 定位留言框并输入内容
                                comment_box_selector = htmljsinput.format(
                                    i)
                                comment_box = await self.page.wait_for_selector(comment_box_selector, timeout=5000)
                            except Exception as e:
                                print(f"原始留言框选择器失败: {str(e)}")
                            if not comment_box:
                                try:
                                    backup_selector = '//div[@role="dialog"]//div[@aria-label="文本栏为空白。请输入内容，撰写新帖子。" or @aria-label="文字欄位空白。請輸入內容以撰寫新貼文。"]'
                                    comment_box = await self.page.wait_for_selector(backup_selector, timeout=3000)
                                    if comment_box:
                                        print(f"使用备用选择器找到留言框")
                                except Exception as e:
                                    print(f"备用留言框选择器也失败: {str(e)}")
                            if comment_box:
                                # 输入留言内容
                                await comment_box.click()

                                random_test = random.randint(0, len(self.leavetext_messags) - 1)

                                await comment_box.fill(self.leavetext_messags[random_test])
                                self.update_status(f"留言內容: {self.leavetext_messags[random_test]}")
                                print(f"已输入留言内容: {self.leavetext_messags[random_test]}")

                                # 等待发送按钮出现
                                await asyncio.sleep(2)
                                send_button = None
                                try:
                                    # 定位并点击发送按钮
                                    send_button_selector = htmljsbut.format(
                                        i)
                                    send_button = await self.page.wait_for_selector(send_button_selector, timeout=5000)
                                except Exception as e:
                                    print(f"原始发送按钮选择器失败: {str(e)}")
                                if not send_button:
                                    try:
                                        backup_selector = '//div[@role="dialog"]//div[text()="發佈" or text()="发布"]'
                                        send_button = await self.page.wait_for_selector(backup_selector,
                                                                                        timeout=3000)
                                        if send_button:
                                            print(f"使用备用选择器找到发送按钮")
                                    except Exception as e:
                                        print(f"备用發送按钮选择器也失败: {str(e)}")
                                if send_button:
                                    await send_button.click()
                                    print(f"成功发送留言第 {i} 个帖子")
                                    # 等待留言发送完成
                                    await asyncio.sleep(2)
                                else:
                                    print(f"发送按钮未找到，第 {i} 个帖子")
                            else:
                                print(f"留言框未找到，第 {i} 个帖子")
                                continue
                await asyncio.sleep(8)
            except Exception as e:
                print(f"使用完整路径选择器也失败: {str(e)}")
                out_count += 1
                if out_count == 3:
                    break
                continue

    async def Personal_post(self, htmljsinput, htmljsbut):
        print("输入框")
        self.update_status("開始尋找文本框...")
        try:
            # 等待留言框出现
            await asyncio.sleep(2)
            # 定位留言框并输入内容
            comment_box_selector = htmljsinput
            comment_box = await self.page.wait_for_selector(comment_box_selector, timeout=5000)

            if comment_box:
                # 定位帖子元素
                await comment_box.scroll_into_view_if_needed()
                # 输入留言内容
                await comment_box.click()

                random_test = random.randint(0, len(self.leave_text) - 1)

                await comment_box.fill(self.leave_text[random_test])
                self.update_status(f"留言內容: {self.leave_text[random_test]}")
                print(f"已输入留言内容: {self.leave_text[random_test]}")
                if self.message_pic :
                    self.pic_path = GetHtmlpic(self.init)
                    self.update_status("下載圖片...")
                    await asyncio.sleep(2)
                    if  self.pic_path is not None :
                        await asyncio.sleep(2)
                        # 使用文件选择器
                        file_input = await self.page.query_selector('input[type="file"]')
                        if file_input:
                            await file_input.set_input_files(self.pic_path)
                            self.update_status("通过文件选择器上传图片")

                    print(f"已输入图片地址: {self.pic_path}")
                # 等待发送按钮出现
                await asyncio.sleep(2)

                # 定位并点击发送按钮
                send_button_selector = htmljsbut
                send_button = await self.page.wait_for_selector(send_button_selector, timeout=5000)

                if send_button:
                    await send_button.click()
                    print(f"成功发送留言帖子")
                    # 等待留言发送完成
                    await asyncio.sleep(2)
                else:
                    print(f"发送按钮未找到")
            else:
                print(f"留言框未找到")
            await asyncio.sleep(8)
        except Exception as e:
            print(f"使用完整路径选择器也失败: {str(e)}")

    async def message_key(self):
        for num in range(len(self.Key)):
            print(self.Key[num])
            self.update_status(f"關鍵字: "+self.Key[num])
            await self.page.goto(url="https://www.threads.com/search?q=" + str(self.Key[num]), wait_until='load')
            await self.force_minimize_browser()
            await asyncio.sleep(8)

            out_count = 0
            for i in range(1, self.Key_num + 1):
                try:
                    self.update_status(f"開始第 {i} 個帖子...")
                    base_selector = "#barcelona-page-layout > div > div > div.xb57i2i.x1q594ok.x5lxg6s.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.x1l7klhg.xs83m0k.x2lwn1j.xx8ngbg.xwo3gff.x1oyok0e.x1odjw0f.x1n2onr6.xq1qtft.xz401s1.x195bbgf.xgb0k9h.x1l19134.xgjo3nb.x1ga7v0g.x15mokao.x18b5jzi.x1q0q8m5.x1t7ytsu.x1ejq31n.xt8cgyo.x128c8uf.x1co6499.xc5fred.x1ma7e2m.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x6ikm8r.xy5w88m.xh8yej3.xbwb3hm.xgh35ic.x19xvnzb.x87ppg5.xev1tu8.xpr2fh2.xgzc8be.xz9dl7a > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div.x6s0dn4.xamitd3.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6.xh8yej3 > div > div.x1iyjqo2.x14vqqas > div > div > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div:nth-child({}) > div > div > div > div > div.x1xdureb.xkbb5z.x13vxnyz > div > div.x4vbgl9.x1qfufaz.x1k70j0n > div "
                    # 定位帖子元素
                    post_selector = base_selector.format(i)
                    element = await self.page.wait_for_selector(post_selector, timeout=10000)
                    if element:
                        await element.scroll_into_view_if_needed()
                        await asyncio.sleep(1)
                        if self.Like:  # 點贊
                            like_selector = post_selector + " > div:nth-child(1) > div"
                            like_btn = await self.page.wait_for_selector(like_selector, timeout=5000)
                            if like_btn:
                                await like_btn.click()
                                self.update_status(f"成功點讚第 {i} 個帖子...")
                                print(f"成功点赞第 {i} 个帖子")
                                await asyncio.sleep(2)

                        await asyncio.sleep(5)

                        if self.Leave:  # 留言
                            comment_selector = post_selector + " > div:nth-child(2) > div"
                            comment_btn = await self.page.wait_for_selector(comment_selector, timeout=5000)
                            if comment_btn:
                                await comment_btn.click()
                                print(f"成功点击留言按钮第 {i} 个帖子")

                                # 等待留言框出现
                                await asyncio.sleep(2)
                                comment_box = None
                                try:
                                    # 定位留言框并输入内容
                                    comment_box_selector = "#barcelona-page-layout > div > div > div.xb57i2i.x1q594ok.x5lxg6s.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.x1l7klhg.xs83m0k.x2lwn1j.xx8ngbg.xwo3gff.x1oyok0e.x1odjw0f.x1n2onr6.xq1qtft.xz401s1.x195bbgf.xgb0k9h.x1l19134.xgjo3nb.x1ga7v0g.x15mokao.x18b5jzi.x1q0q8m5.x1t7ytsu.x1ejq31n.xt8cgyo.x128c8uf.x1co6499.xc5fred.x1ma7e2m.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x6ikm8r.xy5w88m.xh8yej3.xbwb3hm.xgh35ic.x19xvnzb.x87ppg5.xev1tu8.xpr2fh2.xgzc8be.xz9dl7a > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div.x6s0dn4.xamitd3.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6.xh8yej3 > div > div.x1iyjqo2.x14vqqas > div > div > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div:nth-child({}) > div > div > div > div > div.x49hn82.xcrlgei.xz9dl7a.xsag5q8 > div > div > div.x78zum5.xdt5ytf.xfp3qos.xh8yej3 > div > div.x78zum5.x1cvoeml.xdt5ytf.xh8yej3 > div.x1ed109x.x7r5mf7.xh8yej3 > div > div.xzsf02u.xw2csxc.x1odjw0f.x1n2onr6.x1hnll1o.xpqswwc.notranslate".format(
                                        i)
                                    comment_box = await self.page.wait_for_selector(comment_box_selector, timeout=5000)
                                except Exception as e:
                                    print(f"原始留言框选择器失败: {str(e)}")
                                # 如果原始选择器失败，尝试备用选择器
                                if not comment_box:
                                    try:
                                        backup_selector = '//div[@role="dialog"]//div[@aria-label="文本栏为空白。请输入内容，撰写新帖子。" or @aria-label="文字欄位空白。請輸入內容以撰寫新貼文。"]'
                                        comment_box = await self.page.wait_for_selector(backup_selector, timeout=3000)
                                        if comment_box:
                                            print(f"使用备用选择器找到留言框")
                                    except Exception as e:
                                        print(f"备用留言框选择器也失败: {str(e)}")
                                if comment_box:
                                    # 输入留言内容
                                    await comment_box.click()

                                    random_test = random.randint(0, len(self.leavetext_messags) - 1)

                                    await comment_box.fill(self.leavetext_messags[random_test])
                                    self.update_status(f"留言內容: {self.leavetext_messags[random_test]}")
                                    print(f"已输入留言内容: {self.leavetext_messags[random_test]}")

                                    # 等待发送按钮出现
                                    await asyncio.sleep(2)
                                    send_button = None
                                    try:
                                        # 定位并点击发送按钮
                                        send_button_selector = "#barcelona-page-layout > div > div > div.xb57i2i.x1q594ok.x5lxg6s.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.x1l7klhg.xs83m0k.x2lwn1j.xx8ngbg.xwo3gff.x1oyok0e.x1odjw0f.x1n2onr6.xq1qtft.xz401s1.x195bbgf.xgb0k9h.x1l19134.xgjo3nb.x1ga7v0g.x15mokao.x18b5jzi.x1q0q8m5.x1t7ytsu.x1ejq31n.xt8cgyo.x128c8uf.x1co6499.xc5fred.x1ma7e2m.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x6ikm8r.xy5w88m.xh8yej3.xbwb3hm.xgh35ic.x19xvnzb.x87ppg5.xev1tu8.xpr2fh2.xgzc8be.xz9dl7a > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div.x6s0dn4.xamitd3.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6.xh8yej3 > div > div.x1iyjqo2.x14vqqas > div > div > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div:nth-child({}) > div > div > div > div > div.x49hn82.xcrlgei.xz9dl7a.xsag5q8 > div > div > div.x78zum5.xdt5ytf.xfp3qos.xh8yej3 > div > div.xuk3077.x78zum5.xdt5ytf.x1qughib.x1yrsyyn > div > div.x1i10hfl.xjqpnuy.xc5r6h4.xqeqjp1.x1phubyo.x13fuv20.x18b5jzi.x1q0q8m5.x1t7ytsu.x972fbf.x10w94by.x1qhh985.x14e42zd.x1ypdohk.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x14z9mp.xat24cr.x1lziwak.x2lwn1j.xeuugli.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x1lku1pv.x1a2a7pz.x6s0dn4.x9f619.x3nfvp2.x1s688f.xl56j7k.x87ps6o.xuxw1ft.x111bo7f.x1c9tyrk.xeusxvb.x1pahc9y.x1ertn4p.x10w6t97.xx6bhzk.x12w9bfk.x11xpdln.x1td3qas.xd3so5o.x1lcra6a".format(
                                            i)
                                        send_button = await self.page.wait_for_selector(send_button_selector, timeout=5000)
                                    except Exception as e:
                                        print(f"原始发送按钮选择器失败: {str(e)}")
                                    if not send_button:
                                        try:
                                            backup_selector = '//div[@role="dialog"]//div[text()="發佈" or text()="发布"]'
                                            send_button = await self.page.wait_for_selector(backup_selector,
                                                                                            timeout=3000)
                                            if send_button:
                                                print(f"使用备用选择器找到发送按钮")
                                        except Exception as e:
                                            print(f"备用發送按钮选择器也失败: {str(e)}")
                                    if send_button:
                                        await send_button.click()
                                        self.update_status(f"成功留言第 {i} 個帖子...")
                                        print(f"成功发送留言第 {i} 个帖子")
                                        # 等待留言发送完成
                                        await asyncio.sleep(2)
                                    else:
                                        print(f"发送按钮未找到，第 {i} 个帖子")
                                else:
                                    print(f"留言框未找到，第 {i} 个帖子")
                                    continue
                    await asyncio.sleep(8)
                except Exception as e:
                    print(f"使用完整路径选择器也失败: {str(e)}")
                    self.update_status("被限制留言或當前序號沒有貼文...跳過")
                    out_count += 1
                    if out_count == 3:
                        break
                    continue
    async def Personal_is_message(self):
        await self.page.goto(url="https://www.threads.com/", wait_until='load')
        await self.force_minimize_browser()
        await asyncio.sleep(8)
        try:
            # 等待點擊發文框出现
            await asyncio.sleep(2)
            # 定位點擊發文框
            comment_box_selector = '//div/div[@role="button"]'
            comment_box = await self.page.wait_for_selector(comment_box_selector, timeout=5000)

            if comment_box:
                # 定位帖子元素
                await comment_box.scroll_into_view_if_needed()
                await comment_box.click()

            else:
                print(f"點擊發文框未找到")
            await asyncio.sleep(8)
        except Exception as e:
            print(f"使用完整路径选择器也失败: {str(e)}")
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
def GetHtmlpic(data):
    # 创建img文件夹（如果不存在）
    if not os.path.exists('img'):
        os.makedirs('img')
    if len(data["SendData"]["ConfigDatas"]["SendPicList"]) > 0:
        random_test = random.randint(0, len(data["SendData"]["ConfigDatas"]["SendPicList"]) - 1)
        print(data["SendData"]["ConfigDatas"]["SendPicList"][random_test])
        # 下载图片
        htmlpic = requests.get(data["SendData"]["ConfigDatas"]["SendPicList"][random_test], timeout=30)
        # 图片保存路径
        img_path = os.path.join('img', 'image.png')
        # 保存图片
        with open(img_path, 'wb') as file:
            file.write(htmlpic.content)
        # 返回图片的绝对路径
        return os.path.abspath(img_path)
def parse_bool(type_data):
    type_data = str(type_data).lower().strip()
    if type_data in ('true', 'True', 'TRUE'):
        return True
    elif type_data in ('false', 'False', 'FALSE'):
        return False
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