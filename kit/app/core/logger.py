import logging
from logging.handlers import RotatingFileHandler
import sys

def setup_logger(name: str, log_file: str, level=logging.DEBUG):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s: %(message)s')

    # File handler
    file_handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5)  # 10MB per file, keep 5 old files
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger