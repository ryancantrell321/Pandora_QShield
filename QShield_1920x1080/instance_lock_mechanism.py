from alert_threading import error
import os
import sys
import portalocker
from logger import log_message

try:
    def acquire_lock():
        lock_file = os.path.join(os.path.dirname(sys.argv[0]), "instance_lock.qshield")

        try:
            lock_fd = open(lock_file, "w")
            portalocker.lock(lock_fd, portalocker.LOCK_EX | portalocker.LOCK_NB)
            print("Acquired lock on the instance lock file.")
            log_message("INFO", "Acquired lock on the instance")
            return lock_fd
        except portalocker.LockException:
            error("Error", "Another instance of QShield is already running! Exiting.")
            print("Another instance of QShield is already running! Exiting.")
            log_message("ERROR", "Another instance of QShield is already running! Exiting.")
            sys.exit(1)


    def release_lock(lock_fd):
        portalocker.unlock(lock_fd)
        lock_fd.close()
        os.unlink(os.path.join(os.path.dirname(sys.argv[0]), "instance_lock.qshield"))
        print("Released lock on the instance lock file.")
        log_message("INFO", "Released lock on the instance")

except Exception as e:
    log_message("CRITICAL", f"""Error: {e}""")
    print(f"Error: {e}")

# # Example usage:
# lock_fd = acquire_lock()
# release_lock(lock_fd)
