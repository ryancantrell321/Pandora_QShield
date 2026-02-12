import tkinter as tk
from tkinter import messagebox
from kivy.app import App
from kivy.clock import Clock, mainthread
from .logger import log_message
import sys

# Error Threading
try:
    def error(title, message):
        @mainthread
        def show_message(dt):
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(title, message)
            root.destroy()

        Clock.schedule_once(show_message, 0)
        log_message("INFO", "Error Threading between Dependencies Initialized")

except Exception as e:
    log_message("ERROR", f"Failed to initialize Error Threading between Dependencies: {e}")


# Information Box Threading
try:
    def information(title, message):
        @mainthread
        def show_message(dt):
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo(title, message)
            root.destroy()

        Clock.schedule_once(show_message, 0)
        log_message("INFO", "Information Threading between Dependencies Initialized")
except Exception as e:
    log_message("ERROR", f"Failed to initialize Information Threading between Dependencies: {e}")


# Warning Box Threading
try:
    def warning(title, message):
        @mainthread
        def show_message(dt):
            root = tk.Tk()
            root.withdraw()
            messagebox.showwarning(title, message)
            root.destroy()

        Clock.schedule_once(show_message, 0)
        log_message("INFO", "Warning Threading between Dependencies Initialized")

except Exception as e:
    log_message("ERROR", f"Failed to initialize Warning Threading between Dependencies: {e}")


# Exit Prompt Threading:
try:
    def leave(title, message):
        @mainthread
        def show_message(dt):
            root = tk.Tk()
            root.withdraw()
            prompt = messagebox.askyesno(title, message)

            if prompt:
                App.get_running_app().stop()

            root.destroy()

        Clock.schedule_once(show_message, 0)
        log_message("INFO", "Exit Threading between Dependencies Initialized")

except Exception as e:
    log_message("ERROR", f"Failed to initialize Exit Threading between Dependencies: {e}")

