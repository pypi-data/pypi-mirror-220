import logging

# Create a logger for kmemory package
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Configure the logger to write to a file
file_handler = logging.FileHandler('module_downloads.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# Log a message when the kmemory package is imported
logger.info('The kmemory package has been imported.')

# __version__ attribute for the package
__version__ = '1.1.0'  # Update the version number to a higher value

# Import the greet function from kmemory.py to make it accessible from the package level
from .kmemory import greet
