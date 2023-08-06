"""
A collection of logging formatters, including:
TieredFormatter - A logging formatter that allows for different formats based on the log level.
"""
from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any


class TieredFormatter(logging.Formatter):
    """
    A logging formatter that allows for different formats based on the log level.

    For example, you can use this to have DEBUG and INFO messages use a
    format that includes the relative time since the first message, while
    WARNING and above messages use a format that does not include the
    relative time.

    :param fmt: The default format string for the formatter.
    :param level_fmts: A mapping of log levels to format strings.
    :param args: Additional positional arguments to pass to the logging.Formatter constructor.
    :param kwargs: Additional keyword arguments to pass to the logging.Formatter constructor.
    :return: A logging formatter.
    """
    def __init__(
        self,
        fmt: str | None = None,
        level_fmts: Mapping[int, str] | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(fmt, *args, **kwargs)

        self.level_fmts = level_fmts or {}

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified record as text, using the level-specific format if available.

        :param record: The record to be formatted.
        :return: The formatted record.
        """

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._fmt

        try:
            # Replace the original format with one customized by logging level
            self._style._fmt = self.level_fmts.get(record.levelno, self._fmt or "")

            # Call the original format command to do the grunt work
            result = super().format(record)
        finally:
            # Restore the original format configured by the user
            self._fmt = format_orig

        return result
