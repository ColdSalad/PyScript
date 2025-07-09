import os
import json
import asyncio
import random

import requests

from Threadsmain import Crawler
def getCookie():
    if not os.path.exists("threads.json"):
        return None
    with open("threads.json", "r") as f:
        try:
            return json.load(f)
        except:
            return None
def GetHtmluser(data):
    UserLists = []
    getuser_num = 10
    for i in range(len(data["UserInFIdList"])):
        UserRequests  =  requests.get("https://th.ry188.vip/API/GetUserList.aspx?Count="+str(getuser_num)+"&Id="+str(data["UserInFIdList"][i]["Id"]),timeout=30).json()
        for k in range(len(UserRequests["UserList"])):
            UserLists.append(UserRequests["UserList"][k]["name"])
    return UserLists
async def main(content1):
    cookies = getCookie()  # 从文件读取cookies
    data = requests.get("https://th.ry188.vip/API/GetData.aspx?Account=" + content1, timeout=30).json()
    userslists = GetHtmluser(data)
    crawler = Crawler(cookies,data,userslists)

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
        pass
    return crawler