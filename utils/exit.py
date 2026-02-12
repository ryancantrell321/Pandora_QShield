from .logger import log_message
from .alert_threading import leave

try:
    def exit_system():
        leave("Exit?", "Are you sure you want to exit Pandora QShield?")
        log_message("INFO", "Exiting Pandora QShield...")


except Exception as e:
    log_message("CRITICAL", f"""Error: {e}""")
    print(f"Error: {e}")

