import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw
import requests
from io import BytesIO


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
                                  highlightthickness=0,
                                  padx=20,
                                  pady=10)
        self.login_btn.pack(pady=(30, 20), fill='x')
        
        # 创建圆角效果
        self.create_rounded_button(self.login_btn, 8)

        # 添加登录按钮悬停效果
        self.add_login_button_effects()

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
        bottom_frame = tk.Frame(self.login_container, bg='#fafafa')
        bottom_frame.pack(side='bottom', fill='x', pady=(30, 10))

        info_text = tk.Label(bottom_frame, text="简洁 • 安全 • 快速",
                            font=('Microsoft YaHei', 9),
                            fg='#8e8e8e', bg='#fafafa')
        info_text.pack()

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

    def login(self):
        """登录处理"""
        username = self.get_input_value('username')
        password = self.get_input_value('password')

        if not username or not password:
            messagebox.showerror("错误", "请输入用户名和密码")
            return

        # 这里可以添加实际的登录逻辑
        # 目前只是显示一个消息框
        messagebox.showinfo("登录成功", f"欢迎回来，{username}！")

        # 实际应用中，您可以在这里调用Instagram API或其他认证服务
        # 例如：
        # success = authenticate_user(username, password)
        # if success:
        #     self.root.destroy()  # 关闭登录窗口
        #     open_main_app()      # 打开主应用

    def forgot_password(self, event):
        """忘记密码处理"""
        messagebox.showinfo("忘记密码", "请联系管理员重置密码")

def main():
    """主函数"""
    root = tk.Tk()
    app = InstagramLoginGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
