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
