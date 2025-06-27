#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram登录GUI打包脚本
使用PyInstaller将程序打包成单个exe文件
"""

import os
import sys
import subprocess
import shutil

def install_requirements():
    """安装打包所需的依赖"""
    print("正在安装打包依赖...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("PyInstaller安装成功!")
    except subprocess.CalledProcessError:
        print("PyInstaller安装失败，请手动安装: pip install pyinstaller")
        return False
    return True

def create_spec_file():
    """创建PyInstaller规格文件以优化打包"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['ui/instagramLogin.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib', 'numpy', 'scipy', 'pandas', 'jupyter', 'IPython',
        'sphinx', 'pytest', 'setuptools', 'distutils', 'email',
        'xml', 'urllib3', 'certifi', 'charset_normalizer', 'idna',
        'requests', 'PIL.ImageShow', 'PIL.ImageQt', 'PIL.ImageTk'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 移除不需要的模块以减小体积
a.binaries = [x for x in a.binaries if not x[0].startswith('api-ms-win')]
a.binaries = [x for x in a.binaries if not x[0].startswith('ucrtbase')]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='InstagramLogin',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''
    
    with open('instagram_login.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content.strip())
    print("已创建优化的spec文件")

def optimize_source():
    """优化源代码以减小打包体积"""
    print("正在优化源代码...")
    
    # 创建优化版本的登录程序
    optimized_content = '''import tkinter as tk
from tkinter import messagebox

class InstagramLoginGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram 登录")
        self.root.geometry("380x500")
        self.root.configure(bg='#fafafa')
        self.root.resizable(False, False)
        
        # 移除默认标题栏
        self.root.overrideredirect(True)
        
        # 居中显示窗口
        self.center_window()
        
        # 创建自定义标题栏
        self.create_custom_titlebar()
        
        # 创建主框架
        self.main_frame = tk.Frame(root, bg='#fafafa')
        self.main_frame.pack(expand=True, fill='both', padx=30, pady=20)
        
        self.create_widgets()
        self.bind_drag_events()
        
    def create_custom_titlebar(self):
        """创建自定义标题栏"""
        self.titlebar = tk.Frame(self.root, bg='#ffffff', height=40, relief='flat')
        self.titlebar.pack(fill='x', side='top')
        self.titlebar.pack_propagate(False)
        
        # 标题文本
        title_label = tk.Label(self.titlebar, text="Instagram 登录", 
                              font=('Microsoft YaHei', 11, 'bold'), 
                              fg='#262626', bg='#ffffff')
        title_label.pack(side='left', padx=15, pady=10)
        
        # 窗口控制按钮
        controls_frame = tk.Frame(self.titlebar, bg='#ffffff')
        controls_frame.pack(side='right', padx=10, pady=8)
        
        minimize_btn = tk.Button(controls_frame, text="─", 
                               font=('Arial', 8), fg='#666666', bg='#ffffff',
                               relief='flat', bd=0, cursor='hand2',
                               command=self.minimize_window)
        minimize_btn.pack(side='left', padx=2)
        
        close_btn = tk.Button(controls_frame, text="✕", 
                            font=('Arial', 10), fg='#666666', bg='#ffffff',
                            relief='flat', bd=0, cursor='hand2',
                            command=self.close_window)
        close_btn.pack(side='left', padx=2)
        
        # 按钮悬停效果
        minimize_btn.bind('<Enter>', lambda e: minimize_btn.configure(bg='#e1e1e1'))
        minimize_btn.bind('<Leave>', lambda e: minimize_btn.configure(bg='#ffffff'))
        close_btn.bind('<Enter>', lambda e: close_btn.configure(bg='#ff4757', fg='white'))
        close_btn.bind('<Leave>', lambda e: close_btn.configure(bg='#ffffff', fg='#666666'))
        
    def bind_drag_events(self):
        """绑定窗口拖拽事件"""
        self.titlebar.bind('<Button-1>', self.start_drag)
        self.titlebar.bind('<B1-Motion>', self.on_drag)
        
    def start_drag(self, event):
        self.x = event.x
        self.y = event.y
        
    def on_drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
        
    def minimize_window(self):
        self.root.iconify()
        
    def close_window(self):
        self.root.quit()

    def center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """创建所有UI组件"""
        # Instagram Logo
        logo_frame = tk.Frame(self.main_frame, bg='#fafafa')
        logo_frame.pack(pady=(30, 40))
        
        logo_label = tk.Label(logo_frame, text="Instagram", 
                             font=('Arial', 32, 'italic'), 
                             fg='#E1306C', bg='#fafafa')
        logo_label.pack()
        
        # 装饰线
        decoration_frame = tk.Frame(logo_frame, bg='#fafafa', height=3)
        decoration_frame.pack(fill='x', padx=60, pady=(15, 0))
        
        decoration_line = tk.Frame(decoration_frame, bg='#E1306C', height=2)
        decoration_line.pack(fill='x')
        
        # 输入框区域
        input_area = tk.Frame(self.main_frame, bg='#fafafa')
        input_area.pack(fill='x', pady=(20, 0))
        
        # 用户名输入框
        self.create_input_field(input_area, "用户名", 'username')
        
        # 密码输入框
        self.create_input_field(input_area, "密码", 'password', show='*')
        
        # 登录按钮
        self.login_btn = tk.Button(input_area,
                                  text="登录",
                                  font=('Microsoft YaHei', 12, 'bold'),
                                  bg='#0095f6',
                                  fg='white',
                                  relief='flat',
                                  cursor='hand2',
                                  bd=0,
                                  command=self.login,
                                  highlightthickness=0)
        self.login_btn.pack(pady=(30, 20), fill='x', ipady=15)
        
        # 登录按钮悬停效果
        self.login_btn.bind('<Enter>', lambda e: self.login_btn.configure(bg='#1877f2'))
        self.login_btn.bind('<Leave>', lambda e: self.login_btn.configure(bg='#0095f6'))
        
        # 忘记密码链接
        forgot_password = tk.Label(input_area,
                                 text="忘记密码？",
                                 font=('Microsoft YaHei', 10, 'underline'),
                                 fg='#00376b',
                                 bg='#fafafa',
                                 cursor='hand2')
        forgot_password.pack(pady=(15, 0))
        forgot_password.bind("<Button-1>", self.forgot_password)
        
        # 底部信息
        bottom_frame = tk.Frame(self.main_frame, bg='#fafafa')
        bottom_frame.pack(side='bottom', fill='x', pady=(30, 10))
        
        info_text = tk.Label(bottom_frame, text="简洁 • 安全 • 快速", 
                            font=('Microsoft YaHei', 9), 
                            fg='#8e8e8e', bg='#fafafa')
        info_text.pack()

    def create_input_field(self, parent, placeholder, field_name, show=None):
        """创建输入框"""
        input_frame = tk.Frame(parent, bg='#fafafa')
        input_frame.pack(pady=(0, 15), fill='x')
        
        entry = tk.Entry(input_frame,
                        font=('Microsoft YaHei', 12),
                        bg='#ffffff',
                        fg='#262626',
                        relief='flat',
                        bd=0,
                        show=show)
        entry.pack(fill='x', ipady=15, ipadx=15)
        entry.configure(highlightbackground='#dbdbdb', highlightthickness=1,
                       highlightcolor='#0095f6')
        
        # 占位符效果
        entry.insert(0, placeholder)
        entry.configure(fg='#8e8e8e')
        
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.configure(fg='#262626')
            entry.configure(highlightbackground='#0095f6', highlightthickness=2)
                
        def on_focus_out(event):
            if entry.get() == '':
                entry.insert(0, placeholder)
                entry.configure(fg='#8e8e8e')
            entry.configure(highlightbackground='#dbdbdb', highlightthickness=1)
                
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        setattr(self, f'{field_name}_entry', entry)
        
    def get_input_value(self, field_name):
        """获取输入框的值"""
        entry = getattr(self, f'{field_name}_entry')
        value = entry.get()
        placeholder_map = {'username': '用户名', 'password': '密码'}
        if value == placeholder_map.get(field_name, ''):
            return ''
        return value
        
    def login(self):
        """登录处理"""
        username = self.get_input_value('username')
        password = self.get_input_value('password')
        
        if not username or not password:
            messagebox.showerror("错误", "请输入用户名和密码")
            return
            
        messagebox.showinfo("登录成功", f"欢迎回来，{username}！")
        
    def forgot_password(self, event):
        """忘记密码处理"""
        messagebox.showinfo("忘记密码", "请联系管理员重置密码")

def main():
    root = tk.Tk()
    app = InstagramLoginGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
'''
    
    # 创建优化版本文件
    os.makedirs('optimized', exist_ok=True)
    with open('optimized/instagram_login_optimized.py', 'w', encoding='utf-8') as f:
        f.write(optimized_content)
    print("已创建优化版本的源代码")

def build_exe():
    """执行打包"""
    print("开始打包exe文件...")
    
    try:
        # 使用优化的源文件进行打包
        cmd = [
            'pyinstaller',
            '--onefile',                    # 打包成单个文件
            '--windowed',                   # 无控制台窗口
            '--optimize=2',                 # 优化级别
            '--strip',                      # 去除调试信息
            '--clean',                      # 清理临时文件
            '--distpath=dist',              # 输出目录
            '--workpath=build',             # 工作目录
            '--specpath=.',                 # spec文件目录
            '--name=InstagramLogin',        # exe文件名
            '--exclude-module=PIL',         # 排除PIL模块
            '--exclude-module=requests',    # 排除requests模块
            '--exclude-module=urllib3',     # 排除urllib3模块
            'optimized/instagram_login_optimized.py'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("✅ 打包成功!")
            print(f"exe文件位置: dist/InstagramLogin.exe")
            
            # 显示文件大小
            exe_path = "dist/InstagramLogin.exe"
            if os.path.exists(exe_path):
                size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
                print(f"文件大小: {size:.2f} MB")
        else:
            print("❌ 打包失败:")
            print(result.stderr)
            
    except FileNotFoundError:
        print("❌ PyInstaller未找到，请先安装: pip install pyinstaller")
    except Exception as e:
        print(f"❌ 打包过程中出现错误: {e}")

def cleanup():
    """清理临时文件"""
    print("清理临时文件...")
    dirs_to_remove = ['build', '__pycache__', 'optimized']
    files_to_remove = ['InstagramLogin.spec']
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
    
    print("清理完成")

def main():
    print("=== Instagram登录GUI打包工具 ===")
    print("正在准备打包环境...")
    
    # 检查并安装依赖
    if not install_requirements():
        return
    
    # 优化源代码
    optimize_source()
    
    # 执行打包
    build_exe()
    
    # 清理临时文件
    cleanup()
    
    print("\n=== 打包完成 ===")
    print("请查看 dist/ 目录中的 InstagramLogin.exe 文件")

if __name__ == "__main__":
    main() 