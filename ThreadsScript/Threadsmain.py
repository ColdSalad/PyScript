import asyncio
import random
import time
import json
import base64
import platform
import os
import winreg  # 仅适用于Windows
import shutil  # 适用于Linux和macOS
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
        self.home_Browse = bool(data["SendData"]["ConfigDatas"]["Home_IsEnableBrowse"])  # 是否主頁留言
        self.home_like = bool(data["SendData"]["ConfigDatas"]["Home_IsEnableLike"])#主頁點贊
        self.home_comment = bool(data["SendData"]["ConfigDatas"]["Home_IsEnableLeave"])#主頁留言
        self.message_limit = int(data["SendData"]["ConfigDatas"]["Home_HomeBrowseCount"])  # 主頁發送數
        self.user_Tracking = bool(data["SendData"]["ConfigDatas"]["IsTracking"])  # 是否用户追踪
        self.user_Tracking_num = bool(data["SendData"]["ConfigDatas"]["Tracking_UserCount"])  # 追踪数
        self.IsKey = bool(data["SendData"]["ConfigDatas"]["IsKey"])  # 是否关键字
        self.Key = bool(data["SendData"]["ConfigDatas"]["Key"])  # 关键字
        self.Key_num = bool(data["SendData"]["ConfigDatas"]["Key_LeaveCount"])  # 关键字发送贴文数
        self.Like = bool(data["SendData"]["ConfigDatas"]["IsLike"])  # 点赞
        self.Leave = bool(data["SendData"]["ConfigDatas"]["IsLeave"])  # 留言
        self.is_message = bool(data["SendData"]["ConfigDatas"]["IsPersonalSend"])  # 是否发文
        self.message_pic = bool(data["SendData"]["ConfigDatas"]["IsAddPic"])  # 发送图片
        self.fans = bool(data["SendData"]["ConfigDatas"]["IsAtFans"])  # 是否@粉丝
        self.fans_num = bool(data["SendData"]["ConfigDatas"]["AtFansCount"])  # @粉丝数
        self.leave_text = data["SendData"]["ConfigDatas"]["MsgText"].split("\n\n\n")  # 发文内容
        self.leavetext_messags = str(data["SendData"]["LeaveText"]).split("\n\n\n")  # 留言内容
        self.UsersLists = userslists

    async def start(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=False, executable_path=self.browser_path)
        context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )

        # 应用cookies到上下文
        if self.cookies:

            await context.add_cookies(self.cookies)
            print("已应用cookies到浏览器上下文")
        print("已确认登录状态，开始执行任务...")
        self.page = await context.new_page()

        # await self.automate_clicks()#个人主页留言
        await self.Usersmissing()  # 用户个人主页留言

    async def automate_clicks(self):
        await self.page.goto(url="https://www.threads.com/", wait_until='load')
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
                            # 定位留言框并输入内容
                            comment_box_selector = "#barcelona-page-layout > div > div > div.xb57i2i.x1q594ok.x5lxg6s.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.x1l7klhg.xs83m0k.x2lwn1j.xx8ngbg.xwo3gff.x1oyok0e.x1odjw0f.x1n2onr6.xq1qtft.xz401s1.x195bbgf.xgb0k9h.x1l19134.xgjo3nb.x1ga7v0g.x15mokao.x18b5jzi.x1q0q8m5.x1t7ytsu.x1ejq31n.xt8cgyo.x128c8uf.x1co6499.xc5fred.x1ma7e2m.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x6ikm8r.xy5w88m.xh8yej3.xbwb3hm.xgh35ic.x19xvnzb.x87ppg5.xev1tu8.xpr2fh2.xgzc8be.x1y1aw1k > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div.x1c1b4dv.x13dflua.x11xpdln > div > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div:nth-child({}) > div > div > div > div > div.x49hn82.xcrlgei.xz9dl7a.xsag5q8 > div > div > div.x78zum5.xdt5ytf.xfp3qos.xh8yej3 > div.x78zum5.xh8yej3 > div.x78zum5.x1cvoeml.xdt5ytf.xh8yej3 > div.x1ed109x.x7r5mf7.xh8yej3 > div > div.xzsf02u.xw2csxc.x1odjw0f.x1n2onr6.x1hnll1o.xpqswwc.notranslate".format(
                                i)
                            comment_box = await self.page.wait_for_selector(comment_box_selector, timeout=5000)

                            if comment_box:
                                # 输入留言内容
                                await comment_box.click()

                                random_test = random.randint(0, len(self.leavetext_messags) - 1)

                                await comment_box.fill(self.leavetext_messags[random_test])
                                print(f"已输入留言内容: {self.leavetext_messags[random_test]}")

                                # 等待发送按钮出现
                                await asyncio.sleep(2)

                                # 定位并点击发送按钮
                                send_button_selector = "#barcelona-page-layout > div > div > div.xb57i2i.x1q594ok.x5lxg6s.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.x1l7klhg.xs83m0k.x2lwn1j.xx8ngbg.xwo3gff.x1oyok0e.x1odjw0f.x1n2onr6.xq1qtft.xz401s1.x195bbgf.xgb0k9h.x1l19134.xgjo3nb.x1ga7v0g.x15mokao.x18b5jzi.x1q0q8m5.x1t7ytsu.x1ejq31n.xt8cgyo.x128c8uf.x1co6499.xc5fred.x1ma7e2m.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x6ikm8r.xy5w88m.xh8yej3.xbwb3hm.xgh35ic.x19xvnzb.x87ppg5.xev1tu8.xpr2fh2.xgzc8be.x1y1aw1k > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div.x1c1b4dv.x13dflua.x11xpdln > div > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div:nth-child({}) > div > div > div > div > div.x49hn82.xcrlgei.xz9dl7a.xsag5q8 > div > div > div.x78zum5.xdt5ytf.xfp3qos.xh8yej3 > div.x78zum5.xh8yej3 > div.xuk3077.x78zum5.xdt5ytf.x1qughib.x1yrsyyn > div > div.x1i10hfl.xjqpnuy.xc5r6h4.xqeqjp1.x1phubyo.x13fuv20.x18b5jzi.x1q0q8m5.x1t7ytsu.x972fbf.x10w94by.x1qhh985.x14e42zd.x1ypdohk.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x14z9mp.xat24cr.x1lziwak.x2lwn1j.xeuugli.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x1lku1pv.x1a2a7pz.x6s0dn4.x9f619.x3nfvp2.x1s688f.xl56j7k.x87ps6o.xuxw1ft.x111bo7f.x1c9tyrk.xeusxvb.x1pahc9y.x1ertn4p.x10w6t97.xx6bhzk.x12w9bfk.x11xpdln.x1td3qas.xd3so5o.x1lcra6a".format(
                                    i)
                                send_button = await self.page.wait_for_selector(send_button_selector, timeout=5000)

                                if send_button:
                                    await send_button.click()
                                    print(f"成功发送留言第 {i} 个帖子")
                                    # 等待留言发送完成
                                    await asyncio.sleep(2)
                                else:
                                    print(f"发送按钮未找到，第 {i} 个帖子")
                            else:
                                print(f"留言框未找到，第 {i} 个帖子")
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
            self.browser = await playwright.chromium.launch(headless=False, executable_path=self.browser_path)
            self.page = await self.browser.new_page(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            )

            await self.page.goto(url="https://www.threads.net/login", wait_until='load')
            await asyncio.sleep(1)

            # 输入凭证
            await self.page.locator("form input").first.fill(self.username)
            await self.page.locator("form input").nth(1).fill(self.password)
            await self.page.click("form div[role='button']")

            # 检查登录是否成功
            try:
                await self.page.wait_for_url("https://www.threads.net/?login_success=true", timeout=15000)
                self.is_logged_in = True
            except:
                current_url = await self.page.evaluate("() => window.location.href")
                if "login" in current_url or "challenge" in current_url:
                    print(f"登录失败，当前URL: {current_url}")
                    self.is_logged_in = False
                    await self.browser.close()
                    raise Exception("登录失败，请检查用户名和密码")

            # 登录成功处理
            self.cookies = await self.page.context.cookies()
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
        for i in range(len(self.UsersLists)):
            await self.page.goto(url="https://www.threads.com/@"+str(self.UsersLists[i]), wait_until='load')
            await asyncio.sleep(8)

            if self.user_Tracking:
                print("追踪")
                await self.UsersTracking()
            if self.fans:
                print("@粉丝")
                await self.UsersFans()
            if self.Like:
                print("点赞")
                number = 1
                htmljs = "#barcelona-page-layout > div > div > div.xb57i2i.x1q594ok.x5lxg6s.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.x1l7klhg.xs83m0k.x2lwn1j.xx8ngbg.xwo3gff.x1oyok0e.x1odjw0f.x1n2onr6.xq1qtft.xz401s1.x195bbgf.xgb0k9h.x1l19134.xgjo3nb.x1ga7v0g.x15mokao.x18b5jzi.x1q0q8m5.x1t7ytsu.x1ejq31n.xt8cgyo.x128c8uf.x1co6499.xc5fred.x1ma7e2m.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x6ikm8r.xy5w88m.xh8yej3.xbwb3hm.xgh35ic.x19xvnzb.x87ppg5.xev1tu8.xpr2fh2.xgzc8be.x1iorvi4 > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div.x1c1b4dv.x13dflua.x11xpdln > div > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div:nth-child({}) > div > div > div > div > div.x1xdureb.xkbb5z.x13vxnyz > div > div.x4vbgl9.x1qfufaz.x1k70j0n > div "
                # await self.UsersLike(number, htmljs)

            if self.Leave:
                print("留言")
                number = 1
                htmljs = "#barcelona-page-layout > div > div > div.xb57i2i.x1q594ok.x5lxg6s.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.x1l7klhg.xs83m0k.x2lwn1j.xx8ngbg.xwo3gff.x1oyok0e.x1odjw0f.x1n2onr6.xq1qtft.xz401s1.x195bbgf.xgb0k9h.x1l19134.xgjo3nb.x1ga7v0g.x15mokao.x18b5jzi.x1q0q8m5.x1t7ytsu.x1ejq31n.xt8cgyo.x128c8uf.x1co6499.xc5fred.x1ma7e2m.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x6ikm8r.xy5w88m.xh8yej3.xbwb3hm.xgh35ic.x19xvnzb.x87ppg5.xev1tu8.xpr2fh2.xgzc8be.x1iorvi4 > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div.x1c1b4dv.x13dflua.x11xpdln > div > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div:nth-child({}) > div > div > div > div > div.x1xdureb.xkbb5z.x13vxnyz > div > div.x4vbgl9.x1qfufaz.x1k70j0n > div "
                htmljsinput = "#barcelona-page-layout > div > div > div.xb57i2i.x1q594ok.x5lxg6s.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.x1l7klhg.xs83m0k.x2lwn1j.xx8ngbg.xwo3gff.x1oyok0e.x1odjw0f.x1n2onr6.xq1qtft.xz401s1.x195bbgf.xgb0k9h.x1l19134.xgjo3nb.x1ga7v0g.x15mokao.x18b5jzi.x1q0q8m5.x1t7ytsu.x1ejq31n.xt8cgyo.x128c8uf.x1co6499.xc5fred.x1ma7e2m.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x6ikm8r.xy5w88m.xh8yej3.xbwb3hm.xgh35ic.x19xvnzb.x87ppg5.xev1tu8.xpr2fh2.xgzc8be.x1iorvi4 > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div.x1c1b4dv.x13dflua.x11xpdln > div > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div:nth-child({}) > div > div > div > div > div.x49hn82.xcrlgei.xz9dl7a.xsag5q8 > div > div > div.x78zum5.xdt5ytf.xfp3qos.xh8yej3 > div > div.x78zum5.x1cvoeml.xdt5ytf.xh8yej3 > div.x1ed109x.x7r5mf7.xh8yej3 > div > div.xzsf02u.xw2csxc.x1odjw0f.x1n2onr6.x1hnll1o.xpqswwc.notranslate"
                htmljsbut = "#barcelona-page-layout > div > div > div.xb57i2i.x1q594ok.x5lxg6s.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.x1l7klhg.xs83m0k.x2lwn1j.xx8ngbg.xwo3gff.x1oyok0e.x1odjw0f.x1n2onr6.xq1qtft.xz401s1.x195bbgf.xgb0k9h.x1l19134.xgjo3nb.x1ga7v0g.x15mokao.x18b5jzi.x1q0q8m5.x1t7ytsu.x1ejq31n.xt8cgyo.x128c8uf.x1co6499.xc5fred.x1ma7e2m.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x6ikm8r.xy5w88m.xh8yej3.xbwb3hm.xgh35ic.x19xvnzb.x87ppg5.xev1tu8.xpr2fh2.xgzc8be.x1iorvi4 > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div.x1c1b4dv.x13dflua.x11xpdln > div > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div:nth-child({}) > div > div > div > div > div.x49hn82.xcrlgei.xz9dl7a.xsag5q8 > div > div > div.x78zum5.xdt5ytf.xfp3qos.xh8yej3 > div > div.xuk3077.x78zum5.xdt5ytf.x1qughib.x1yrsyyn > div > div.x1i10hfl.xjqpnuy.xc5r6h4.xqeqjp1.x1phubyo.x13fuv20.x18b5jzi.x1q0q8m5.x1t7ytsu.x972fbf.x10w94by.x1qhh985.x14e42zd.x1ypdohk.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x14z9mp.xat24cr.x1lziwak.x2lwn1j.xeuugli.xexx8yu.xyri2b.x18d9i69.x1c1uobl.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x1lku1pv.x1a2a7pz.x6s0dn4.x9f619.x3nfvp2.x1s688f.xl56j7k.x87ps6o.xuxw1ft.x111bo7f.x1c9tyrk.xeusxvb.x1pahc9y.x1ertn4p.x10w6t97.xx6bhzk.x12w9bfk.x11xpdln.x1td3qas.xd3so5o.x1lcra6a"
                # await self.UsersLeave(number, htmljs, htmljsinput, htmljsbut)

    async def UsersTracking(self):
        try:
            base_selector = "#barcelona-page-layout > div > div > div.xb57i2i.x1q594ok.x5lxg6s.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.x1l7klhg.xs83m0k.x2lwn1j.xx8ngbg.xwo3gff.x1oyok0e.x1odjw0f.x1n2onr6.xq1qtft.xz401s1.x195bbgf.xgb0k9h.x1l19134.xgjo3nb.x1ga7v0g.x15mokao.x18b5jzi.x1q0q8m5.x1t7ytsu.x1ejq31n.xt8cgyo.x128c8uf.x1co6499.xc5fred.x1ma7e2m.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x6ikm8r.xy5w88m.xh8yej3.xbwb3hm.xgh35ic.x19xvnzb.x87ppg5.xev1tu8.xpr2fh2.xgzc8be.x1iorvi4 > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div:nth-child(2) > div > div:nth-child(1)"
            element = await self.page.wait_for_selector(base_selector, timeout=10000)
            if element:
                await element.scroll_into_view_if_needed()
                await asyncio.sleep(1)
                await element.click()
                print(f"成功点击追踪")
            await asyncio.sleep(8)
        except Exception as e:
            print(f"使用完整路径选择器也失败: {str(e)}")

    async def UsersFans(self):
        try:
            base_selector = "#barcelona-page-layout > div > div > div.xb57i2i.x1q594ok.x5lxg6s.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.x1l7klhg.xs83m0k.x2lwn1j.xx8ngbg.xwo3gff.x1oyok0e.x1odjw0f.x1n2onr6.xq1qtft.xz401s1.x195bbgf.xgb0k9h.x1l19134.xgjo3nb.x1ga7v0g.x15mokao.x18b5jzi.x1q0q8m5.x1t7ytsu.x1ejq31n.xt8cgyo.x128c8uf.x1co6499.xc5fred.x1ma7e2m.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x6ikm8r.xy5w88m.xh8yej3.xbwb3hm.xgh35ic.x19xvnzb.x87ppg5.xev1tu8.xpr2fh2.xgzc8be.x1iorvi4 > div.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6 > div:nth-child(2) > div > div:nth-child(2)"
            element = await self.page.wait_for_selector(base_selector, timeout=10000)
            if element:
                await element.scroll_into_view_if_needed()
                await asyncio.sleep(1)
                await element.click()
                print(f"成功点击提及")
            await asyncio.sleep(8)
        except Exception as e:
            print(f"使用完整路径选择器也失败: {str(e)}")
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
                            # 定位留言框并输入内容
                            comment_box_selector = htmljsinput.format(
                                i)
                            comment_box = await self.page.wait_for_selector(comment_box_selector, timeout=5000)

                            if comment_box:
                                # 输入留言内容
                                await comment_box.click()

                                random_test = random.randint(0, len(self.leavetext_messags) - 1)

                                await comment_box.fill(self.leavetext_messags[random_test])
                                print(f"已输入留言内容: {self.leavetext_messags[random_test]}")

                                # 等待发送按钮出现
                                await asyncio.sleep(2)

                                # 定位并点击发送按钮
                                send_button_selector = htmljsbut.format(
                                    i)
                                send_button = await self.page.wait_for_selector(send_button_selector, timeout=5000)

                                if send_button:
                                    await send_button.click()
                                    print(f"成功发送留言第 {i} 个帖子")
                                    # 等待留言发送完成
                                    await asyncio.sleep(2)
                                else:
                                    print(f"发送按钮未找到，第 {i} 个帖子")
                            else:
                                print(f"留言框未找到，第 {i} 个帖子")
                await asyncio.sleep(8)
            except Exception as e:
                print(f"使用完整路径选择器也失败: {str(e)}")
                out_count += 1
                if out_count == 3:
                    break
                continue
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