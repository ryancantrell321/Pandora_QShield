from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from times import get_current_year
from exit import exit_system
from about import about
from guides import guide
from view_logs import open_logs
import os
import tempfile

os.environ['GST_REGISTRY'] = os.path.join(tempfile.gettempdir(), "registry.bin")


class MainScreen(Screen):
    current_year = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_year = f"© {get_current_year()} Pandora Dynamics. All Rights Reserved"
        self.exit_system = exit_system
        self.about = about
        self.guide = guide
        self.open_logs = open_logs
