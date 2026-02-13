import threading
import os
import shutil
import zipfile
from tkinter import filedialog
from kivy.clock import mainthread
from .logger import log_message
from .alert_threading import information, error, warning
import tkinter as tk


@mainthread
def select_backup_location(callback):
    def thread_function():
        root = tk.Tk()
        root.withdraw()
        location = filedialog.askdirectory()
        root.destroy()
        if location:
            callback(location)
        else:
            warning("Backup Location", "No backup location selected.")

    threading.Thread(target=thread_function).start()


def backup_data(backup_location, backup_date, progress_callback):
    try:
        localappdata_path = os.path.join(os.getenv("LOCALAPPDATA"), "qBittorrent")
        appdata_path = os.path.join(os.getenv("APPDATA"), "qBittorrent")

        backup_dir = os.path.join(backup_location, f"qSHIELD_Qbt_Backup_{backup_date}")
        os.makedirs(backup_dir, exist_ok=True)

        localappdata_backup = os.path.join(backup_dir, "localappdata")
        appdata_backup = os.path.join(backup_dir, "appdata")

        # Manual copy function that skips locked files
        def copy_tree_safe(src, dst):
            """Copy directory tree, skipping files that can't be accessed"""
            os.makedirs(dst, exist_ok=True)
            for item in os.listdir(src):
                src_path = os.path.join(src, item)
                dst_path = os.path.join(dst, item)
                try:
                    if os.path.isdir(src_path):
                        copy_tree_safe(src_path, dst_path)
                    else:
                        shutil.copy2(src_path, dst_path)
                except (PermissionError, OSError) as e:
                    log_message("WARNING", f"Skipping file due to access error: {src_path} - {e}")
                    continue

        copy_tree_safe(localappdata_path, localappdata_backup)
        copy_tree_safe(appdata_path, appdata_backup)

        zip_path = os.path.join(backup_location, f"qSHIELD_Qbt_Backup_{backup_date}.zip")
        with zipfile.ZipFile(zip_path, "w") as backup_zip:
            total_files = sum([len(files) for _, _, files in os.walk(backup_dir)])
            processed_files = 0

            for folder_name, subfolders, filenames in os.walk(backup_dir):
                for filename in filenames:
                    file_path = os.path.join(folder_name, filename)
                    try:
                        backup_zip.write(file_path, os.path.relpath(file_path, backup_dir))
                    except (PermissionError, OSError) as e:
                        log_message("WARNING", f"Skipping file in zip: {file_path} - {e}")
                    processed_files += 1
                    progress = (processed_files / total_files) * 100
                    progress_callback(progress)

        shutil.rmtree(backup_dir)
        information("Backup Complete", f"Backup completed successfully: {zip_path}")
        log_message("INFO", f"Backup completed successfully: {zip_path}")

    except Exception as e:
        error("Failed to Backup Data", f"Failed to backup data: {e}")
        raise


@mainthread
def select_restore_location(update_location_callback):
    try:
        selected_file = filedialog.askopenfilename(filetypes=[("Zip Files", "*.zip")])
        if selected_file:
            update_location_callback(selected_file)
            log_message("INFO", f"Selected restore file: {selected_file}")
        else:
            log_message("INFO", "No restore file selected")
    except Exception as e:
        error("Restore Location Error", f"Failed to select restore file: {e}")
        log_message("ERROR", f"Failed to select restore file: {e}")


def restore_data(restore_file, restore_location, progress_callback):
    try:

        if not os.path.basename(restore_file).startswith("qSHIELD_Qbt_Backup"):
            error("Invalid File", "Selected file is not a valid qSHIELD backup file.")
            log_message("ERROR", "Attempted restore with an invalid file.")
            return

        if not os.path.exists(restore_location):
            os.makedirs(restore_location)

        if os.listdir(restore_location):
            for root, dirs, files in os.walk(restore_location):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    shutil.rmtree(os.path.join(root, dir))

        with zipfile.ZipFile(restore_file, "r") as zip_ref:
            total_files = len(zip_ref.namelist())
            processed_files = 0

            for file in zip_ref.namelist():
                zip_ref.extract(file, restore_location)
                processed_files += 1
                progress = (processed_files / total_files) * 100
                progress_callback(progress)

        # Copy restored data back to the appropriate directories
        localappdata_restore = os.path.join(restore_location, "localappdata")
        appdata_restore = os.path.join(restore_location, "appdata")

        shutil.copytree(localappdata_restore, os.path.join(os.getenv("LOCALAPPDATA"), "qBittorrent"), dirs_exist_ok=True)
        shutil.copytree(appdata_restore, os.path.join(os.getenv("APPDATA"), "qBittorrent"), dirs_exist_ok=True)

        information("Success!", f"Restore Successful!\n\nFile {restore_file} restored to {localappdata_restore} and {appdata_restore}")
        log_message("INFO", f"Restore Successful for file {restore_file} at {localappdata_restore} and {appdata_restore}")

    except Exception as e:
        error("Restore Error", f"Failed to restore data: {e}")
        log_message("ERROR", f"Failed to restore data: {e}")
