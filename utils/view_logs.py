import os
from .logger import log_message
from .alert_threading import error


def open_logs():
    try:
        documents_folder = os.path.join(os.path.expanduser("~"), "Documents")
        log_directory = os.path.join(documents_folder, "QShield Logs")
        file_path = os.path.join(log_directory, "events.log")
        os.startfile(file_path)
        log_message("INFO", f"Opening file: {file_path}")

    except Exception as e:
        log_message("ERROR", f"Failed to open file: {e}")
        error("Error", f"Failed to open file: {e}")
        print(f"Error: {e}")


# Example usage
if __name__ == "__main__":
    open_logs()
