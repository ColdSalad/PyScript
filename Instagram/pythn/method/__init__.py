#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Method模块包
包含Instagram登录GUI的各种功能模块
"""

from src.main.pythn.method.browser_manager import BrowserManager, open_instagram, open_url, get_available_browsers

# 尝试导入网页自动化模块
try:
    from src.main.pythn.method.web_automation import InstagramWebAutomation, auto_login_instagram
    SELENIUM_AVAILABLE = True
    __all__ = [
        'BrowserManager',
        'open_instagram',
        'open_url',
        'get_available_browsers',
        'InstagramWebAutomation',
        'auto_login_instagram'
    ]
except ImportError:
    SELENIUM_AVAILABLE = False
    __all__ = [
        'BrowserManager',
        'open_instagram',
        'open_url',
        'get_available_browsers'
    ]

__version__ = "1.0.0"
__author__ = "Instagram Login GUI"
