#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram评论自动化测试脚本
"""

import sys
import os

# 添加method目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'method'))

from instagram_comment_automation import InstagramCommentAutomation

def test_comment_automation():
    """测试评论自动化功能"""
    print("=== Instagram 评论自动化测试 ===")
    
    # 创建评论自动化实例
    comment_automation = InstagramCommentAutomation()
    
    try:
        # 测试基本功能
        print("✅ 评论自动化模块导入成功")
        print("✅ 实例创建成功")
        
        # 显示可用方法
        print("\n📋 可用方法:")
        methods = [method for method in dir(comment_automation) if not method.startswith('_')]
        for method in methods:
            print(f"   - {method}")
        
        print("\n🎉 评论自动化模块测试完成！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    finally:
        # 清理资源
        comment_automation.close_browser()

if __name__ == "__main__":
    test_comment_automation()