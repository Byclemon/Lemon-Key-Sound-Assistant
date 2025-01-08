import json
import os

class ConfigManager:
    @staticmethod
    def load_config():
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 如果是旧版配置，转换为新格式
                if 'key_sounds' in config and 'scenes' not in config:
                    config = {
                        'current_scene': 'default',
                        'scenes': {
                            'default': {
                                'name': '默认场景',
                                'key_sounds': config['key_sounds']
                            }
                        },
                        'stop_key': config.get('stop_key', 'SPACE'),
                        'stop_on_unbound': config.get('stop_on_unbound', True),
                        'long_press_optimize': config.get('long_press_optimize', True)
                    }
                return config
        except FileNotFoundError:
            return {
                'current_scene': 'default',
                'scenes': {
                    'default': {
                        'name': '默认场景',
                        'key_sounds': {}
                    }
                },
                'stop_key': 'SPACE',
                'stop_on_unbound': True,
                'long_press_optimize': True
            }
    
    @staticmethod
    def save_config(config):
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)