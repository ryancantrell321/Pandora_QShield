from threading import Thread
from kivy.clock import mainthread
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from exit import exit_system
from guides import restore_guide
from view_logs import open_logs
from logger import log_message
from times import get_current_year
from alert_threading import warning
from file_management_threading import select_restore_location, restore_data
import os
import tempfile

os.environ['GST_REGISTRY'] = os.path.join(tempfile.gettempdir(), "registry.bin")


class RestoreScreen(Screen):
    current_year = StringProperty()
    selected_restore_file = StringProperty("")
    progress = NumericProperty(0)
    restore_in_progress = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_year = f"© {get_current_year()} Pandora Dynamics. All Rights Reserved"
        self.exit_system = exit_system
        self.open_logs = open_logs
        self.restore_guide = restore_guide

    @mainthread
    def select_restore_location(self):
        select_restore_location(self.update_restore_location)
        log_message("INFO", "Selecting Restore Location")

    def restore_data(self):
        if self.restore_in_progress:
            warning("Restore in Progress", "A restore operation is already in progress. Please wait until it finishes.")
            return

        restore_file = self.selected_restore_file
        restore_location = os.path.join(os.getenv("LOCALAPPDATA"), "qBittorrent")

        if restore_file != "Selected Restore File":
            self.restore_in_progress = True

            def run_restore():
                try:
                    restore_data(restore_file, restore_location, self.update_progress)
                finally:
                    self.restore_in_progress = False

            Thread(target=run_restore).start()
        else:
            warning("Restore Error", "No restore file selected")
            log_message("ERROR", "No restore file selected")

    def update_restore_location(self, location):
        self.selected_restore_file = location

    @mainthread
    def update_progress(self, progress):
        self.progress = progress
        if progress == 100:
            log_message("INFO", "Restore completed successfully")
