from tkinter import *
from tkinter import ttk

class HelpWindow:
    def __init__(self, parent):
        self.window = Toplevel(parent)
        self.window.title("使用说明")
        self.window.geometry("800x600")
        self.window.configure(bg='#FFFFFF')
        
        # 创建主容器
        container = ttk.Frame(self.window)
        container.pack(fill='both', expand=True)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(container)
        scrollbar.pack(side='right', fill='y')
        
        # 创建可滚动的文本区域
        self.text = Text(container, 
                        wrap=WORD,
                        padx=40,
                        pady=30,
                        bg='#FFFFFF',
                        fg='#333333',
                        border=0,
                        font=('Microsoft YaHei UI', 11))
        self.text.pack(side='left', fill='both', expand=True)
        
        # 配置滚动
        self.text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text.yview)
        
        # 添加内容
        self.add_content()
        
        # 禁用文本编辑
        self.text.config(state='disabled')
        
        # 设置模态
        self.window.transient(parent)
        self.window.grab_set()
    
    def add_content(self):
        """添加内容"""
        self.text.tag_configure('title', 
                              font=('Microsoft YaHei UI', 24, 'bold'),
                              foreground='#1565C0',
                              spacing3=30)  # 段后空间
        
        self.text.tag_configure('section', 
                              font=('Microsoft YaHei UI', 16, 'bold'),
                              foreground='#1565C0',
                              spacing1=25,   # 段前空间
                              spacing3=10)   # 段后空间
        
        self.text.tag_configure('content',
                              font=('Microsoft YaHei UI', 11),
                              foreground='#666666',
                              spacing1=3,    # 段前空间
                              spacing3=3)    # 段后空间
        
        self.text.tag_configure('footer',
                              font=('Microsoft YaHei UI', 11),
                              foreground='#666666',
                              spacing1=15,   # 段前空间
                              spacing3=3)    # 段后空间
        
        # 标题
        self.text.insert('end', "使用说明\n", 'title')
        
        # 基本操作
        self.text.insert('end', "基本操作\n", 'section')
        self.text.insert('end', """1. 点击"启动监听"开始使用
2. 在按键绑定中添加需要的按键和音频
3. 按下绑定的按键即可播放对应音频
4. 按下停止键可以停止当前播放的音频\n""", 'content')
        
        # 场景管理
        self.text.insert('end', "场景管理\n", 'section')
        self.text.insert('end', """1. 可以创建多个场景保存不同的按键配置
2. 点击场景标签可以快速切换场景
3. 支持导入导出配置文件
4. 场景设置会自动保存\n""", 'content')
        
        # 播放设置
        self.text.insert('end', "播放设置\n", 'section')
        self.text.insert('end', """1. 长按优化：防止按住按键重复播放
2. 未绑定按键停止：按下未绑定的按键时停止播放
3. 可以自定义停止键
4. 设置会自动保存并生效\n""", 'content')
        
        # 免责说明
        self.text.insert('end', "免责说明\n", 'section')
        self.text.insert('end', """本软件仅供学习和娱乐使用，请勿用于非法用途。使用本软件所产生的任何后果由用户自行承担。\n""", 'content')
        
        # 分隔线
        self.text.insert('end', "\n" + "─" * 80 + "\n\n", 'content')
        
        # 作者信息
        self.text.insert('end', """作者：byclemon
联系邮箱：byclemon@gmail.com""", 'footer') 