"""Log formatter files."""
# Standard Library
import logging
from datetime import datetime


class CustomFormatter(logging.Formatter):  # noqa D101
    def format(self, record: logging.LogRecord) -> str:  # noqa D102
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f'{super().format(record)}[{timestamp}]'
