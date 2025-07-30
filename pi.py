# import time
#
# from selenium import webdriver
# from selenium.common import WebDriverException
# from selenium.webdriver.edge.options import Options
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# chrome_options = Options()
# prefs = {
#     'profile.default_content_setting_values':
#         {
#             'notifications': 2
#         }
# }
# chrome_options.add_experimental_option('prefs', prefs)
# driver = webdriver.Edge(chrome_options)
# driver.get('https://www.facebook.com/')
# time.sleep(10)
# # 查找用户名和密码输入框
# email_element = driver.find_element(By.ID, 'email')
# password_element = driver.find_element(By.ID, 'pass')
# email = "lsning824@Yahoo.com"
# password = "LSn82242"
# email_element.send_keys(email)
# password_element.send_keys(password + Keys.RETURN)
# WebDriverWait(driver, 25).until(EC.url_to_be('https://www.facebook.com/'))
# users_url = "100000383656939"
# driver.get("https://www.facebook.com/profile.php?id="+users_url)  # 访问网站
# time.sleep(6)
# faxinxi_shurubutton = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH,'//div[@class="xq8finb x16n37ib"]/div/div[2]/div'))
#         )
# faxinxi_shurubutton.click()
# time.sleep(3)

import random
import time

# import os
# import platform
# import winreg  # 仅适用于Windows
# import shutil  # 适用于Linux和macOS
#
#
# def get_chrome_path():
#     system = platform.system()
#
#     if system == "Windows":
#         # 尝试通过注册表获取安装路径
#         try:
#             reg_path = r"SOFTWARE\Google\Chrome\BLBeacon"
#             with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path) as key:
#                 install_path = winreg.QueryValueEx(key, "InstallPath")[0]
#                 chrome_path = os.path.join(install_path, "chrome.exe")
#                 if os.path.exists(chrome_path):
#                     return chrome_path
#         except FileNotFoundError:
#             pass  # 继续检查默认路径
#
#         # 检查常见的默认安装路径
#         possible_paths = [
#             os.path.expandvars(r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe"),
#             os.path.expandvars(r"%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe"),
#             os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
#         ]
#         for path in possible_paths:
#             if os.path.exists(path):
#                 return path
#         return None
#
#     elif system == "Darwin":
#         # macOS的默认安装路径
#         chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
#         return chrome_path if os.path.exists(chrome_path) else None
#
#     elif system == "Linux":
#         # 使用which命令查找或检查常见路径
#         chrome_path = shutil.which("google-chrome") or "/usr/bin/google-chrome"
#         return chrome_path if os.path.exists(chrome_path) else None
#
#     else:
#         return None
#
#
# # 使用示例
# path = get_chrome_path()
# if path:
#     print(f"找到Chrome路径: {path}")
# else:
#     print("未找到Chrome安装路径。")

# def duplicates_and_add(lst, string):
#     if string in lst:
#         return False, lst
#     else:
#         lst.append(string)
#         return True, lst
#
# user_list = []
# user_in_bool = False
# s = 1
# li = ["apple0","apple1","apple0"]
# for i in li:
#     user_in_bool, user_list = duplicates_and_add(user_list, i)
#     if user_in_bool or s == 1:
#         print(user_in_bool, user_list)
# print(user_in_bool, user_list)

# import webview
#
# def main():
#     webview.create_window('---', "https://www.baidu.com/", height=650, width=760,
#                                    confirm_close=True)
#     chinese = {
#         'global.quitConfirmation': '确定关闭?',
#     }
#
#     webview.start(localization=chinese)
# if __name__ == "__main__":
#     main()

# import requests
# import random
# import os
#
# admin = "272275"
# data = requests.get("https://th.ry188.vip/API/GetData.aspx?Account=" + admin, timeout=30).json()
# def GetHtmluser():
#     UserLists = []
#     getuser_num = 10
#     for i in range(len(data["UserInFIdList"])):
#         UserRequests = requests.get(
#             "https://th.ry188.vip/API/GetUserList.aspx?Count=" + str(getuser_num) + "&Id=" + str(
#                 data["UserInFIdList"][i]["Id"]), timeout=30).json()
#         for k in range(len(UserRequests["UserList"])):
#             UserLists.append(UserRequests["UserList"][k]["name"])
#     return UserLists
#
# def GetHtmlpic():
#     # 创建img文件夹（如果不存在）
#     if not os.path.exists('img'):
#         os.makedirs('img')
#     if len(data["SendData"]["ConfigDatas"]["SendPicList"]) > 0:
#         random_test = random.randint(0, len(data["SendData"]["ConfigDatas"]["SendPicList"]) - 1)
#         print(data["SendData"]["ConfigDatas"]["SendPicList"][random_test])
#         # 下载图片
#         htmlpic = requests.get(data["SendData"]["ConfigDatas"]["SendPicList"][random_test], timeout=30)
#         # 图片保存路径
#         img_path = os.path.join('img', 'img.jpg')
#         # 保存图片
#         with open(img_path, 'wb') as file:
#             file.write(htmlpic.content)
#
#         # 返回图片的绝对路径
#         return os.path.abspath(img_path)
#
# # 调用函数并获取图片路径
# image_path = GetHtmlpic()
# print(f"图片已保存到：{image_path}")
# message_pic = True
# if message_pic and image_path is not None :
#     print(222)

import aiohttp
import asyncio
import json
import os


async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=30) as response:
            return await response.json()


async def GetHtmluser(data, messags_types, messags_types2):
    # 计算需要的总用户数
    total_needed = int(data["SendData"]["SendConfigs"]["FriendCount2"]) - int(
        data["SendData"]["SendConfigs"]["FriendCount"]) + 1

    # 计算需要跳过的用户数（起始点之前的用户）
    skip_count = int(data["SendData"]["SendConfigs"]["FriendCount"]) - 1

    print(f"需要获取 {total_needed} 个用户 (跳过前 {skip_count} 个)")

    UserLists = []
    global_skipped = 0  # 全局已跳过计数器
    global_collected = 0  # 全局已收集计数器

    # 遍历所有ID源（群组/页面/支持列表）
    for i in range(len(data[messags_types2])):
        current_id = data[messags_types2][i]['Id']
        pages = 1
        print(f"\n开始处理 ID源 {i + 1}/{len(data[messags_types2])}: {current_id}")
        print(f"全局状态: 已跳过 {global_skipped}/{skip_count}, 已收集 {global_collected}/{total_needed}")

        # 当还需要获取用户时继续请求
        while global_collected < total_needed:
            # 计算当前页需要跳过的用户数
            page_skip = 0
            if global_skipped < skip_count:
                page_skip = min(10, skip_count - global_skipped)

            url = f"https://cj.ry188.vip/api/GetUserDatanew.aspx?T={messags_types}&P={pages}&Z=10&Id={current_id}"
            print(f"正在请求: {url} (跳过本页前 {page_skip} 个用户)")

            try:
                response = await fetch_data(url)

                # 检查是否返回有效用户列表
                if "UserList" not in response or not response["UserList"]:
                    print(f"ID {current_id} 第{pages}页无数据")
                    break

                # 更新全局跳过计数
                global_skipped += page_skip

                # 获取当前页用户列表（跳过指定数量的用户）
                users_in_page = response["UserList"][page_skip:]

                # 添加本页所有用户ID
                for user in users_in_page:
                    if global_collected < total_needed:
                        UserLists.append(user["userid"])
                        global_collected += 1
                    else:
                        break

                # 检查是否已获取足够用户
                if global_collected >= total_needed:
                    print(f"已达目标人数 {total_needed}，停止请求")
                    break

                # 检查是否最后一页（不足10人）
                if len(response["UserList"]) < 10:
                    print(f"ID {current_id} 最后一页数据不足10条")
                    break

                pages += 1

            except Exception as e:
                print(f"请求异常: {e}")
                break

        # 检查是否已满足总人数要求
        if global_collected >= total_needed:
            break

    print(f"实际获取 {len(UserLists)} 个用户 (跳过 {global_skipped} 个)")
    return UserLists


# 以下函数保持不变（parse_bool, save_progress, load_progress, clear_progress, main）
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


def load_progress(account):
    """从文件加载处理进度"""
    filename = f"{account}_progress.json"
    if not os.path.exists(filename):
        print(f"无进度文件 {filename}")
        return None, 0

    try:
        with open(filename, 'r') as f:
            progress_data = json.load(f)
        print(f"从 {filename} 加载进度: 位置 {progress_data['position']}/{len(progress_data['users'])}")
        return progress_data["users"], progress_data["position"]
    except:
        print(f"加载进度文件 {filename} 失败")
        return None, 0


def clear_progress(account):
    """清除进度文件"""
    filename = f"{account}_progress.json"
    if os.path.exists(filename):
        os.remove(filename)
        print(f"已清除进度文件 {filename}")


async def main():
    content1 = "272275"
    data = await fetch_data(f"https://cj.ry188.vip/API/GetData.aspx?Account={content1}")

    # 检查是否继续上一次
    continue_last = parse_bool(data["SendData"]["SendConfigs"]["IsResetProgress"])
    print(f"继续上一次: {continue_last}")

    users = []
    start_position = 0

    if continue_last:
        # 尝试加载进度
        users, start_position = load_progress(content1)

    # 如果没有加载到进度或不需要继续，重新获取用户列表
    if not users:
        # 确定请求类型
        if parse_bool(data["SendData"]["SendConfigs"]["IsGroup"]):
            messags_types = "G"
            messags_types2 = "GroupIdList"
        elif parse_bool(data["SendData"]["SendConfigs"]["IsPages"]):
            messags_types = "P"
            messags_types2 = "PagesIdList"
        else:
            messags_types = "S"
            messags_types2 = "SupportIdList"

        print(f"请求类型: {messags_types}, 数据源: {messags_types2}")

        # 获取用户列表
        users = await GetHtmluser(data, messags_types, messags_types2)
        print(f"共获取 {len(users)} 个用户ID")

    # 处理用户列表（从保存的位置开始）
    print(f"从位置 {start_position} 开始处理")
    for i in range(start_position, len(users)):
        user_id = users[i]
        print(f"处理用户 {i + 1}/{len(users)}: {user_id}")

        # 模拟处理工作
        # await your_processing_function(user_id)

        # 更新进度
        current_position = i + 1
        save_progress(content1, users, current_position)

        # 每处理一个用户等待3秒
        # await asyncio.sleep(3)
    # 处理完成后清除进度
    clear_progress(content1)
    print("所有用户处理完成!")


if __name__ == "__main__":
    asyncio.run(main())