import os
import json
import asyncio
from Threadsmain import Crawler
def getCookie():
    if not os.path.exists("threads.json"):
        return None
    with open("threads.json", "r") as f:
        try:
            return json.load(f)
        except:
            return None
async def main():
    cookies = getCookie()  # 从文件读取cookies
    crawler = Crawler(cookies)

    # 确保登录成功
    if cookies is None or not await crawler.check_cookies_valid():
        try:
            # 尝试GUI登录
            await crawler.login_with_gui()
            if not crawler.is_logged_in:
                print("登录失败，无法继续执行任务")
                return  # 直接返回，不再执行后续任务
        except Exception as e:
            print(f"登录失败: {str(e)}")
            return  # 登录失败时直接返回
    else:
        # 如果cookies有效，标记为已登录
        crawler.is_logged_in = True
        print("使用有效cookies登录成功")
    try:
        await crawler.start()
    finally:
        # 确保关闭浏览器
        if crawler.browser:
            await crawler.browser.close()
            print("浏览器已关闭")
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("完成！")