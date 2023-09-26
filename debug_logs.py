import logging
from configurations import get_logging_level

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    
    log_level = get_logging_level()  # Getting the logging level from configurations

    if log_level == "DEBUG":  # Check if the log level is set to DEBUG
        logger.setLevel(logging.DEBUG)
    elif log_level == "INFO":  # Check if the log level is set to INFO
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)  # Default to WARNING if none match
    
    logger.addHandler(handler)
    return logger

# Example Usage
if __name__ == "__main__":
    logger = setup_custom_logger('main')
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")