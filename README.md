pygame
pillow
pystray
keyboard

```

### 安装依赖

```bash
pip install -r requirements.txt
```
### 运行开发版本

```bash
python main.py
```
### 项目结构

```
src/
├── core/           # 核心功能
│   ├── config.py   # 配置管理
│   └── sound_player.py  # 音频播放
├── gui/            # 界面相关
│   ├── keyboard_ui.py   # 键盘界面
│   ├── main_window.py   # 主窗口
│   ├── help_window.py   # 帮助窗口
│   └── styles.py        # 样式定义
└── utils/          # 工具函数
    └── resource.py      # 资源管理
```
## 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 致谢

- 感谢所有贡献者的支持
- 使用了以下开源项目：
  - [pygame](https://www.pygame.org/)
  - [tkinter](https://docs.python.org/3/library/tkinter.html)
  - [keyboard](https://github.com/boppreh/keyboard)
  - [pystray](https://github.com/moses-palmer/pystray)

## 作者

**Byclemon**

- GitHub: [@byclemon](https://github.com/byclemon)

## 更新日志

### v1.0.0 (2024-03-21)

- 首次发布
- 实现基本功能：按键绑定、场景管理、音效播放
- 添加可视化键盘界面
- 支持场景导入导出
- 支持系统托盘运行

```
