from tkinter import messagebox
import sys


def fatal_error(message):
    messagebox.showerror("Fatal Error!", f"""The program has encountered a fatal error!\n\nDetails:\n{message}""")
    sys.exit(0)


