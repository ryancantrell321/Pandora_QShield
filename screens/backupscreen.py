from threading import Thread
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import mainthread
from utils import exit_system, open_logs, backup_guide, log_message, get_current_year, warning
from utils.file_management_threading import select_backup_location, backup_data
import os
from datetime import datetime
import tempfile

# Avoid Permission issues for multiple instances
os.environ['GST_REGISTRY'] = os.path.join(tempfile.gettempdir(), "registry.bin")


class BackupScreen(Screen):
    current_year = StringProperty()
    selected_backup_location = StringProperty("")
    progress = NumericProperty(0)
    backup_in_progress = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_year = f"© {get_current_year()} Pandora Dynamics. All Rights Reserved"
        self.exit_system = exit_system
        self.open_logs = open_logs
        self.backup_guide = backup_guide

    @mainthread
    def on_select_backup_location(self):
        select_backup_location(self.update_backup_location)
        log_message("INFO", "Selecting backup location")

    def backup_data(self):

        if self.backup_in_progress:
            warning("Backup in Progress", "A backup operation is already in progress. Please wait until it finishes.")
            return

        self.backup_in_progress = True
        backup_location = self.selected_backup_location

        if not backup_location or backup_location == "Selected Backup Location":
            backup_location = os.path.join(os.path.expanduser("~"), "Downloads")
            self.update_backup_location(backup_location)
            warning("Backup", "Backup location not selected, using default location.")
            log_message("Backup", "Backup location not selected, using default location")
        backup_date = datetime.now().strftime("%Y%m%d%H%M%S")

        def run_backup():
            try:
                backup_data(backup_location, backup_date, self.update_progress)
            finally:
                self.backup_in_progress = False

        Thread(target=run_backup).start()


    @mainthread
    def update_backup_location(self, location):
        self.selected_backup_location = location

    @mainthread
    def update_progress(self, progress):
        self.progress = progress
        if progress == 100:
            log_message("Backup", "Backup completed successfully")