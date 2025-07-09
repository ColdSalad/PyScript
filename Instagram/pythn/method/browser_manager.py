#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器管理模块
提供智能打开浏览器的功能，优先Edge，然后Chrome
"""

import os
import subprocess
import webbrowser
from tkinter import messagebox


class BrowserManager:
    """浏览器管理类"""
    
    def __init__(self):
        """初始化浏览器管理器"""
        self.edge_paths = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\Application\msedge.exe")
        ]
        
        self.chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
        ]
    
    def find_edge_browser(self):
        """查找Edge浏览器路径"""
        for edge_path in self.edge_paths:
            if os.path.exists(edge_path):
                return edge_path
        return None
    
    def find_chrome_browser(self):
        """查找Chrome浏览器路径"""
        for chrome_path in self.chrome_paths:
            if os.path.exists(chrome_path):
                return chrome_path
        return None
    
    def open_edge(self, url="https://www.instagram.com"):
        """打开Edge浏览器"""
        try:
            edge_path = self.find_edge_browser()
            if edge_path:
                subprocess.Popen([edge_path, url])
                print("✅ 成功打开Microsoft Edge浏览器")
                return True
            else:
                print("❌ 未找到Microsoft Edge浏览器")
                return False
        except Exception as e:
            print(f"❌ Edge启动失败: {e}")
            return False
    
    def open_chrome(self, url="https://www.instagram.com"):
        """打开Chrome浏览器"""
        try:
            chrome_path = self.find_chrome_browser()
            if chrome_path:
                subprocess.Popen([chrome_path, url])
                print("✅ 成功打开Google Chrome浏览器")
                return True
            else:
                print("❌ 未找到Google Chrome浏览器")
                return False
        except Exception as e:
            print(f"❌ Chrome启动失败: {e}")
            return False
    
    def open_default_browser(self, url="https://www.instagram.com"):
        """打开系统默认浏览器"""
        try:
            webbrowser.open(url)
            print("✅ 使用系统默认浏览器打开")
            return True
        except Exception as e:
            print(f"❌ 默认浏览器启动失败: {e}")
            return False
    
    def open_browser_smart(self, url="https://www.instagram.com", show_messages=True):
        """智能打开浏览器 - 优先Edge，然后Chrome，最后默认浏览器"""
        success = False
        browser_used = ""
        
        # 方法1：尝试打开Edge浏览器
        if self.open_edge(url):
            success = True
            browser_used = "Microsoft Edge"
        
        # 方法2：如果Edge失败，尝试Chrome
        elif self.open_chrome(url):
            success = True
            browser_used = "Google Chrome"
        
        # 方法3：使用系统默认浏览器
        elif self.open_default_browser(url):
            success = True
            browser_used = "默认浏览器"
        
        # 处理结果
        if success:
            if show_messages:
                print(f"✅ 已使用{browser_used}打开: {url}")
            return True, browser_used
        else:
            if show_messages:
                messagebox.showwarning("提示", f"无法自动打开浏览器\n请手动访问: {url}")
            return False, None
    
    def get_available_browsers(self):
        """获取可用的浏览器列表"""
        available_browsers = []
        
        if self.find_edge_browser():
            available_browsers.append("Microsoft Edge")
        
        if self.find_chrome_browser():
            available_browsers.append("Google Chrome")
        
        # 默认浏览器总是可用的
        available_browsers.append("系统默认浏览器")
        
        return available_browsers
    
    def open_instagram(self, show_messages=True):
        """专门用于打开Instagram的方法"""
        return self.open_browser_smart("https://www.instagram.com", show_messages)
    
    def open_url(self, url, show_messages=True):
        """打开指定URL"""
        return self.open_browser_smart(url, show_messages)


# 便捷函数
def open_instagram():
    """便捷函数：打开Instagram"""
    browser_manager = BrowserManager()
    return browser_manager.open_instagram()

def open_url(url):
    """便捷函数：打开指定URL"""
    browser_manager = BrowserManager()
    return browser_manager.open_url(url)

def get_available_browsers():
    """便捷函数：获取可用浏览器列表"""
    browser_manager = BrowserManager()
    return browser_manager.get_available_browsers()


if __name__ == "__main__":
    # 测试代码
    print("=== 浏览器管理器测试 ===")
    
    manager = BrowserManager()
    
    print("可用浏览器:")
    for browser in manager.get_available_browsers():
        print(f"  - {browser}")
    
    print("\n正在测试打开Instagram...")
    success, browser_used = manager.open_instagram()
    
    if success:
        print(f"测试成功！使用了: {browser_used}")
    else:
        print("测试失败！") 