from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from utils import get_current_year, exit_system, about, open_logs, log_message, check_for_updates
import os
import tempfile

os.environ['GST_REGISTRY'] = os.path.join(tempfile.gettempdir(), "registry.bin")

CURRENT_VERSION = "1.2"


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
        log_message("INFO", "User initiated update check")
        check_for_updates(show_no_update=True)
