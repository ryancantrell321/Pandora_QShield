import os
from logger import log_message
from alert_threading import error


def open_logs(file_path):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "..", "qShield Event Logs", "events.docx")
        os.startfile(file_path)
        log_message("INFO", f"Opening file: {file_path}")

    except Exception as e:
        log_message("ERROR", f"Failed to open file: {e}")
        error("Error", f"Failed to open file: {e}")
        print(f"Error: {e}")


# Example usage
if __name__ == "__main__":
    file_to_open = "Logs/events.docx"
    open_logs(file_to_open)
