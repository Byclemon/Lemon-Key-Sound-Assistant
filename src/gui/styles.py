from tkinter import ttk

def configure_styles(gui):
    gui.style = ttk.Style()
    gui.style.configure('TButton', padding=6)
    gui.style.configure('TCheckbutton', 
                       background="#FFFFFF",
                       font=('Microsoft YaHei UI', 10))
    
    # 配置树形视图样式
    gui.style.configure('Custom.Treeview', 
                       background="#FFFFFF",
                       fieldbackground="#FFFFFF",
                       foreground='#333333',
                       rowheight=45,
                       font=('Microsoft YaHei UI', 11))
    
    # 设置选中行的样式
    gui.style.map('Custom.Treeview',
                  background=[('selected', '#E3F2FD')],
                  foreground=[('selected', '#1565C0')])
    
    # 配置复选框样式
    gui.style.configure('Switch.TCheckbutton',
                       background='#FFFFFF',
                       font=('Microsoft YaHei UI', 10))
    
    # 设置复选框选中和未选中状态的样式
    gui.style.map('Switch.TCheckbutton',
                 background=[('active', '#FFFFFF')],  # 鼠标悬停时保持白色背景
                 indicatorcolor=[('selected', '#2196F3'),  # 选中时的颜色
                               ('!selected', '#E0E0E0')],  # 未选中时的颜色
                 indicatorrelief=[('pressed', 'flat'),    # 按下时保持平面
                                ('!pressed', 'flat')])    # 未按下时保持平面