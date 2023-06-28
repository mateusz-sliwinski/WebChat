import logging
from datetime import datetime

class CustomFormatter(logging.Formatter):
    def format(self, record):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f"{super().format(record)}[{timestamp}]"
