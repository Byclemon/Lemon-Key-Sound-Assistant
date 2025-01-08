from tkinter import *
from tkinter import ttk, messagebox, filedialog
import pystray
from PIL import Image, ImageTk
import keyboard
from ..core.sound_player import SoundPlayer
from ..utils.resource import ResourceManager
from .help_window import HelpWindow
from .styles import configure_styles
import os
from .keyboard_ui import KeyboardUI

# 定义全局颜色变量
COLORS = {
    'bg_main': '#F5F7FA',           # 主背景色
    'bg_white': '#FFFFFF',          # 白色背景
    'primary': '#2196F3',           # 主色调（统一的蓝色）
    'primary_light': '#E3F2FD',     # 主色调浅色
    'primary_hover': '#1976D2',     # 主色调悬停
    'text_primary': '#333333',      # 主要文字
    'text_secondary': '#666666',    # 次要文字
    'button_default': '#F5F5F5',    # 默认按钮背景
    'button_text': '#333333',       # 默认按钮文字
    'button_hover': '#E0E0E0',      # 默认按钮悬停
}

class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("柠檬键音助手 BY Byclemon")
        self.root.geometry("1200x800")
        self.root.configure(bg='#FFFFFF')
        
        # 创建样式
        self.style = ttk.Style()
        
        # 配置样式
        configure_styles(self)
        
        # 创建播放器
        self.player = SoundPlayer()
        
        # 初始化实例变量
        self.header_left = None
        self.stop_key_button = None
        
        # 设置窗口图标
        self.setup_window_icon()
        
        # 创建界面
        self.create_widgets()
        
        # 创建系统托盘图标
        self.create_tray_icon()
        
        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 标记是否最小化到托盘
        self.minimized = False
    
    def setup_window_icon(self):
        """设置窗口图标"""
        icon_path = ResourceManager.get_resource_path('logo.png')
        try:
            icon_image = Image.open(icon_path)
            icon = ImageTk.PhotoImage(icon_image)
            self.root.iconphoto(True, icon)
            self.icon_image = icon_image  # 保存引用防止被回收
        except Exception as e:
            print(f"[DEBUG] 加载图标失败: {e}")
    
    def create_tray_icon(self):
        """创建系统托盘图标"""
        try:
            # 获取图标文件路径
            icon_path = ResourceManager.get_resource_path('logo.png')
            image = Image.open(icon_path)
            
            def on_left_click(icon, item):
                print("[DEBUG] 托盘图标被点击")
                self.show_window()
            
            menu = (
                pystray.MenuItem("显示主窗口", self.show_window, default=True),  # 设置为默认动作
                pystray.MenuItem("退出程序", self.quit_app)
            )
            print("[DEBUG] 创建托盘图标")
            self.tray_icon = pystray.Icon(
                "柠檬键音助手",
                image,
                "柠檬键音助手",
                menu
            )
        except Exception as e:
            print(f"[DEBUG] 加载托盘图标失败: {e}")
            self.tray_icon = None
    
    def show_window(self, icon=None, item=None):
        print(f"[DEBUG] show_window 被调用: icon={icon}, item={item}")
        def do_show():
            print("[DEBUG] 开始显示窗口")
            self.root.deiconify()
            self.root.state('normal')
            self.root.lift()
            self.root.focus_force()
            self.root.attributes('-topmost', True)
            self.root.update()
            self.root.attributes('-topmost', False)
            self.minimized = False
            print("[DEBUG] 窗口显示完成")
        
        if icon:
            print("[DEBUG] 通过托盘图标调用，使用 after")
            self.root.after(0, do_show)
        else:
            print("[DEBUG] 直接调用显示窗口")
            do_show()
    
    def hide_window(self):
        print("[DEBUG] 开始隐藏窗口")
        self.minimized = True
        self.root.withdraw()
        if not self.tray_icon.visible:
            print("[DEBUG] 托盘图标不可见，启动托盘图标")
            self.tray_icon.run()
        print("[DEBUG] 窗口隐藏完成")
    
    def on_closing(self):
        # 直接最小化到托盘，不再询问
        self.hide_window()
        # 显示提示信息
        self.tray_icon.notify(
            "程序已最小化到系统托盘",
            "点击托盘图标可以重新打开窗口"
        )
    
    def quit_app(self, icon=None, item=None):
        # 停止播放器
        if self.player.is_running:
            if self.player.keyboard_listener:
                keyboard.unhook(self.player.keyboard_listener)
            if self.player.keyboard_release_listener:
                keyboard.unhook(self.player.keyboard_release_listener)
            self.player.stop_sound()
        
        # 停止托盘图标
        if hasattr(self, 'tray_icon'):
            try:
                self.tray_icon.stop()
            except:
                pass
        
        # 确保程序完全退出
        self.root.after(100, self._force_quit)
    
    def _force_quit(self):
        try:
            self.root.quit()
            self.root.destroy()
        finally:
            os._exit(0)  # 强制退出程序
    
    def run(self):
        print("[DEBUG] 程序开始运行")
        print("[DEBUG] 启动托盘图标")
        self.tray_icon.run_detached()
        print("[DEBUG] 运行主窗口")
        self.root.mainloop()

    def show_help(self):
        """显示帮助窗口"""
        HelpWindow(self.root)
    
    def add_new_sound(self):
        """添加新的按键绑定"""
        # 检查是否在监听模式
        if self.player.is_running:
            messagebox.showinfo("提示", "请先停止监听，再添加按键绑定")
            return
        
        dialog = Toplevel(self.root)
        dialog.title("设置按键")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = self.root.winfo_x() + (self.root.winfo_width() - width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - height) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 提示标签
        Label(dialog,
              text="请按下要绑定的按键",
              font=('Microsoft YaHei UI', 12),
              pady=20).pack()
        
        # 按键显示标签
        key_label = Label(dialog,
                         text="等待按键...",
                         font=('Microsoft YaHei UI', 16, 'bold'))
        key_label.pack(pady=10)
        
        # 标记对话框是否已关闭
        dialog.is_closed = False
        
        def on_key(event):
            if dialog.is_closed:
                return
            
            key = event.name.upper()
            
            # 检查是否是停止键
            if key == self.player.stop_key:
                key_label.config(text=f"按键 {key} 已被设为停止键", fg='#f44336')
                dialog.after(1500, lambda: key_label.config(
                    text="请按下其他按键...",
                    fg='#000000'
                ))
                return
                
            # 检查按键是否已存在
            if key in self.player.key_sounds:
                key_label.config(text=f"按键 {key} 已被绑定", fg='#f44336')
                dialog.after(1500, lambda: key_label.config(
                    text="请按下其他按键...",
                    fg='#000000'
                ))
                return
            
            # 选择音频文件
            file_path = filedialog.askopenfilename(
                title="选择音频文件",
                filetypes=[("音频文件", "*.mp3;*.wav")]
            )
            
            if file_path:
                self.player.add_sound(key, file_path)
                self.update_binding_list()
            
            dialog.destroy()
            dialog.is_closed = True
        
        # 绑定键盘事件
        keyboard_listener = keyboard.on_press(on_key)
        
        def on_dialog_close():
            dialog.is_closed = True
            try:
                keyboard.unhook(keyboard_listener)
            except:
                pass
            dialog.destroy()
        
        dialog.protocol("WM_DELETE_WINDOW", on_dialog_close)
        dialog.wait_window()
    
    def update_binding_list(self):
        """更新绑定显示"""
        if hasattr(self, 'keyboard_ui'):
            self.keyboard_ui.refresh_all()
    
    def toggle_stop_on_unbound(self):
        """切换未绑定按键停止播放的设置"""
        self.player.stop_on_unbound = self.stop_on_unbound_var.get()
        self.player.save_config()
    
    def save_setting(self, setting_name, value):
        """保存设置"""
        if setting_name == 'long_press_optimize':
            self.player.long_press_optimize = value
        self.player.save_config()

    def create_widgets(self):
        """创建主界面控件"""
        # 创建主容器
        container = ttk.Frame(self.root)
        container.pack(fill='both', expand=True)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(container)
        scrollbar.pack(side='right', fill='y')
        
        # 创建可滚动的文本区域
        self.canvas = Canvas(container,
                            bg='#F5F7FA',
                            highlightthickness=0)
        self.canvas.pack(side='left', fill='both', expand=True)
        
        # 创建内容框架
        self.main_frame = Frame(self.canvas, bg='#F5F7FA')
        self.canvas_frame = self.canvas.create_window(
            (0, 0),
            window=self.main_frame,
            anchor='nw',
            width=self.canvas.winfo_width()
        )
        
        # 配置滚动
        scrollbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=scrollbar.set)
        
        # 绑定事件
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        self.main_frame.bind('<Configure>', self._on_frame_configure)
        self.root.bind('<MouseWheel>', self._on_mousewheel)
        
        # 标题区域
        title_frame = Frame(self.main_frame, bg='#F5F7FA')
        title_frame.pack(fill='x', pady=(30, 40), padx=40)
        
        # 标题
        Label(title_frame, 
              text="柠檬键音助手",
              font=('Microsoft YaHei UI', 36, 'bold'),
              bg='#F5F7FA',
              fg='#1A237E').pack()
        
        Label(title_frame,
              text="让您的键盘发出美妙声音",
              font=('Microsoft YaHei UI', 14),
              bg='#F5F7FA',
              fg='#5C6BC0').pack(pady=(5, 0))
        
        # 帮助按钮
        Button(title_frame,
               text="使用说明",
               command=self.show_help,
               font=('Microsoft YaHei UI', 11),
               bg='#E8EAF6',
               fg='#3F51B5',
               relief='flat',
               cursor='hand2',
               padx=15,
               pady=8).pack(side='right')
        
        # 状态和控制区域
        self.control_container = Frame(self.main_frame, bg='#FFFFFF')
        self.control_container.pack(fill='x', pady=(0, 30), padx=30)
        
        # 状态显示区域
        status_frame = Frame(self.control_container, bg='#FFFFFF')
        status_frame.pack(fill='x', padx=30, pady=25)
        
        # 状态标签
        self.status_label = Label(status_frame, 
                                text="等待启动...",
                                font=('Microsoft YaHei UI', 13),
                                bg='#FFFFFF',
                                fg='#546E7A')
        self.status_label.pack(side='left')
        
        # 启动按钮
        self.start_button = Button(status_frame,
                                 text="启动监听",
                                 command=self.player.toggle_running,
                                 font=('Microsoft YaHei UI', 12, 'bold'),
                                 bg=COLORS['primary'],
                                 fg='white',
                                 width=12,
                                 height=1,
                                 relief='flat',
                                 cursor='hand2')
        self.start_button.pack(side='right')
        
        # 分隔线
        Frame(self.control_container, height=1, bg='#E3F2FD').pack(fill='x')
        
        # 播放设置区域
        settings_frame = Frame(self.main_frame, bg='#FFFFFF')
        settings_frame.pack(fill='x', pady=(0, 30), padx=30)
        
        # 创建播放设置模块
        self.create_settings_module(settings_frame)
        
        # 场景管理区域
        scene_frame = Frame(self.main_frame, bg='#FFFFFF')
        scene_frame.pack(fill='x', pady=(0, 30), padx=30)
        
        # 创建场景管理模块
        self.create_scene_manager(scene_frame)
        
        # 按键绑定列表区域
        list_frame = Frame(self.main_frame, bg='#FFFFFF')
        list_frame.pack(fill='both', expand=True, pady=(0, 40), padx=30)
        
        # 标题和按钮区域
        header_frame = Frame(list_frame, bg=COLORS['bg_white'])
        header_frame.pack(fill='x', padx=30, pady=(20, 15))
        
        # 标题
        Label(header_frame,
              text="按键绑定",
              font=('Microsoft YaHei UI', 16, 'bold'),
              bg=COLORS['bg_white'],
              fg=COLORS['primary']).pack(side='left')
        
        # 按钮区域
        button_frame = Frame(header_frame, bg=COLORS['bg_white'])
        button_frame.pack(side='right')
        
        # 停止键按钮
        self.stop_key_button = Button(button_frame,
                                     text=f"停止键：{self.player.stop_key}",
                                     command=self.change_stop_key,
                                     font=('Microsoft YaHei UI', 11),
                                     bg=COLORS['primary'],
                                     fg='white',
                                     relief='flat',
                                     cursor='hand2',
                                     padx=15,
                                     pady=5)
        self.stop_key_button.pack(side='right', padx=5)
        
        # 添加绑定按钮
        Button(button_frame,
               text="添加绑定",
               command=self.add_new_sound,
               font=('Microsoft YaHei UI', 11),
               bg=COLORS['primary'],
               fg='white',
               relief='flat',
               cursor='hand2',
               padx=15,
               pady=5).pack(side='right', padx=5)
        
        # 为所有按钮添加悬停效果
        for btn in button_frame.winfo_children():
            btn.bind('<Enter>', lambda e: e.widget.config(bg=COLORS['primary_hover']))
            btn.bind('<Leave>', lambda e: e.widget.config(bg=COLORS['primary']))
        
        # 创建键盘 UI 容器
        keyboard_container = Frame(
            list_frame,
            bg=COLORS['bg_white'],
            width=1000,  # 设置一个足够大的固定宽度
            height=400   # 设置一个合适的固定高度
        )
        keyboard_container.pack(fill='x', expand=False, padx=30)  # 改为 expand=False
        keyboard_container.pack_propagate(False)  # 防止子组件改变容器大小
        
        # 创建键盘 UI
        self.keyboard_ui = KeyboardUI(
            keyboard_container,
            self.player,
            bg=COLORS['bg_white']
        )
        self.keyboard_ui.place(relx=0.5, rely=0.5, anchor='center')  # 使用place布局居中显示
        
        # 不在这里调用 update_binding_list
        # self.update_binding_list()
        
        # 设置 GUI 元素引用
        self.player.set_gui_elements(self.status_label, self.start_button, self)
        
        # 启动按钮样式
        self.start_button.config(
            bg=COLORS['primary'],
            activebackground=COLORS['primary_hover']
        )
        
        # 添加绑定按钮的样式
        for button in button_frame.winfo_children():
            button.config(
                bg=COLORS['primary'],
                fg='white',
                activebackground=COLORS['primary_hover'],
                activeforeground='white'
            )

    def change_stop_key(self):
        """修改停止键"""
        # 检查是否在监听模式
        if self.player.is_running:
            messagebox.showinfo("提示", "请先停止监听，再修改停止键")
            return
        
        dialog = Toplevel(self.root)
        dialog.title("设置停止键")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = self.root.winfo_x() + (self.root.winfo_width() - width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - height) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 提示标签
        Label(dialog,
              text="请按下要设置为停止键的按键",
              font=('Microsoft YaHei UI', 12),
              pady=20).pack()
        
        # 按键显示标签
        key_label = Label(dialog,
                         text="等待按键...",
                         font=('Microsoft YaHei UI', 16, 'bold'))
        key_label.pack(pady=10)
        
        # 标记对话框是否已关闭
        dialog.is_closed = False
        
        def on_key_press(event):
            if dialog.is_closed:
                return
            
            key = event.name.upper()
            
            # 检查按键是否已被绑定音频
            if key in self.player.key_sounds:
                key_label.config(text=f"按键 {key} 已被绑定音频", fg='#f44336')
                dialog.after(1500, lambda: key_label.config(
                    text="请按下其他按键...",
                    fg='#000000'
                ))
                return
            
            # 更新停止键
            self.player.stop_key = key
            self.player.save_config()
            
            # 更新按钮文字
            self.stop_key_button.config(text=f"停止键：{key}")
            
            # 刷新键盘显示
            self.keyboard_ui.refresh_all()
            
            dialog.destroy()
            dialog.is_closed = True
        
        # 绑定键盘事件
        keyboard_listener = keyboard.on_press(on_key_press)
        
        def on_dialog_close():
            dialog.is_closed = True
            try:
                keyboard.unhook(keyboard_listener)
            except:
                pass
            dialog.destroy()
        
        dialog.protocol("WM_DELETE_WINDOW", on_dialog_close)
        dialog.wait_window()

    def create_settings_module(self, parent):
        """创建设置模块"""
        # 标题
        Label(parent,
              text="播放设置",
              font=('Microsoft YaHei UI', 16, 'bold'),
              bg='#FFFFFF',
              fg='#1565C0').pack(anchor='w', padx=30, pady=(20, 15))
        
        # 设置选项容器
        options_frame = Frame(parent, bg='#FFFFFF')
        options_frame.pack(fill='x', padx=30, pady=(0, 20))
        
        
        # 长按优化选项
        optimize_var = BooleanVar(value=self.player.long_press_optimize)
        optimize_check = ttk.Checkbutton(
            options_frame,
            text="长按优化模式（防止按住按键重复播放）",
            variable=optimize_var,
            command=lambda: self.on_optimize_change(optimize_var.get()),
            style='Switch.TCheckbutton'
        )
        optimize_check.pack(side='left', padx=(0, 30))
        
        # 未绑定按键停止选项
        self.stop_on_unbound_var = BooleanVar(value=self.player.stop_on_unbound)
        stop_check = ttk.Checkbutton(
            options_frame,
            text="未绑定按键时停止播放",
            variable=self.stop_on_unbound_var,
            command=self.on_stop_unbound_change,
            style='Switch.TCheckbutton'
        )
        stop_check.pack(side='left')

    def on_optimize_change(self, value):
        """处理长按优化选项变化"""
        self.save_setting('long_press_optimize', value)
        self.root.focus_set()  # 移除复选框焦点

    def on_stop_unbound_change(self):
        """处理未绑定按键停止选项变化"""
        self.toggle_stop_on_unbound()
        self.root.focus_set()  # 移除复选框焦点

    def create_scene_manager(self, parent):
        """创建场景管理模块"""
        # 标题和按钮区域
        header_frame = Frame(parent, bg=COLORS['bg_white'])
        header_frame.pack(fill='x', padx=30, pady=(20, 15))
        
        # 标题
        Label(header_frame,
              text="场景管理",
              font=('Microsoft YaHei UI', 16, 'bold'),
              bg=COLORS['bg_white'],
              fg=COLORS['primary']).pack(side='left')
        
        # 按钮区域
        button_frame = Frame(header_frame, bg=COLORS['bg_white'])
        button_frame.pack(side='right')
        
        # 场景管理按钮
        buttons = [
            ("新建场景", self.create_new_scene),
            ("删除场景", self.delete_scene),
            ("导入配置", self.import_scene),
            ("导出配置", self.export_scene),
        ]
        
        for text, command in buttons:
            btn = Button(button_frame,
                        text=text,
                        command=command,
                        font=('Microsoft YaHei UI', 11),
                        bg=COLORS['primary'],
                        fg='white',
                        relief='flat',
                        cursor='hand2',
                        padx=15,
                        pady=5)
            btn.pack(side='right', padx=5)
            
            # 添加悬停效果
            btn.bind('<Enter>', lambda e: e.widget.config(bg=COLORS['primary_hover']))
            btn.bind('<Leave>', lambda e: e.widget.config(bg=COLORS['primary']))
        
        # 场景标签容器
        tabs_container = Frame(parent, bg='#FFFFFF')
        tabs_container.pack(fill='x', padx=30, pady=(0, 20))
        
        # 创建场景标签页容器
        self.scene_tabs = Frame(tabs_container, bg='#FFFFFF')
        self.scene_tabs.pack(fill='x')
        
        # 初始化场景标签页
        self.update_scene_tabs()

    def update_scene_tabs(self):
        """更新场景标签页"""
        # 清除所有现有标签页
        for widget in self.scene_tabs.winfo_children():
            widget.destroy()
        
        # 创建标签页容器
        tabs_frame = Frame(self.scene_tabs, bg=COLORS['bg_white'])
        tabs_frame.pack(fill='x', pady=10)
        
        # 创建新的标签页
        for scene_id, scene_data in self.player.scenes.items():
            tab = Frame(tabs_frame, bg=COLORS['bg_white'], cursor='hand2')
            tab.pack(side='left', padx=4)  # 增加标签间距
            
            # 判断是否是当前场景
            is_current = scene_id == self.player.current_scene
            
            # 标签页按钮
            btn = Label(tab,
                       text=scene_data['name'],
                       font=('Microsoft YaHei UI', 11),
                       bg=COLORS['primary_light'] if is_current else COLORS['bg_white'],
                       fg=COLORS['primary'] if is_current else COLORS['text_secondary'],
                       padx=20,  # 增加水平内边距
                       pady=10)  # 增加垂直内边距
            btn.pack(fill='both')
            
            # 底部指示条
            indicator = Frame(tab,
                             bg=COLORS['primary'] if is_current else COLORS['bg_white'],
                             height=3)  # 增加指示条高度
            indicator.pack(fill='x')
            
            # 绑定点击事件
            def make_callback(sid):
                return lambda e: self.on_scene_change(sid)
            
            btn.bind('<Button-1>', make_callback(scene_id))
            
            # 绑定鼠标悬停效果
            def on_enter(e, ind, is_current):
                if not is_current:
                    e.widget.config(bg='#F5F5F5')
                    ind.config(bg=COLORS['primary_light'])  # 使用浅色指示条
            
            def on_leave(e, ind, is_current):
                if not is_current:
                    e.widget.config(bg=COLORS['bg_white'])
                    ind.config(bg=COLORS['bg_white'])
            
            if not is_current:
                btn.bind('<Enter>', lambda e, i=indicator: on_enter(e, i, is_current))
                btn.bind('<Leave>', lambda e, i=indicator: on_leave(e, i, is_current))

    def on_scene_change(self, scene_id):
        """处理场景切换"""
        if self.player.switch_scene(scene_id):
            self.update_binding_list()
            self.update_scene_tabs()  # 更新标签页显示

    def create_new_scene(self):
        """创建新场景"""
        dialog = Toplevel(self.root)
        dialog.title("新建场景")
        dialog.geometry("400x250")  # 增加高度
        dialog.configure(bg='#FFFFFF')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = self.root.winfo_x() + (self.root.winfo_width() - width) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - height) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 主容器
        main_frame = Frame(dialog, bg='#FFFFFF', padx=40, pady=30)
        main_frame.pack(fill='both', expand=True)
        
        # 标题
        Label(main_frame,
              text="创建新场景",
              font=('Microsoft YaHei UI', 16, 'bold'),
              bg='#FFFFFF',
              fg='#1565C0').pack(pady=(0, 25))
        
        # 输入框容器
        entry_frame = Frame(main_frame, bg='#FFFFFF')
        entry_frame.pack(fill='x', pady=(0, 30))
        
        # 输入框
        name_entry = Entry(entry_frame,
                          font=('Microsoft YaHei UI', 11),
                          justify='center',
                          relief='solid',
                          bd=1)
        name_entry.pack(fill='x', ipady=8)  # 增加输入框高度
        name_entry.insert(0, "请输入场景名称")
        name_entry.config(fg='#999999')
        
        # 输入框焦点事件
        def on_focus_in(e):
            if name_entry.get() == "请输入场景名称":
                name_entry.delete(0, 'end')
                name_entry.config(fg='#333333')
        
        def on_focus_out(e):
            if not name_entry.get():
                name_entry.insert(0, "请输入场景名称")
                name_entry.config(fg='#999999')
        
        name_entry.bind('<FocusIn>', on_focus_in)
        name_entry.bind('<FocusOut>', on_focus_out)
        
        # 按钮容器
        button_frame = Frame(main_frame, bg='#FFFFFF')
        button_frame.pack(fill='x')
        
        # 设置按钮权重，使其平分宽度
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        def on_confirm():
            name = name_entry.get().strip()
            if name and name != "请输入场景名称":
                scene_id = f"scene_{len(self.player.scenes)}"
                while scene_id in self.player.scenes:
                    scene_id = f"scene_{int(scene_id.split('_')[1]) + 1}"
                
                if self.player.add_scene(scene_id, name):
                    self.update_scene_tabs()
                    self.update_binding_list()
                    dialog.destroy()
            else:
                messagebox.showwarning("提示", "请输入场景名称")
        
        # 取消按钮
        Button(button_frame,
               text="取消",
               command=dialog.destroy,
               font=('Microsoft YaHei UI', 11),
               bg='#F5F5F5',
               fg='#333333',
               relief='flat',
               cursor='hand2',
               width=12,
               pady=8,
               activebackground='#E0E0E0',
               activeforeground='#333333').grid(row=0, column=0, padx=(0, 5))
        
        # 确定按钮
        Button(button_frame,
               text="确定",
               command=on_confirm,
               font=('Microsoft YaHei UI', 11),
               bg=COLORS['primary'],
               fg='white',
               relief='flat',
               cursor='hand2',
               width=12,
               pady=8,
               activebackground=COLORS['primary_hover'],
               activeforeground='white').grid(row=0, column=1, padx=(5, 0))
        
        # 绑定回车键和ESC键
        dialog.bind('<Return>', lambda e: on_confirm())
        dialog.bind('<Escape>', lambda e: dialog.destroy())
        
        # 设置初始焦点
        name_entry.focus_set()
        name_entry.select_range(0, 'end')

    def import_scene(self):
        """导入配置"""
        filepath = filedialog.askopenfilename(
            title="导入配置",
            filetypes=[("配置文件", "*.json")]
        )
        if filepath:
            if self.player.import_config(filepath):
                # 更新场景标签页
                self.update_scene_tabs()
                # 更新按键绑定列表
                self.update_binding_list()
                # 更新停止键显示
                self.stop_key_button.config(text=f"停止键：{self.player.stop_key}")
                messagebox.showinfo("成功", "配置导入成功")

    def export_scene(self):
        """导出配置"""
        filepath = filedialog.asksaveasfilename(
            title="导出配置",
            defaultextension=".json",
            filetypes=[("配置文件", "*.json")]
        )
        if filepath:
            if self.player.export_config(filepath):
                messagebox.showinfo("成功", "配置导出成功")

    def delete_scene(self):
        """删除当前场景"""
        current_scene = self.player.current_scene
        scene_name = self.player.scenes[current_scene]['name']
        
        # 确认删除
        if messagebox.askyesno("确认删除", f"确定要删除场景「{scene_name}」吗？\n删除后无法恢复。"):
            if self.player.remove_scene(current_scene):
                # 更新场景标签页和按键绑定列表
                self.update_scene_tabs()
                self.update_binding_list()

    def _on_canvas_configure(self, event):
        """处理画布大小变化"""
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def _on_frame_configure(self, event):
        """处理框架大小变化"""
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def _on_mousewheel(self, event):
        """处理鼠标滚轮事件"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

    def load_scene(self, scene_name):
        """加载场景"""
        # 先更新数据
        self.player.load_scene(scene_name)
        
        # 更新场景标签
        for label in self.scene_labels:
            if label.cget('text') == scene_name:
                label.config(bg=COLORS['primary'], fg='white')
            else:
                label.config(bg=COLORS['button_default'], fg=COLORS['button_text'])
        
        # 更新键盘UI（如果已经创建）
        if hasattr(self, 'keyboard_ui'):
            self.after(10, self.keyboard_ui.refresh_all)  # 延迟一下刷新，避免布局抖动

    # ... 其他 GUI 类的方法 ... 