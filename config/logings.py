import logging
import os

def initialize_logging(log_file='my_log.log', log_level=logging.INFO):
    # Split the log_file path into directory and file name
    log_directory, log_filename = os.path.split(log_file)

    # Create the log directory if it doesn't exist
    if log_directory and not os.path.exists(log_directory):
        os.makedirs(log_directory)

    logging.basicConfig(level=log_level, filename=log_file, filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    return logger