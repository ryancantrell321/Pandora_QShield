from .text import text1
from .alert_threading import information, error
from .logger import log_message

try:
    def about():
        information("About", f"""{text1}""")
        log_message("INFO", "About button pressed")

except Exception as e:
    log_message("ERROR", f"Failed to open about: {e}")
    error("Error", f"Failed to open about: {e}")
    print(f"Error: {e}")
