from alert_threading import information, error
from text import text2, text3, text4
from logger import log_message

try:
    def guide():
        information("Usage Guide", f"""{text2}""")
        log_message("INFO", "Usage Guide Opened")

except Exception as e:
    log_message("ERROR", f"Failed to open usage guide: {e}")
    error("Error", f"Failed to open usage guide: {e}")


try:
    def backup_guide():
        information("Backup Guide", f"""{text3}""")
        log_message("INFO", "Backup Guide Opened")

except Exception as e:
    log_message("ERROR", f"Failed to backup guide: {e}")
    error("Error", f"Failed to open backup guide: {e}")


try:
    def restore_guide():
        information("Restore Guide", f"""{text4}""")
        log_message("INFO", "Restore Guide Opened")

except Exception as e:
    log_message("ERROR", f"Failed to open restore guide: {e}")
    error("Error", f"Failed to open restore guide: {e}")




