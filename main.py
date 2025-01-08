import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.gui.main_window import GUI

if __name__ == "__main__":
    app = GUI()
    app.run()