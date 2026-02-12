import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

try:
    # Get Windows Documents folder
    documents_folder = os.path.join(os.path.expanduser("~"), "Documents")
    log_directory = os.path.join(documents_folder, "QShield Logs")
    os.makedirs(log_directory, exist_ok=True)

    # Log file path
    LOG_FILE = os.path.join(log_directory, "events.log")

    # Setting up the logger
    logger = logging.getLogger("QShield Logger")
    logger.setLevel(logging.DEBUG)
    # Create a rotating file handler that logs to a file with max size of 1MB and keeps 3 backup files
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1*1024*1024, backupCount=3)
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler to also output logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Create a formatter and set it for the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    def log_message(level, message):
        if level == "DEBUG":
            logger.debug(message)
        elif level == "INFO":
            logger.info(message)
        elif level == "WARNING":
            logger.warning(message)
        elif level == "ERROR":
            logger.error(message)
        elif level == "CRITICAL":
            logger.critical(message)

    # Example usage
    if __name__ == "__main__":
        log_message("INFO", "This is an info message")
        log_message("ERROR", "This is an error message")

except Exception as e:
    print(f"Error: {e}")
