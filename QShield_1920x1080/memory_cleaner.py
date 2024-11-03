import gc
import psutil
import time
import threading
from logger import log_message


def memory_cleaner():
    """Function to free up memory by calling garbage collection."""
    try:
        while True:
            gc.collect()
            memory_info = psutil.virtual_memory()
            print("INFO", f"Memory cleaned. Current usage: {memory_info.percent}%")
            time.sleep(5)
    except Exception as e:
        log_message("CRITICAL", f"Memory cleaner error: {e}")


def start_cleaner():
    """Starts the memory cleaner in a separate thread."""
    cleaner_thread = threading.Thread(target=memory_cleaner, daemon=True)
    cleaner_thread.start()
    return cleaner_thread
