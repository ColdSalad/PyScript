#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试自动登录功能
"""

import sys
import os

# 添加method目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'method'))

try:
    from web_automation import InstagramWebAutomation
    print("✅ 成功导入web_automation模块")
    
    # 测试自动化对象创建
    automation = InstagramWebAutomation()
    print("✅ 成功创建InstagramWebAutomation对象")
    
    # 测试浏览器驱动设置
    if automation.setup_driver():
        print("✅ 浏览器驱动设置成功")
        
        # 测试打开Instagram
        if automation.open_instagram():
            print("✅ 成功打开Instagram页面")
            
            # 测试等待登录表单
            if automation.wait_for_login_form():
                print("✅ 登录表单加载成功")
                print("🎯 所有基础功能测试通过！")
            else:
                print("❌ 登录表单加载失败")
        else:
            print("❌ 打开Instagram页面失败")
    else:
        print("❌ 浏览器驱动设置失败")
        
except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    print("请确保已安装selenium: pip install selenium")
except Exception as e:
    print(f"❌ 测试过程中出错: {e}")

print("\n=== 测试完成 ===") 