from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from utils import get_current_year, exit_system, about, open_logs, log_message, check_for_updates
from utils.alert_threading import information
import os
import tempfile

# Avoid Permission issues for multiple instances
os.environ['GST_REGISTRY'] = os.path.join(tempfile.gettempdir(), "registry.bin")

CURRENT_VERSION = "1.4"


class SettingsScreen(Screen):
    current_year = StringProperty()
    current_version = StringProperty(CURRENT_VERSION)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_year = f"© 2024-{get_current_year()} Pandora Dynamics. All Rights Reserved"
        self.exit_system = exit_system
        self.about = about
        self.open_logs = open_logs

    def check_for_updates(self):
        """Check for software updates"""
        log_message("INFO", "User initiated update check")
        check_for_updates(show_no_update=True)
    
    def view_license(self):
        """Display license information"""
        try:
            license_summary = (
                "PROPRIETARY SOFTWARE LICENSE\n\n"
                "Copyright (c) 2024-2026 RyanCantrell321, Pandora Dynamics.\n"
                "All Rights Reserved.\n\n"
                "This software is licensed for personal, non-commercial use only.\n\n"
                "You may NOT:\n"
                "• Modify, reverse engineer, or decompile the software\n"
                "• Distribute or transfer to third parties\n"
                "• Use for commercial purposes without permission\n\n"
                "THE SOFTWARE IS PROVIDED 'AS IS' WITHOUT WARRANTY.\n\n"
                "For full license terms, see LICENSE.md in the github repository.\n\n"
                "Contact: pandoradynamics@gmail.com"
            )
            information("Pandora qSHIELD - License", license_summary)
            log_message("INFO", "License viewed by user")
        except Exception as e:
            information("Error", f"Could not display license: {e}")
            log_message("ERROR", f"Failed to display license: {e}")
