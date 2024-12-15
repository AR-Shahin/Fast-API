import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime


# Create a logger
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

# Set up console handler for logging to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Log all messages to the console
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Set up timed rotating file handler for daily log rotation
# Use current working directory (where main.py is executed) to create the log directory
log_dir = os.path.join(os.getcwd(), 'logs')  # Logs directory will be created in the current working directory
os.makedirs(log_dir, exist_ok=True)

# Use a static log file name and let TimedRotatingFileHandler manage rotation
log_filename = 'app.log'  # Static log file name
log_file = os.path.join(log_dir, log_filename)

# Create the TimedRotatingFileHandler to rotate logs every day at midnight
file_handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=7)
file_handler.setLevel(logging.DEBUG)  # Log all messages to the file (DEBUG and above)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

