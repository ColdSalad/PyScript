import os
import json
import asyncio
import random
import sys
from PyQt5.QtWidgets import QApplication
from Threads_status import StatusWindow
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
        UserRequests = requests.get(
            "https://th.ry188.vip/API/GetUserList.aspx?Count=" + str(getuser_num) + "&Id=" + str(
                data["UserInFIdList"][i]["Id"]), timeout=30).json()
        for k in range(len(UserRequests["UserList"])):
            UserLists.append(UserRequests["UserList"][k]["name"])
    return UserLists


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
        img_path = os.path.join('img', 'img.jpg')
        # 保存图片
        with open(img_path, 'wb') as file:
            file.write(htmlpic.content)
        # 返回图片的绝对路径
        return os.path.abspath(img_path)


async def main(content1):
    cookies = getCookie()  # 从文件读取cookies
    data = requests.get("https://th.ry188.vip/API/GetData.aspx?Account=" + content1, timeout=30).json()
    userslists = GetHtmluser(data)
    image_path = GetHtmlpic(data)
    crawler = Crawler(cookies, data, userslists, image_path)

    # 确保登录成功
    if cookies is None or not await crawler.check_cookies_valid():
        try:
            # 尝试GUI登录
            await crawler.login_with_gui()
            if not crawler.is_logged_in:
                print("登录失败，无法继续执行任务")
                await crawler.login_with_gui()
                # return  # 直接返回，不再执行后续任务
        except Exception as e:
            print(f"登录失败: {str(e)}")
            return  # 登录失败时直接返回
    else:
        # 如果cookies有效，标记为已登录
        crawler.is_logged_in = True
        print("使用有效cookies登录成功")
    try:
        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)

        status_window = StatusWindow()
        status_window.show()
        # 关键修改：将状态窗口传递给crawler对象
        crawler.status_window = status_window

        QApplication.processEvents()  # 确保UI更新
        await crawler.start()
    finally:
        # 确保关闭浏览器
        pass
    return crawler