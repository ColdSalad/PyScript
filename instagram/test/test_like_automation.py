#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram点赞自动化测试脚本
"""

import sys
import os

# 添加method目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'method'))

try:
    from method.instagram_like_automation import InstagramLikeAutomation, auto_login_and_like
    print("✅ 成功导入Instagram点赞自动化模块")
except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    print("请确保已安装selenium和相关依赖")
    sys.exit(1)

def test_like_automation():
    """测试点赞自动化功能"""
    print("=== Instagram点赞自动化测试 ===")
    
    # 获取用户输入
    print("\n请输入测试信息:")
    username = input("用户名: ").strip()
    password = input("密码: ").strip()
    
    if not username or not password:
        print("❌ 用户名和密码不能为空")
        return
    
    # 设置测试参数
    target_url = "https://www.instagram.com/?next=%2F"
    max_likes = 3  # 测试时使用较小的数值
    
    print(f"\n测试参数:")
    print(f"- 用户名: {username}")
    print(f"- 目标地址: {target_url}")
    print(f"- 最大点赞数: {max_likes}")
    
    # 确认开始测试
    confirm = input("\n确认开始测试? (y/n): ").strip().lower()
    if confirm != 'y':
        print("测试已取消")
        return
    
    # 执行测试
    print("\n开始执行测试...")
    success, message = auto_login_and_like(username, password, target_url, max_likes)
    
    # 显示结果
    if success:
        print(f"\n✅ 测试成功: {message}")
        print("请查看浏览器窗口确认操作结果")
    else:
        print(f"\n❌ 测试失败: {message}")
    
    # 等待用户确认
    input("\n按回车键结束测试...")

if __name__ == "__main__":
    try:
        test_like_automation()
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}") 