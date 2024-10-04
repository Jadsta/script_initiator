import logging
import os
from datetime import datetime
from collections import deque

class CircularBufferFileHandler(logging.FileHandler):
    def __init__(self, filename, max_lines, mode='a', encoding=None, delay=False):
        super().__init__(filename, mode, encoding, delay)
        self.max_lines = max_lines
        self.buffer = deque(maxlen=max_lines)
        self._load_existing_lines()

    def _load_existing_lines(self):
        if os.path.exists(self.baseFilename):
            with open(self.baseFilename, 'r') as f:
                for line in f:
                    self.buffer.append(line.strip())

    def emit(self, record):
        log_entry = self.format(record)
        self.buffer.append(log_entry)
        with open(self.baseFilename, 'w') as f:
            for line in self.buffer:
                f.write(line + '\n')

    def handle_log(self, log_filename, log_dir, max_lines, log_message):
        # Ensure the log directory exists
        os.makedirs(log_dir, exist_ok=True)

        # Check if the filename already ends with .log
        if not log_filename.endswith('.log'):
            log_filename += '.log'

        # Construct the log file path
        log_file_path = os.path.join(log_dir, log_filename)

        # Update handler attributes
        self.baseFilename = log_file_path
        self.max_lines = max_lines
        self.buffer = deque(maxlen=max_lines)
        self._load_existing_lines()

        # Create a log record and emit it
        record = logging.LogRecord(name='', level=logging.INFO, pathname='', lineno=0, msg=log_message, args=(), exc_info=None)
        self.emit(record)

# Example usage
if __name__ == "__main__":
    # Configure logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create custom handler
    handler = CircularBufferFileHandler('default.log', 10, mode='a')
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)

    # Add handler to the logger
    logger.addHandler(handler)

    # Use the new method to handle logging
    handler.handle_log('my_log', '/path/to/logs', 20, 'This is a new log message')
