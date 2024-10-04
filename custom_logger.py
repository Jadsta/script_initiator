import logging
import os
from datetime import datetime
from collections import deque

class CircularBufferFileHandler(logging.FileHandler):
    def __init__(self, log_filename, log_dir, max_lines, mode='a', encoding=None, delay=False):
        # Ensure the log directory exists
        os.makedirs(log_dir, exist_ok=True)

        # Check if the filename already ends with .log
        if not log_filename.endswith('.log'):
            log_filename += '.log'

        # Construct the log file path
        log_file_path = os.path.join(log_dir, log_filename)

        super().__init__(log_file_path, mode, encoding, delay)
        self.max_lines = max_lines
        self.buffer = deque(maxlen=max_lines)
        self._load_existing_lines()

        # Set up the formatter
        formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.setFormatter(formatter)

        # Add the handler to the logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(self)

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

    def handle_log(self, log_message):
        # Create a log record and emit it
        record = logging.LogRecord(name='', level=logging.INFO, pathname='', lineno=0, msg=log_message, args=(), exc_info=None)
        self.emit(record)

# Example usage
if __name__ == "__main__":
    # Create custom handler
    #handler = CircularBufferFileHandler('my_log', '/path/to/logs', 20)

    # Use the handle_log method
    #handler.handle_log('This is a new log message from another script')
