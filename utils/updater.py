import requests
import os
import subprocess
import sys
from threading import Thread
from .logger import log_message
from .alert_threading import warning, information, error
from kivy.clock import mainthread

# Update configuration
GITHUB_REPO = "ryancantrell321/Pandora_QShield"  
CURRENT_VERSION = "1.2"  # Must match version in settingsscreen.py
UPDATE_CHECK_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"


def get_latest_version():
    """Fetch latest version from GitHub releases"""
    try:
        log_message("INFO", f"Checking GitHub API: {UPDATE_CHECK_URL}")
        response = requests.get(UPDATE_CHECK_URL, timeout=10)
        log_message("INFO", f"GitHub API response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            latest_version = data.get("tag_name", "").replace("v", "")
            download_url = None
            
            # Find the correct asset for this resolution
            for asset in data.get("assets", []):
                if "Pandora_qSHIELD.exe" in asset["name"]:
                    download_url = asset["browser_download_url"]
                    break
            
            return latest_version, download_url, data.get("body", "")
        elif response.status_code == 404:
            log_message("WARNING", "No releases found for this repository")
            return None, None, None
        else:
            log_message("WARNING", f"Failed to check for updates: HTTP {response.status_code}")
            return None, None, None
    except requests.exceptions.RequestException as e:
        log_message("ERROR", f"Network error during update check: {e}")
        return None, None, None
    except Exception as e:
        log_message("ERROR", f"Update check failed: {e}")
        return None, None, None


def compare_versions(current, latest):
    """Compare version strings (e.g., '1.1' vs '1.2')"""
    try:
        current_parts = [int(x) for x in current.split('.')]
        latest_parts = [int(x) for x in latest.split('.')]
        
        # Pad shorter version with zeros
        max_len = max(len(current_parts), len(latest_parts))
        current_parts += [0] * (max_len - len(current_parts))
        latest_parts += [0] * (max_len - len(latest_parts))
        
        return latest_parts > current_parts
    except:
        return False


def download_update(download_url, progress_callback=None):
    """Download update file"""
    try:
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        filename = f"Pandora_qSHIELD_Update.exe"
        filepath = os.path.join(downloads_folder, filename)
        
        log_message("INFO", f"Downloading update from: {download_url}")
        
        response = requests.get(download_url, stream=True, timeout=30)
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback and total_size > 0:
                        progress = int((downloaded / total_size) * 100)
                        progress_callback(progress)
        
        log_message("INFO", f"Update downloaded to: {filepath}")
        return filepath
    except Exception as e:
        log_message("ERROR", f"Download failed: {e}")
        return None


@mainthread
def show_update_prompt(latest_version, download_url, release_notes):
    """Show update available prompt"""
    from tkinter import messagebox
    import tkinter as tk
    
    root = tk.Tk()
    root.withdraw()
    
    message = f"A new version ({latest_version}) is available!\n\n"
    message += f"Current version: {CURRENT_VERSION}\n\n"
    if release_notes:
        message += f"Release Notes:\n{release_notes[:200]}...\n\n"
    message += "Would you like to download the update now?"
    
    result = messagebox.askyesno("Update Available", message)
    root.destroy()
    
    if result:
        download_and_install(download_url, latest_version)


def download_and_install(download_url, version):
    """Download update and prompt for installation"""
    def download_thread():
        information("Downloading Update", f"Downloading version {version}...\nThis may take a few moments.")
        
        filepath = download_update(download_url)
        
        if filepath and os.path.exists(filepath):
            show_install_prompt(filepath, version)
        else:
            error("Download Failed", "Failed to download the update. Please try again later.")
    
    Thread(target=download_thread, daemon=True).start()


@mainthread
def show_install_prompt(filepath, version):
    """Prompt user to install downloaded update"""
    from tkinter import messagebox
    import tkinter as tk
    
    root = tk.Tk()
    root.withdraw()
    
    message = f"Update downloaded successfully!\n\n"
    message += f"Location: {filepath}\n\n"
    message += "The application will now close.\n"
    message += "Please run the new executable to complete the update."
    
    messagebox.showinfo("Update Ready", message)
    root.destroy()
    
    # Open downloads folder
    downloads_folder = os.path.dirname(filepath)
    os.startfile(downloads_folder)
    
    # Exit application
    log_message("INFO", "Exiting for update installation")
    from kivy.app import App
    App.get_running_app().stop()


def check_for_updates(show_no_update=True):
    """Main update check function"""
    def check_thread():
        log_message("INFO", "Checking for updates...")
        
        latest_version, download_url, release_notes = get_latest_version()
        
        if latest_version and download_url:
            if compare_versions(CURRENT_VERSION, latest_version):
                log_message("INFO", f"Update available: {latest_version}")
                show_update_prompt(latest_version, download_url, release_notes)
            else:
                log_message("INFO", "No updates available")
                if show_no_update:
                    information("No Updates", f"You are running the latest version ({CURRENT_VERSION})")
        else:
            log_message("WARNING", "Update check returned no data")
            if show_no_update:
                warning("Update Check Failed", f"Unable to check for updates.\n\nPossible reasons:\n- No releases published on GitHub\n- Repository not found\n- Network connection issue\n\nRepository: {GITHUB_REPO}")
    
    Thread(target=check_thread, daemon=True).start()
