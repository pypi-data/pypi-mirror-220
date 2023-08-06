"""
Logging filters for use with the Python logging module.
RelativeTimeFilter - A logging filter that adds a relative time to the log record.
DiffTimeFilter - A logging filter that adds a time difference to the log record.
"""
from __future__ import annotations

import logging
from datetime import datetime


class RelativeTimeFilter(logging.Filter):
    """
    Abuse of a logging filter to augment the logged record with timings relative
    to a settable point.

    For a justification of this abuse see:
       https://docs.python.org/3/howto/logging-cookbook.html#filters-contextual
    """

    def __init__(self, *args, **kwargs):  # type: ignore
        super().__init__(*args, **kwargs)
        # Set the time reference to now when the filter is created.
        self.time_reference = datetime.now()

    def filter(self, record: logging.LogRecord) -> bool:
        now = datetime.now()

        if not self.time_reference:
            self.time_reference = now

        record.reltime = now - self.time_reference

        return True

    def reset_time_reference(self) -> None:
        """
        Update the time reference to now.
        """
        self.time_reference = datetime.now()


class DiffTimeFilter(logging.Filter):
    """
    Abuse of a logging filter to augment the logged record with relative timing data.

    For a justification of this abuse see:
       https://docs.python.org/3/howto/logging-cookbook.html#filters-contextual
    """
    last_time = None

    def filter(self, record: logging.LogRecord) -> bool:
        now = datetime.now()

        if not self.last_time:
            self.last_time = now

        record.difftime = now - self.last_time

        self.last_time = now

        return True
