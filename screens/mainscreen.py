from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from utils import get_current_year, exit_system, about, open_logs
from utils.guides import guide
import os
import tempfile

# Avoid Permission issues for multiple instances
os.environ['GST_REGISTRY'] = os.path.join(tempfile.gettempdir(), "registry.bin")


class MainScreen(Screen):
    current_year = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_year = f"© 2024-{get_current_year()} Pandora Dynamics. All Rights Reserved"
        self.exit_system = exit_system
        self.about = about
        self.guide = guide
        self.open_logs = open_logs
