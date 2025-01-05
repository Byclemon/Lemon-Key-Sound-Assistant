
# 柠檬键音助手 (Lemon Key Sound Assistant)

一个简单易用的按键音效工具，让您的键盘按下时发出自定义的声音。

## 功能特点

- 🎵 自定义按键音效：为任意按键绑定 MP3 或 WAV 音频文件
- 🎹 可视化键盘界面：直观地显示和管理按键绑定
- 🎯 场景管理：支持创建多个场景，轻松切换不同的按键音效配置
- ⚡ 快捷操作：支持导入/导出配置，方便分享和备份
- 🛑 停止键设置：自定义停止所有音效播放的按键
- 🔄 长按优化：防止按键长按时重复播放音效
- 🎮 后台运行：支持最小化到系统托盘，不影响正常使用
- 🎨 现代界面：简洁美观的用户界面，操作直观

## 下载安装

从 [Releases](https://github.com/byclemon/lemon-key-sound/releases) 下载最新版本的压缩包，解压后运行 `柠檬键音助手.exe` 即可使用。

## 使用说明

### 基本操作

1. **添加按键绑定**
   - 点击界面右上角的"添加绑定"按钮
   - 按下要绑定的按键
   - 选择要绑定的音频文件（支持 MP3 和 WAV 格式）

2. **管理按键绑定**
   - 点击键盘界面上已绑定的按键（蓝色）可以更换或删除音效
   - 停止键（红色）用于停止所有正在播放的音效
   - 可以通过右上角的"停止键"按钮修改停止键

3. **场景管理**
   - 点击"新建场景"创建新的配置
   - 使用场景标签切换不同配置
   - 可以导入/导出场景配置文件（JSON 格式）

### 高级设置

- **长按优化**：开启后可以防止按键被按住时重复播放音效
- **未绑定按键停止播放**：开启后，按下未绑定音效的按键时会停止当前正在播放的音效

## 开发相关

### 环境要求

- Python 3.8+
- 依赖库：
  ```
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


