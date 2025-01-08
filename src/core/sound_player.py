import pygame
import json
import os
from tkinter import messagebox, Toplevel
import keyboard
from .config import ConfigManager

class SoundPlayer:
    def __init__(self):
        try:
            pygame.mixer.init()
        except pygame.error as e:
            messagebox.showerror("错误", f"初始化音频系统失败: {str(e)}")
        self.key_sounds = {}        # 按键到音频文件路径的映射
        self.sounds = {}            # 按键到 Sound 对象的映射
        self.current_playing = None  # 当前播放的声音
        self.stop_on_unbound = True # 未绑定按键是否停止播放
        self.is_running = False     # 是否正在运行
        self.stop_key = 'SPACE'     # 停止键
        self.keyboard_listener = None 
        self.keyboard_release_listener = None
        self.pressed_keys = set()   # 只记录当前按下的键
        self.long_press_optimize = True  # 添加长按优化设置
        self.gui = None
        self.status_label = None
        self.start_button = None
        self.scenes = {}           # 所有场景
        self.current_scene = None  # 当前场景ID
        self.load_config()
        self.load_sounds()
    
    def load_sounds(self):
        """加载所有音频文件"""
        for key, sound_path in self.key_sounds.items():
            try:
                if os.path.exists(sound_path):
                    self.sounds[key] = pygame.mixer.Sound(sound_path)
                else:
                    messagebox.showwarning("警告", f"音频文件不存在: {sound_path}")
            except pygame.error as e:
                messagebox.showerror("错误", f"加载音频文件失败 {sound_path}: {str(e)}")
    
    def load_config(self):
        """加载配置"""
        config = ConfigManager.load_config()
        self.scenes = config.get('scenes', {})
        
        # 如果没有场景，创建一个默认场景
        if not self.scenes:
            self.scenes['scene_1'] = {
                'name': '默认场景',
                'key_sounds': {}
            }
        
        # 设置当前场景
        self.current_scene = config.get('current_scene')
        if not self.current_scene or self.current_scene not in self.scenes:
            self.current_scene = next(iter(self.scenes.keys()))
        
        self.key_sounds = self.scenes[self.current_scene]['key_sounds']
        self.stop_key = config.get('stop_key', 'SPACE')
        self.stop_on_unbound = config.get('stop_on_unbound', True)
        self.long_press_optimize = config.get('long_press_optimize', True)
    
    def save_config(self):
        """保存配置"""
        # 确保当前的 key_sounds 保存到当前场景
        self.scenes[self.current_scene]['key_sounds'] = self.key_sounds
        
        config = {
            'current_scene': self.current_scene,
            'scenes': self.scenes,
            'stop_key': self.stop_key,
            'stop_on_unbound': self.stop_on_unbound,
            'long_press_optimize': self.long_press_optimize
        }
        ConfigManager.save_config(config)
    
    def add_sound(self, key, sound_path):
        """添加新的按键音频绑定"""
        try:
            self.key_sounds[key] = sound_path
            self.sounds[key] = pygame.mixer.Sound(sound_path)
            self.save_config()
        except Exception as e:
            messagebox.showerror("错误", f"添加音频失败: {str(e)}")
    
    def play_sound(self, key):
        """播放指定按键的声音"""
        print(f"[DEBUG] 尝试播放按键 {key} 的声音")
        if key in self.sounds:
            # 如果有声音在播放，先停止并清除按键状态
            if self.current_playing:
                print(f"[DEBUG] 停止当前播放的声音")
                self.current_playing.stop()
                self.pressed_keys.clear()
                print(f"[DEBUG] 清除按键状态，当前状态: {self.pressed_keys}")
            
            # 播放新的声音
            print(f"[DEBUG] 开始播放按键 {key} 的声音")
            self.sounds[key].play()
            self.current_playing = self.sounds[key]
            self.pressed_keys.add(key)
            print(f"[DEBUG] 添加新按键，当前状态: {self.pressed_keys}")
            
            # 检查音频播放完成
            def check_sound_finished():
                if self.current_playing and not pygame.mixer.get_busy():
                    print(f"[DEBUG] 音频播放完成，清除状态")
                    self.current_playing = None
                    self.pressed_keys.clear()
                    print(f"[DEBUG] 清除后的按键状态: {self.pressed_keys}")
                    # 清除状态显示
                    if self.status_label:
                        self.status_label.config(text="正在运行" if self.is_running else "已停止")
                elif self.current_playing:
                    self.gui.root.after(100, check_sound_finished)
            
            self.gui.root.after(100, check_sound_finished)
    
    def stop_sound(self):
        """停止当前播放的声音"""
        if self.current_playing:
            self.current_playing.stop()
            self.current_playing = None
        self.pressed_keys.clear()
    
    def remove_sound(self, key):
        """移除按键音频绑定"""
        if key in self.key_sounds:
            del self.key_sounds[key]
            del self.sounds[key]
            self.save_config()
    
    def set_gui_elements(self, status_label, start_button, gui):
        """设置GUI元素引用"""
        self.status_label = status_label
        self.start_button = start_button
        self.gui = gui
    
    def toggle_running(self):
        """切换运行状态"""
        self.is_running = not self.is_running
        
        if self.is_running:
            self.keyboard_listener = keyboard.on_press(self.on_keyboard_press)
            self.keyboard_release_listener = keyboard.on_release(self.on_keyboard_release)
            if self.status_label:
                self.status_label.config(text="正在运行")
            if self.start_button:
                self.start_button.config(text="停止监听", bg='#f44336')
        else:
            if self.keyboard_listener:
                keyboard.unhook(self.keyboard_listener)
            if self.keyboard_release_listener:
                keyboard.unhook(self.keyboard_release_listener)
            self.pressed_keys.clear()
            self.stop_sound()
            if self.status_label:
                self.status_label.config(text="已停止")
            if self.start_button:
                self.start_button.config(text="启动监听", bg='#4CAF50')
    
    def on_keyboard_press(self, event):
        """处理按键按下事件"""
        if not self.is_running:
            return
            
        key = event.name.upper()
        
        # 如果有对话框打开，不处理按键事件
        if self.gui and self.gui.root.focus_get() and isinstance(self.gui.root.focus_get(), Toplevel):
            return
        
        # 如果是停止键
        if key == self.stop_key:
            self.stop_sound()
            if self.status_label:
                self.status_label.config(text="停止播放")
                self.gui.root.after(2000, lambda: self.status_label.config(
                    text="正在运行" if self.is_running else "已停止"
                ))
            return
        
        # 如果开启了长按优化，检查按键状态
        if self.long_press_optimize:
            if key in self.pressed_keys:
                return
            self.pressed_keys.add(key)
        
        self.play_sound_with_feedback(key)
    
    def on_keyboard_release(self, event):
        """处理按键释放事件"""
        key = event.name.upper()
        self.pressed_keys.discard(key)
    
    def play_sound_with_feedback(self, key):
        """播放声音并更新界面反馈"""
        if key in self.key_sounds:
            if self.status_label:
                self.status_label.config(text=f"播放按键 {key} 的音频")
            self.play_sound(key)
        else:
            if self.stop_on_unbound:
                self.stop_sound()
            if self.status_label:
                self.status_label.config(text=f"按键 {key} 未绑定音频")
        
        # 2秒后恢复状态显示
        if self.status_label and self.gui:
            self.gui.root.after(2000, lambda: self.status_label.config(
                text="正在运行" if self.is_running else "已停止"
            )) 
    
    def switch_scene(self, scene_id):
        """切换场景"""
        if scene_id in self.scenes:
            # 保存当前场景的按键绑定
            self.scenes[self.current_scene]['key_sounds'] = self.key_sounds
            # 切换到新场景
            self.current_scene = scene_id
            self.key_sounds = self.scenes[scene_id]['key_sounds']
            # 重新加载音频
            self.sounds.clear()
            self.load_sounds()
            # 保存配置
            self.save_config()
            return True
        return False
    
    def add_scene(self, scene_id, name):
        """添加新场景"""
        if scene_id not in self.scenes:
            self.scenes[scene_id] = {
                'name': name,
                'key_sounds': {}
            }
            # 自动切换到新场景
            self.switch_scene(scene_id)
            self.save_config()
            return True
        return False
    
    def remove_scene(self, scene_id):
        """删除场景"""
        if scene_id in self.scenes:
            # 如果只剩一个场景，不允许删除
            if len(self.scenes) == 1:
                messagebox.showwarning("警告", "至少需要保留一个场景")
                return False
            
            # 如果要删除的是当前场景，先保存当前场景的按键绑定
            if self.current_scene == scene_id:
                self.scenes[scene_id]['key_sounds'] = self.key_sounds
            
            # 删除场景
            del self.scenes[scene_id]
            
            # 如果删除的是当前场景，切换到其他场景
            if self.current_scene == scene_id:
                # 切换到第一个可用的场景
                new_scene_id = next(iter(self.scenes.keys()))
                self.current_scene = new_scene_id
                self.key_sounds = self.scenes[new_scene_id]['key_sounds']
                # 重新加载音频
                self.sounds.clear()
                self.load_sounds()
            
            self.save_config()
            return True
        return False
    
    def export_scene(self, scene_id, filepath):
        """导出场景"""
        if scene_id in self.scenes:
            scene_data = self.scenes[scene_id]
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(scene_data, f, indent=4, ensure_ascii=False)
                return True
            except Exception as e:
                messagebox.showerror("错误", f"导出场景失败: {str(e)}")
        return False
    
    def import_scene(self, filepath):
        """导入场景"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                scene_data = json.load(f)
                if isinstance(scene_data, dict) and 'name' in scene_data and 'key_sounds' in scene_data:
                    # 生成唯一的场景ID
                    scene_id = f"scene_{len(self.scenes)}"
                    while scene_id in self.scenes:
                        scene_id = f"scene_{int(scene_id.split('_')[1]) + 1}"
                    
                    self.scenes[scene_id] = scene_data
                    self.save_config()
                    return scene_id
                else:
                    messagebox.showerror("错误", "无效的场景文件格式")
        except Exception as e:
            messagebox.showerror("错误", f"导入场景失败: {str(e)}")
        return None 
    
    def export_config(self, filepath):
        """导出所有配置"""
        try:
            # 确保当前场景的按键绑定已保存
            self.scenes[self.current_scene]['key_sounds'] = self.key_sounds
            
            config = {
                'current_scene': self.current_scene,
                'scenes': self.scenes,
                'stop_key': self.stop_key,
                'stop_on_unbound': self.stop_on_unbound,
                'long_press_optimize': self.long_press_optimize
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            messagebox.showerror("错误", f"导出配置失败: {str(e)}")
            return False
    
    def import_config(self, filepath):
        """导入所有配置"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
                # 验证配置文件格式
                required_keys = ['current_scene', 'scenes', 'stop_key', 'stop_on_unbound', 'long_press_optimize']
                if not all(key in config for key in required_keys):
                    messagebox.showerror("错误", "无效的配置文件格式")
                    return False
                
                # 更新所有配置
                self.scenes = config['scenes']
                self.current_scene = config['current_scene']
                self.key_sounds = self.scenes[self.current_scene]['key_sounds']
                self.stop_key = config['stop_key']
                self.stop_on_unbound = config['stop_on_unbound']
                self.long_press_optimize = config['long_press_optimize']
                
                # 重新加载音频
                self.sounds.clear()
                self.load_sounds()
                
                # 保存配置
                self.save_config()
                return True
        except Exception as e:
            messagebox.showerror("错误", f"导入配置失败: {str(e)}")
            return False 