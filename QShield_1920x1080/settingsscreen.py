from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from times import get_current_year
from exit import exit_system
from about import about
from view_logs import open_logs
from logger import log_message
from alert_threading import warning
import os
import tempfile

os.environ['GST_REGISTRY'] = os.path.join(tempfile.gettempdir(), "registry.bin")

CURRENT_VERSION = "1.1"


class SettingsScreen(Screen):
    current_year = StringProperty()
    current_version = StringProperty(CURRENT_VERSION)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_year = f"© {get_current_year()} Pandora Dynamics. All Rights Reserved"
        self.exit_system = exit_system
        self.about = about
        self.open_logs = open_logs

    def check_for_updates(self):
        """Check for software updates"""
        log_message("INFO", "Checking for updates...")
        warning("Update Check", "Update feature coming soon! Check GitHub for latest releases.")
