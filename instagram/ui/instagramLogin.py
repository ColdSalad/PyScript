import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw
import requests
from io import BytesIO
import math
import webbrowser
import subprocess
import os
import sys
import threading

# 添加method目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'method'))
from browser_manager import BrowserManager

# 尝试导入网页自动化模块
try:
    from web_automation import InstagramWebAutomation
    print("✅ 网页自动化模块导入成功")
    WEB_AUTOMATION_AVAILABLE = True
except ImportError:
    print("⚠️ 网页自动化模块不可用")
    WEB_AUTOMATION_AVAILABLE = False

# 尝试导入点赞自动化模块
try:
    from instagram_like_automation import InstagramLikeAutomation
    print("✅ 点赞自动化模块导入成功")
    LIKE_AUTOMATION_AVAILABLE = True
except ImportError:
    print("⚠️ 点赞自动化模块不可用")
    LIKE_AUTOMATION_AVAILABLE = False

# 检查Selenium是否完全可用
SELENIUM_AVAILABLE = WEB_AUTOMATION_AVAILABLE and LIKE_AUTOMATION_AVAILABLE

if SELENIUM_AVAILABLE:
    print("✅ Selenium模块完全可用，支持自动填充和点赞功能")
else:
    print("❌ Selenium功能受限，仅支持普通浏览器打开")

class InstagramLoginGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram 登录")
        self.root.geometry("380x500")
        self.root.configure(bg='#fafafa')
        self.root.resizable(False, False)

        # 移除默认标题栏
        self.root.overrideredirect(True)

        # 设置窗口透明度和圆角效果
        self.setup_window_style()

        # 居中显示窗口
        self.center_window()

        # 创建自定义标题栏
        self.create_custom_titlebar()

        # 创建主框架 - 移除边框
        self.main_frame = tk.Frame(root, bg='#fafafa')
        self.main_frame.pack(expand=True, fill='both')

        # 创建登录表单容器 - 移除边框
        self.login_container = tk.Frame(self.main_frame, bg='#fafafa')
        self.login_container.pack(expand=True, fill='both', padx=30, pady=20)

        # 初始化浏览器管理器
        self.browser_manager = BrowserManager()

        # 初始化网页自动化实例（保持引用防止被垃圾回收）
        self.web_automation = None
        self.like_automation = None

        self.create_widgets()

        # 绑定窗口拖拽事件
        self.bind_drag_events()

    def setup_window_style(self):
        """设置窗口样式"""
        try:
            # 设置窗口属性
            self.root.attributes('-alpha', 0.98)  # 轻微透明度
            # 在Windows上设置窗口层级
            self.root.attributes('-topmost', False)
        except:
            pass

    def create_custom_titlebar(self):
        """创建自定义标题栏"""
        # 标题栏框架
        self.titlebar = tk.Frame(self.root, bg='#ffffff', height=40, relief='flat')
        self.titlebar.pack(fill='x', side='top')
        self.titlebar.pack_propagate(False)

        # 添加标题栏渐变效果
        self.add_titlebar_gradient()

        # 标题文本
        title_label = tk.Label(self.titlebar, text="Instagram 登录",
                              font=('Microsoft YaHei', 11, 'bold'),
                              fg='#262626', bg='#ffffff')
        title_label.pack(side='left', padx=15, pady=10)

        # 窗口控制按钮框架
        controls_frame = tk.Frame(self.titlebar, bg='#ffffff')
        controls_frame.pack(side='right', padx=10, pady=8)

        # 最小化按钮
        minimize_btn = tk.Button(controls_frame, text="─",
                               font=('Arial', 8), fg='#666666', bg='#ffffff',
                               relief='flat', bd=0, cursor='hand2',
                               command=self.minimize_window)
        minimize_btn.pack(side='left', padx=2)

        # 关闭按钮
        close_btn = tk.Button(controls_frame, text="✕",
                            font=('Arial', 10), fg='#666666', bg='#ffffff',
                            relief='flat', bd=0, cursor='hand2',
                            command=self.close_window)
        close_btn.pack(side='left', padx=2)

        # 按钮悬停效果
        self.add_button_hover_effects(minimize_btn, close_btn)

    def add_titlebar_gradient(self):
        """为标题栏添加渐变效果"""
        try:
            # 创建渐变背景
            gradient_frame = tk.Frame(self.titlebar, bg='#f8f9fa', height=2)
            gradient_frame.pack(fill='x', side='bottom')
        except:
            pass

    def add_button_hover_effects(self, minimize_btn, close_btn):
        """添加按钮悬停效果"""
        def on_minimize_enter(e):
            minimize_btn.configure(bg='#e1e1e1')

        def on_minimize_leave(e):
            minimize_btn.configure(bg='#ffffff')

        def on_close_enter(e):
            close_btn.configure(bg='#ff4757', fg='white')

        def on_close_leave(e):
            close_btn.configure(bg='#ffffff', fg='#666666')

        minimize_btn.bind('<Enter>', on_minimize_enter)
        minimize_btn.bind('<Leave>', on_minimize_leave)
        close_btn.bind('<Enter>', on_close_enter)
        close_btn.bind('<Leave>', on_close_leave)

    def bind_drag_events(self):
        """绑定窗口拖拽事件"""
        self.titlebar.bind('<Button-1>', self.start_drag)
        self.titlebar.bind('<B1-Motion>', self.on_drag)

        # 为标题标签也绑定拖拽事件
        for widget in self.titlebar.winfo_children():
            if isinstance(widget, tk.Label):
                widget.bind('<Button-1>', self.start_drag)
                widget.bind('<B1-Motion>', self.on_drag)

    def start_drag(self, event):
        """开始拖拽"""
        self.x = event.x
        self.y = event.y

    def on_drag(self, event):
        """拖拽过程中"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def minimize_window(self):
        """最小化窗口"""
        self.root.iconify()

    def close_window(self):
        """关闭窗口"""
        self.cleanup()
        self.root.quit()

    def cleanup(self):
        """清理资源"""
        try:
            # 清理普通自动化实例
            if self.web_automation and hasattr(self.web_automation, 'driver') and self.web_automation.driver:
                print("正在关闭浏览器...")
                self.web_automation.close_browser()
            
            # 清理点赞自动化实例
            if self.like_automation and hasattr(self.like_automation, 'driver') and self.like_automation.driver:
                print("正在关闭点赞自动化浏览器...")
                self.like_automation.close_browser()
        except Exception as e:
            print(f"清理资源时出错: {e}")

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
        logo_frame = tk.Frame(self.login_container, bg='#fafafa')
        logo_frame.pack(pady=(30, 40))

        logo_label = tk.Label(logo_frame, text="Instagram",
                             font=('Brush Script MT', 42, 'italic'),
                             fg='#E1306C', bg='#fafafa')
        logo_label.pack()

        # 添加Logo下方的装饰线
        decoration_frame = tk.Frame(logo_frame, bg='#fafafa', height=3)
        decoration_frame.pack(fill='x', padx=60, pady=(15, 0))

        decoration_line = tk.Frame(decoration_frame, bg='#E1306C', height=2)
        decoration_line.pack(fill='x')

        # 输入框区域
        input_area = tk.Frame(self.login_container, bg='#fafafa')
        input_area.pack(fill='x', pady=(20, 0))

        # 用户名输入框
        self.create_enhanced_input_field(input_area, "用户名", 'username')

        # 密码输入框
        self.create_enhanced_input_field(input_area, "密码", 'password', show='*')

        # 登录按钮 - 使用Canvas创建圆角按钮
        self.create_rounded_login_button(input_area)

        # 底部信息
        bottom_frame = tk.Frame(self.login_container, bg='#fafafa')
        bottom_frame.pack(side='bottom', fill='x', pady=(30, 10))

        info_text = tk.Label(bottom_frame, text="自动登录 • 智能点赞 • 安全快速",
                            font=('Microsoft YaHei', 9),
                            fg='#8e8e8e', bg='#fafafa')
        info_text.pack()

        # 添加调试按钮
        debug_frame = tk.Frame(bottom_frame, bg='#fafafa')
        debug_frame.pack(pady=(15, 0))

        debug_btn = tk.Button(debug_frame,
                             text="JavaScript选择器调试",
                             font=('Microsoft YaHei', 9),
                             bg='#f0f0f0',
                             fg='#666666',
                             relief='flat',
                             cursor='hand2',
                             bd=0,
                             command=self.launch_js_debugger,
                             highlightthickness=0)
        debug_btn.pack(pady=5, padx=20, fill='x')

        # 添加调试按钮悬停效果
        def on_debug_enter(e):
            debug_btn.configure(bg='#e0e0e0')

        def on_debug_leave(e):
            debug_btn.configure(bg='#f0f0f0')

        debug_btn.bind('<Enter>', on_debug_enter)
        debug_btn.bind('<Leave>', on_debug_leave)

    def create_enhanced_input_field(self, parent, placeholder, field_name, show=None):
        """创建增强的输入框"""
        # 输入框容器
        input_frame = tk.Frame(parent, bg='#fafafa')
        input_frame.pack(pady=(0, 15), fill='x')

        # 输入框
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

        # 存储引用
        setattr(self, f'{field_name}_entry', entry)

    def add_login_button_effects(self):
        """添加登录按钮悬停效果"""
        def on_enter(e):
            self.login_btn.configure(bg='#1877f2')

        def on_leave(e):
            self.login_btn.configure(bg='#0095f6')

        self.login_btn.bind('<Enter>', on_enter)
        self.login_btn.bind('<Leave>', on_leave)

    def create_rounded_button(self, button, radius):
        """创建圆角按钮效果"""
        try:
            button.configure(
                relief='flat',
                bd=0,
                highlightthickness=0,
                borderwidth=0,
                padx=10,
                pady=8
            )
        except Exception as e:
            pass

    def get_input_value(self, field_name):
        """获取输入框的值"""
        entry = getattr(self, f'{field_name}_entry')
        value = entry.get()
        placeholder_map = {
            'username': '用户名、邮箱或手机号',
            'password': '密码'
        }
        if value == placeholder_map.get(field_name, ''):
            return ''
        return value

    def create_rounded_login_button(self, parent):
        """创建登录按钮"""
        # 登录按钮
        self.login_btn = tk.Button(parent,
                                  text="登录",
                                  font=('Microsoft YaHei', 12, 'bold'),
                                  bg='#0095f6',
                                  fg='white',
                                  relief='flat',
                                  cursor='hand2',
                                  bd=0,
                                  command=self.login,
                                  highlightthickness=0)
        self.login_btn.pack(pady=(20, 15), fill='x', ipady=15)

        # 添加登录按钮悬停效果
        self.add_login_button_effects()

    def login(self):
        """登录处理 - 优先使用点赞自动化模式"""
        username = self.get_input_value('username')
        password = self.get_input_value('password')

        if not username or not password:
            messagebox.showerror("错误", "请输入用户名和密码")
            return

        # 如果点赞自动化可用，优先使用点赞自动化模式
        if LIKE_AUTOMATION_AVAILABLE:
            print("🎯 使用点赞自动化模式")
            self.auto_login_and_like(username, password)
        elif WEB_AUTOMATION_AVAILABLE:
            print("🔧 使用网页自动化模式")
            self.auto_fill_login(username, password)
        else:
            print("🌐 使用普通浏览器模式")
            self.open_browser()

    def auto_fill_login(self, username, password):
        """自动填充登录信息"""
        try:
            # 更新登录按钮状态，显示处理中
            self.login_btn.configure(text="正在处理...", state='disabled')
            self.root.update()

            # 在后台线程中执行自动填充，避免界面卡死
            def auto_fill_thread():
                try:
                    # 使用类实例变量保持引用
                    self.web_automation = InstagramWebAutomation()
                    success, message = self.web_automation.auto_login_instagram(username, password)

                    # 在主线程中显示结果
                    self.root.after(0, lambda: self.show_auto_fill_result(success, message))

                except Exception as e:
                    error_msg = f"自动填充过程中出现错误: {e}"
                    self.root.after(0, lambda: self.show_auto_fill_result(False, error_msg))

            # 启动后台线程
            thread = threading.Thread(target=auto_fill_thread, daemon=True)
            thread.start()

        except Exception as e:
            # 恢复按钮状态
            self.login_btn.configure(text="登录", state='normal')
            messagebox.showerror("错误", f"启动自动填充失败: {e}")

    def auto_login_and_like(self, username, password):
        """自动登录并点赞"""
        try:
            # 使用默认设置
            max_likes = 10  # 默认点赞数量
            target_url = "https://www.instagram.com/?next=%2F"  # Instagram首页推荐页面
            
            # 更新登录按钮状态
            self.login_btn.configure(text="正在登录并点赞...", state='disabled')
            self.root.update()

            # 显示开始提示
            self.show_status_message("🚀 正在启动自动登录和点赞功能...", "info")

            # 在后台线程中执行登录并点赞
            def login_and_like_thread():
                try:
                    print(f"🔄 开始自动登录和点赞流程")
                    print(f"   用户名: {username}")
                    print(f"   目标URL: {target_url}")
                    print(f"   最大点赞数: {max_likes}")
                    
                    # 使用类实例变量保持引用
                    self.like_automation = InstagramLikeAutomation()
                    success, message = self.like_automation.login_and_like(
                        username, password, target_url, max_likes
                    )

                    # 在主线程中显示结果
                    self.root.after(0, lambda: self.show_like_automation_result(success, message))

                except Exception as e:
                    error_msg = f"登录并点赞过程中出现错误: {e}"
                    print(f"❌ {error_msg}")
                    self.root.after(0, lambda: self.show_like_automation_result(False, error_msg))

            # 启动后台线程
            thread = threading.Thread(target=login_and_like_thread, daemon=True)
            thread.start()

        except Exception as e:
            # 恢复按钮状态
            self.login_btn.configure(text="登录", state='normal')
            error_msg = f"启动登录并点赞失败: {e}"
            print(f"❌ {error_msg}")
            messagebox.showerror("错误", error_msg)

    def show_like_automation_result(self, success, message):
        """显示登录并点赞结果"""
        # 恢复登录按钮状态
        self.login_btn.configure(text="登录", state='normal')
        
        if success:
            # 成功时显示详细提示
            print(f"✅ 点赞自动化成功: {message}")
            self.show_status_message(f"🎉 {message}！浏览器将保持打开状态，您可以查看操作结果", "success")
            
            # 显示成功对话框
            messagebox.showinfo("自动点赞成功", 
                f"✅ 登录和点赞操作已完成！\n\n{message}\n\n浏览器将保持打开状态，您可以继续浏览或手动操作。")
        else:
            # 如果失败，显示错误信息并提供选择
            print(f"❌ 点赞自动化失败: {message}")
            self.show_status_message(f"⚠️ 自动化失败: {message}", "error")
            
            # 询问用户是否使用普通模式
            result = messagebox.askyesno("自动化失败", 
                f"❌ 自动登录和点赞失败:\n{message}\n\n是否使用普通浏览器模式打开Instagram？")
            
            if result:
                # 用户选择使用普通模式
                self.show_status_message("🔄 正在使用普通模式打开浏览器...", "info")
                self.root.after(1000, self.open_browser)
            else:
                # 用户选择不打开浏览器
                self.show_status_message("操作已取消", "info")

    def show_auto_fill_result(self, success, message):
        """显示自动填充结果"""
        # 恢复登录按钮状态
        self.login_btn.configure(text="登录", state='normal')
        
        if success:
            # 成功时显示简洁提示，不需要用户确认
            self.show_status_message("✅ 已自动填入登录信息并点击登录按钮，请查看浏览器登录结果", "success")
        else:
            # 如果自动填充失败，回退到普通模式
            self.show_status_message(f"⚠️ 自动填充失败: {message}，正在使用普通模式...", "warning")
            # 延迟一秒后打开普通浏览器
            self.root.after(1000, self.open_browser)

    def show_status_message(self, message, msg_type="info"):
        """显示状态消息（非阻塞）"""
        # 创建状态标签（如果不存在）
        if not hasattr(self, 'status_label'):
            self.status_label = tk.Label(
                self.login_container,
                font=('Microsoft YaHei', 9),
                bg='#fafafa',
                wraplength=320
            )
            self.status_label.pack(pady=(10, 0))
        
        # 根据消息类型设置颜色
        if msg_type == "success":
            color = "#28a745"  # 绿色
        elif msg_type == "warning":
            color = "#ffc107"  # 黄色
        elif msg_type == "error":
            color = "#dc3545"  # 红色
        else:
            color = "#6c757d"  # 灰色
        
        self.status_label.configure(text=message, fg=color)
        self.status_label.pack(pady=(10, 0))
        
        # 5秒后清除消息
        self.root.after(5000, lambda: self.clear_status_message())

    def clear_status_message(self):
        """清除状态消息"""
        if hasattr(self, 'status_label'):
            self.status_label.configure(text="")

    def open_browser(self):
        """使用浏览器管理器打开Instagram（普通模式）"""
        try:
            success, browser_used = self.browser_manager.open_instagram(show_messages=False)

            if success:
                # 显示成功消息
                message = f"登录信息已记录！\n已使用 {browser_used} 打开Instagram\n\n请在浏览器中手动输入登录信息。"
                messagebox.showinfo("浏览器已打开", message)
                print(f"✅ 浏览器打开成功: {browser_used}")
            else:
                # 如果自动打开失败，显示手动访问提示
                messagebox.showwarning("提示",
                    "登录信息已记录！\n\n无法自动打开浏览器\n请手动访问: https://www.instagram.com")
                print("❌ 所有浏览器打开方法都失败了")

        except Exception as e:
            print(f"❌ 浏览器管理器出错: {e}")
            messagebox.showerror("错误", f"打开浏览器时出现错误: {str(e)}")

    def get_available_browsers_info(self):
        """获取可用浏览器信息（调试用）"""
        try:
            browsers = self.browser_manager.get_available_browsers()
            print("可用浏览器:")
            for browser in browsers:
                print(f"  - {browser}")
            return browsers
        except Exception as e:
            print(f"获取浏览器信息失败: {e}")
            return []

    def launch_js_debugger(self):
        """启动JavaScript选择器调试器"""
        try:
            # 获取用户输入的登录信息
            username = self.get_input_value('username')
            password = self.get_input_value('password')

            if not username or not password:
                messagebox.showwarning("提示", "请先输入用户名和密码，调试器需要登录Instagram")
                return

            # 在后台线程中启动调试器
            def launch_debugger_thread():
                try:
                    # 导入JavaScript调试器
                    import sys
                    import os
                    test_dir = os.path.join(os.path.dirname(__file__), '..', 'test')
                    sys.path.append(test_dir)
                    
                    from JavaScript_debugger import InstagramJSDebugger
                    
                    # 创建调试器实例
                    debugger = InstagramJSDebugger()
                    
                    # 设置登录信息（避免重复输入）
                    debugger._username = username
                    debugger._password = password
                    
                    # 修改调试器的登录凭据获取方法
                    def get_cached_credentials():
                        return username, password
                    
                    debugger.get_login_credentials = get_cached_credentials
                    
                    # 启动调试器
                    debugger.run_debug()
                    
                except Exception as e:
                    error_msg = f"启动JavaScript调试器失败: {e}"
                    print(f"❌ {error_msg}")
                    # 在主线程中显示错误
                    self.root.after(0, lambda: messagebox.showerror("错误", error_msg))

            # 显示启动提示
            self.show_status_message("🔧 正在启动JavaScript选择器调试器...", "info")
            
            # 启动后台线程
            thread = threading.Thread(target=launch_debugger_thread, daemon=True)
            thread.start()

        except Exception as e:
            messagebox.showerror("错误", f"启动调试器时出现错误: {e}")
            print(f"❌ 启动调试器错误: {e}")

def main():
    """主函数"""
    root = tk.Tk()
    app = InstagramLoginGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
