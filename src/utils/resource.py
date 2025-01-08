import os
import sys
from pathlib import Path

class ResourceManager:
    @staticmethod
    def get_resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller 打包后的路径
            return os.path.join(sys._MEIPASS, 'resources', relative_path)
        else:
            # 开发环境下的路径
            return os.path.join(Path(__file__).parent.parent.parent, 'resources', relative_path) 