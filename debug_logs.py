#debug_logs.py
import logging
import sys

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    handler = logging.StreamHandler(sys.stdout)  # Aqui você usa sys.stdout
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger

log = setup_custom_logger('my_logger')

# Example Usage
if __name__ == "__main__":
    logger = setup_custom_logger('main')
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

