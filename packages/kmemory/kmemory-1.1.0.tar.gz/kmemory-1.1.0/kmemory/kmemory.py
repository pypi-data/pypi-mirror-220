import logging

# Create a logger for kmemory module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Configure the logger to write to a file
file_handler = logging.FileHandler('module_downloads.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def greet():
    logger.info("The greet() function from kmemory module has been called.")
    print("Hello, This Is Professor!")