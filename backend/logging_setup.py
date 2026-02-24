import logging

def setup_logger(name, log_file = 'server.log', level = logging.DEBUG ):
    logger = logging.getLogger(name) 

    logger.setLevel(level)  # Set minimum level
    file_handler = logging.FileHandler(log_file)  # Where to save
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  #Format
    file_handler.setFormatter(formatter)  # Apply format
    logger.addHandler(file_handler)  # Attach handler

    return logger



