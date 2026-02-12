"""  
Pandora QShield
Version: 1.2
Author: Pandora Dynamics
Release: November 2024
Copyright: RyanCantrell321, Pandora Dynamics
License: Proprietary - All Rights Reserved
"""
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'minimum_width', '1000')
Config.set('graphics', 'minimum_height', '820')

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.text import LabelBase as LB
import os
import sys
import tempfile

# Import modules
from screens import MainScreen, BackupScreen, RestoreScreen, SettingsScreen
from utils import log_message, acquire_lock, release_lock, start_cleaner, fatal_error, get_ui_path, get_asset_path

# Avoid Permission issues for multiple instances
os.environ['GST_REGISTRY'] = os.path.join(tempfile.gettempdir(), "registry.bin")
log_message("INFO", "Pandora QShield Initialized")

# Start initializing instance locker
lock_fd = acquire_lock()

# Memory cleaner
start_cleaner()

try:
    # Load emoji font
    LB.register(name="EmojiFont", fn_regular="C:/Windows/Fonts/seguiemj.ttf")
    
    # Register custom fonts
    LB.register(name="Montserrat-Bold.ttf", fn_regular=get_asset_path("Montserrat-Bold.ttf"))
    LB.register(name="Montserrat-Medium.ttf", fn_regular=get_asset_path("Montserrat-Medium.ttf"))
    LB.register(name="Montserrat-Regular.ttf", fn_regular=get_asset_path("Montserrat-Regular.ttf"))
    
    # Load .kv design files
    Builder.load_file(get_ui_path("main_screen.kv"))
    Builder.load_file(get_ui_path("backup_screen.kv"))
    Builder.load_file(get_ui_path("restore_screen.kv"))
    Builder.load_file(get_ui_path("settings_screen.kv"))

    # Execute Software
    class QShield(App):
        def build(self):
            self.title = "Pandora QShield"
            self.icon = get_asset_path("qbittorrent.png")

            log_message("INFO", "Maximizing window")
            Window.maximize()

            # Screen Manager Algorithm
            sm = ScreenManager(transition=FadeTransition())

            sm.add_widget(MainScreen(name="main"))
            log_message("INFO", "Main Screen Loaded")
            
            sm.add_widget(BackupScreen(name="backup"))
            log_message("INFO", "Backup QBittorrent Data Screen Loaded")
            
            sm.add_widget(RestoreScreen(name="restore"))
            log_message("INFO", "Restore QBittorrent Data Screen Loaded")
            
            sm.add_widget(SettingsScreen(name="settings"))
            log_message("INFO", "Settings Screen Loaded")

            return sm

        def minimize_window(self):
            Window.minimize()
            log_message("INFO", "Minimizing window")

    if __name__ == "__main__":
        QShield().run()

except Exception as e:
    log_message("CRITICAL", f"""Error: {e}""")
    fatal_error(e)
    print(f"Error: {e}")

# Instance locked to 1 operational instance only
release_lock(lock_fd)
