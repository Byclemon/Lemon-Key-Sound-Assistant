from tkinter import *
from tkinter import ttk, messagebox
import os

class KeyboardUI(Frame):
    def __init__(self, parent, player, **kwargs):
        super().__init__(parent, **kwargs)
        self.player = player
        self.configure(bg='#FFFFFF')
        
        # 设置固定尺寸
        self.pack_propagate(False)  # 防止子组件影响容器大小
        self.grid_propagate(False)  # 防止网格布局影响容器大小
        
        # 计算键盘合适的固定尺寸
        base_width = 64  # 基础按键宽度
        base_height = 64  # 基础按键高度
        gap = 6  # 间隙
        
        # 计算总宽度（基于最长的一行）
        total_width = (base_width * 15) + (gap * 14) + 20  # 15个单位宽度 + 间隙 + padding
        # 计算总高度（5行按键）
        total_height = (base_height * 5) + (gap * 4) + 20  # 5行按键 + 间隙 + padding
        
        # 设置固定尺寸
        self.configure(width=total_width, height=total_height)
        
        # 键盘布局定义 - 使用统一的单位宽度
        self.keyboard_layout = [
            # 第一行 - 数字键
            [
                ('`', 1), ('1', 1), ('2', 1), ('3', 1), ('4', 1), ('5', 1),
                ('6', 1), ('7', 1), ('8', 1), ('9', 1), ('0', 1),
                ('-', 1), ('=', 1), ('BACKSPACE', 2)  # 总宽度：15单位
            ],
            # 第二行
            [
                ('TAB', 1.5), ('Q', 1), ('W', 1), ('E', 1), ('R', 1), ('T', 1),
                ('Y', 1), ('U', 1), ('I', 1), ('O', 1), ('P', 1),
                ('[', 1), (']', 1), ('\\', 1.5)  # 总宽度：15单位
            ],
            # 第三行
            [
                ('CAPS', 1.75), ('A', 1), ('S', 1), ('D', 1), ('F', 1), ('G', 1),
                ('H', 1), ('J', 1), ('K', 1), ('L', 1), (';', 1),
                ("'", 1), ('ENTER', 2.25)  # 总宽度：15单位
            ],
            # 第四行
            [
                ('SHIFT', 2.25), ('Z', 1), ('X', 1), ('C', 1), ('V', 1), ('B', 1),
                ('N', 1), ('M', 1), (',', 1), ('.', 1), ('/', 1),
                ('SHIFT', 2.75)  # 总宽度：15单位
            ],
            # 第五行
            [
                ('CTRL', 1.75), ('WIN', 1.75), ('ALT', 1.75), 
                ('SPACE', 6.8),
                ('ALT', 1.75), ('CTRL', 1.75)  # 总宽度：15单位
            ]
        ]
        
        self.create_keyboard()
        
    def create_keyboard(self):
        """创建键盘界面"""
        # 键盘容器
        keyboard_frame = Frame(self, bg='#FFFFFF', padx=10, pady=10)
        keyboard_frame.pack(expand=True)
        
        # 基础按键大小
        base_width = 64  # 增大基础宽度
        base_height = 64  # 增大基础高度
        gap = 6  # 调整间隙
        
        # 创建每一行按键
        for row_index, row in enumerate(self.keyboard_layout):
            row_frame = Frame(keyboard_frame, bg='#FFFFFF')
            row_frame.pack(pady=gap/2)
            
            # 计算当前行的总单位数
            total_units = sum(width for _, width in row)
            
            # 创建每个按键
            for key, width_multiplier in row:
                # 计算按键宽度，确保每行总宽度相同
                key_width = int(base_width * width_multiplier)
                key_button = self.create_key_button(
                    row_frame, 
                    key, 
                    key_width, 
                    base_height
                )
                key_button.pack(side='left', padx=gap/2)
    
    def create_key_button(self, parent, key, width, height):
        """创建单个按键"""
        # 按键框架
        button_frame = Frame(
            parent,
            width=width,
            height=height,
            bg='#FFFFFF'
        )
        button_frame.pack_propagate(False)
        
        # 判断按键是否已绑定音频或是停止键
        is_bound = key in self.player.key_sounds
        is_stop_key = key.upper() == self.player.stop_key.upper()
        
        # 设置按键颜色和显示文本
        display_text = key
        if is_stop_key:
            bg_color = '#FF5252'
            fg_color = '#FFFFFF'
            display_text = f"{key}\n[停止键]"
        elif is_bound:
            bg_color = '#2196F3'
            fg_color = '#FFFFFF'
        else:
            bg_color = '#F5F5F5'
            fg_color = '#333333'
        
        # 创建内部框架（用于边框效果）
        inner_frame = Frame(
            button_frame,
            bg=bg_color,
            relief='raised',
            bd=1
        )
        inner_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # 创建按键标签
        button = Label(
            inner_frame,
            text=display_text,
            font=('Microsoft YaHei UI', 9, 'bold'),
            bg=bg_color,
            fg=fg_color,
            relief='flat',
            wraplength=width-8
        )
        button.pack(fill='both', expand=True)
        
        # 添加点击效果
        def on_press(e):
            if not is_stop_key:
                temp_color = '#1976D2' if is_bound else '#E0E0E0'
                inner_frame.config(bg=temp_color)
                button.config(bg=temp_color)
        
        def on_release(e):
            if not is_stop_key:
                # 根据按键当前状态恢复颜色
                current_is_bound = key in self.player.key_sounds
                if current_is_bound:
                    restore_color = '#2196F3'  # 已绑定的蓝色
                    restore_fg = '#FFFFFF'
                else:
                    restore_color = '#F5F5F5'  # 未绑定的灰色
                    restore_fg = '#333333'
                
                inner_frame.config(bg=restore_color)
                button.config(bg=restore_color, fg=restore_fg)
        
        # 绑定点击事件
        if not is_stop_key:
            button.bind('<Button-1>', lambda e: [on_press(e), self.on_key_click(key)])
            button.bind('<ButtonRelease-1>', on_release)
            inner_frame.bind('<Button-1>', lambda e: [on_press(e), self.on_key_click(key)])
            inner_frame.bind('<ButtonRelease-1>', on_release)
        else:
            button.bind('<Button-1>', lambda e: self.show_stop_key_message())
            inner_frame.bind('<Button-1>', lambda e: self.show_stop_key_message())
        
        return button_frame
    
    def on_key_click(self, key):
        """处理按键点击事件"""
        # 如果是停止键，不允许绑定
        if key == self.player.stop_key:
            return
            
        # 如果已经绑定了音频，显示选项菜单
        if key in self.player.key_sounds:
            self.show_key_menu(key)
        else:
            # 否则打开文件选择对话框绑定音频
            self.bind_new_sound(key)
    
    def show_key_menu(self, key):
        """显示已绑定按键的选项菜单"""
        menu = Menu(self, tearoff=0)
        menu.add_command(
            label=f"当前音频: {os.path.basename(self.player.key_sounds[key])}",
            state='disabled'
        )
        menu.add_separator()
        menu.add_command(label="更换音频", command=lambda: self.bind_new_sound(key))
        menu.add_command(label="删除绑定", command=lambda: self.remove_binding(key))
        
        # 在鼠标位置显示菜单
        menu.tk_popup(self.winfo_pointerx(), self.winfo_pointery())
    
    def bind_new_sound(self, key):
        """绑定新的音频文件"""
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            title=f"为按键 {key} 选择音频文件",
            filetypes=[("音频文件", "*.mp3;*.wav")]
        )
        
        if file_path:
            self.player.add_sound(key, file_path)
            self.refresh_all()  # 改回使用整体刷新
    
    def remove_binding(self, key):
        """删除按键绑定"""
        self.player.remove_sound(key)
        self.refresh_all()  # 改回使用整体刷新
    
    def show_stop_key_message(self):
        """显示停止键提示信息"""
        messagebox.showinfo("提示", "此按键已被设置为停止键，不能绑定音频")
    
    def refresh_all(self):
        """刷新所有按键的显示状态"""
        # 遍历所有按键并更新状态
        for widget in self.winfo_children():
            for row_frame in widget.winfo_children():
                for key_frame in row_frame.winfo_children():
                    # 获取按键的组件
                    inner_frame = key_frame.winfo_children()[0]
                    button = inner_frame.winfo_children()[0]
                    key = button.cget('text').split('\n')[0]  # 获取按键文本（去除可能的停止键标识）
                    
                    # 判断按键状态
                    is_bound = key in self.player.key_sounds
                    is_stop_key = key.upper() == self.player.stop_key.upper()
                    
                    # 设置按键颜色和显示文本
                    if is_stop_key:
                        bg_color = '#FF5252'
                        fg_color = '#FFFFFF'
                        display_text = f"{key}\n[停止键]"
                    elif is_bound:
                        bg_color = '#2196F3'
                        fg_color = '#FFFFFF'
                        display_text = key
                    else:
                        bg_color = '#F5F5F5'
                        fg_color = '#333333'
                        display_text = key
                    
                    # 更新按键外观
                    inner_frame.config(bg=bg_color)
                    button.config(
                        bg=bg_color,
                        fg=fg_color,
                        text=display_text
                    ) 