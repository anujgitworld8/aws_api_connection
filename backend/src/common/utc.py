import logging
from datetime import datetime, timezone

class UTCFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        # Format the time in UTC
        timestamp = datetime.now(timezone.utc)
        datetime_str = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
        return datetime_str
