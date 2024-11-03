"""
Pandora QShield
Version: 1.1
Author: Pandora Dynamics
Release: November 2024
Copyright: RyanCantrell321, Pandora Dynamics | UI Advisor: Shad0wW0rri0r
License: GNU General Public License (GPL) v3.0
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from mainscreen import MainScreen
from alert_codes import fatal_error
from instance_lock_mechanism import acquire_lock, release_lock
from backupscreen import BackupScreen
from memory_cleaner import start_cleaner
from restorescreen import RestoreScreen
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from logger import log_message
import os
import tempfile

os.environ['GST_REGISTRY'] = os.path.join(tempfile.gettempdir(), "registry.bin")
log_message("INFO", "Pandora QShield Initialized")

# start initializing instance locker
lock_fd = acquire_lock()
# finish initializing instance locker

# memory cleaner
start_cleaner()

try:

    # Load .kv design files
    # Builder.load_file("custom_titlebar.kv")
    Builder.load_file("main_screen.kv")
    Builder.load_file("backup_screen.kv")
    Builder.load_file("restore_screen.kv")

    # Execute Software
    class QShield(App):
        def build(self):
            self.title = "Pandora QShield"
            self.icon = "qbittorrent.png"

            log_message("INFO", "Maximizing window")
            Window.maximize()

            # Screen Manager Algorithm
            sm = ScreenManager(transition=FadeTransition())

            if sm.add_widget(MainScreen(name="main")):
                log_message("INFO", "Main Screen Loaded")
            elif sm.add_widget(BackupScreen(name="backup")):
                log_message("INFO", "Backup QBittorrent Data Screen Loaded")
            elif sm.add_widget(RestoreScreen(name="restore")):
                log_message("INFO", "Restore QBittorrent Data Screen Loaded")

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

# instance locked to 1 operational instance only
release_lock(lock_fd)
