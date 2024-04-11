import logging
import os

from pathlib import Path
from datetime import datetime

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.log_file_path = None
            cls._instance.logger = None
            cls._instance.init_logger()
        return cls._instance

    def info(self, param):
        self.logger.info(param)

    def error(self, param):
        self.logger.error(param)

    def init_logger(self):
        # Create logs directory if it doesn't exist
        #project_dir = Path(__file__).resolve().parent.parent.parent
        project_dir = Path(os.getcwd())
        logs_dir = project_dir.parent / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)

        # Configure logger
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s -|- %(message)s')

        # Include current timestamp in the log file name
        current_timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
        self.log_file_path = logs_dir / f'{current_timestamp}.log'

        # Create a file handler for the logger
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(logging.INFO)

        # Create a formatter and set it for the file handler
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger = logging.getLogger(__name__)
        logger.addHandler(file_handler)

        # Disable propagation to the root logger
        logger.propagate = False

        self.logger = logger

    def get_log_file_path(self):
        return os.path.abspath(self.log_file_path)

    def close(self):
        # Perform any cleanup or resource release here
        for handler in self.logger.handlers:
            if isinstance(handler, logging.FileHandler):
                handler.close()

# Initialize logger
logger = Logger()