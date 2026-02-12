import os
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def get_asset_path(filename):
    """Get path to asset file"""
    return resource_path(os.path.join("assets", filename))

def get_ui_path(filename):
    """Get path to UI file"""
    return resource_path(os.path.join("ui", filename))
