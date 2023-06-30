import logging
from datetime import datetime


class CustomFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f"{super().format(record)}[{timestamp}]"
