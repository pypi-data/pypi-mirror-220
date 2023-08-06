import logging
from time import sleep

import pytest

import logger_extras


def test_log_function_call(caplog):
    """
    Test that the log_function_call decorator logs the function call and return value.

    Test the level of the log messages can be set and the functions module is
    used as the logger name.
    """
    @logger_extras.log_function_call(level=logging.INFO)
    def func(a, b, c=1, d=2):
        return a + b + c + d

    caplog.set_level(logging.INFO)

    _ = func(1, 2, d=3)

    assert caplog.record_tuples == [
        (
            "test_tools",
            logging.INFO,
            "Calling test_log_function_call.<locals>.func(1, 2, d=3)",
        ),
        (
            "test_tools",
            logging.INFO,
            "'test_log_function_call.<locals>.func' returned 7",
        ),
    ]


def test_log_function_call_fixed_fixed_logger(caplog):
    """
    Test that the log_function_call decorator logs to a fixed logger.
    """
    logger = logging.getLogger("test_tools_custom")
    logger.setLevel(logging.DEBUG)

    @logger_extras.log_function_call(fixed_logger=logger)
    def func(a, b, c=1, d=2):
        return a + b + c + d

    caplog.set_level(logging.DEBUG)

    _ = func(1, 2, d=3)

    assert caplog.record_tuples == [
        (
            "test_tools_custom",
            logging.DEBUG,
            "Calling test_log_function_call_fixed_fixed_logger.<locals>.func(1, 2, d=3)",
        ),
        (
            "test_tools_custom",
            logging.DEBUG,
            "'test_log_function_call_fixed_fixed_logger.<locals>.func' returned 7",
        ),
    ]


def test_relative_time_filter(caplog):
    """
    Test that the RelativeTimeFilter adds the relative time to the log record.
    """
    logger = logging.getLogger("test_tools_custom")
    logger.setLevel(logging.DEBUG)

    time_filter = logger_extras.RelativeTimeFilter()
    logger.addFilter(time_filter)

    caplog.set_level(logging.DEBUG)

    logger.debug("Test message 1")

    sleep(1)

    logger.info("Test message 2")

    sleep(2)

    logger.debug("Test message 3")

    time_filter.reset_time_reference()

    logger.warning("Test message 4")

    sleep(1)

    logger.error("Test message 5")

    assert caplog.records[0].reltime == pytest.approx(0, abs=0.2)
    assert caplog.records[1].reltime == pytest.approx(1, abs=0.2)
    assert caplog.records[2].reltime == pytest.approx(3, abs=0.5)
    assert caplog.records[3].reltime == pytest.approx(0, abs=0.2)
    assert caplog.records[4].reltime == pytest.approx(1, abs=0.2)
    assert caplog.record_tuples == [
        ("test_tools_custom", logging.DEBUG, "Test message 1"),
        ("test_tools_custom", logging.INFO, "Test message 2"),
        ("test_tools_custom", logging.DEBUG, "Test message 3"),
        ("test_tools_custom", logging.WARNING, "Test message 4"),
        ("test_tools_custom", logging.ERROR, "Test message 5"),
    ]


def test_diff_time_filter(caplog):
    """
    Test that the DiffTimeFilter adds the differential time to the log record.
    """
    logger = logging.getLogger("test_tools_custom")
    logger.setLevel(logging.DEBUG)

    time_filter = logger_extras.DiffTimeFilter()
    logger.addFilter(time_filter)

    caplog.set_level(logging.DEBUG)

    logger.debug("Test message 1")

    sleep(1)

    logger.info("Test message 2")

    sleep(2)

    logger.debug("Test message 3")
    logger.warning("Test message 4")

    sleep(1)

    logger.error("Test message 5")

    assert caplog.records[0].difftime == pytest.approx(0, abs=0.2)
    assert caplog.records[1].difftime == pytest.approx(1, abs=0.2)
    assert caplog.records[2].difftime == pytest.approx(2, abs=0.2)
    assert caplog.records[3].difftime == pytest.approx(0, abs=0.2)
    assert caplog.records[4].difftime == pytest.approx(1, abs=0.2)
    assert caplog.record_tuples == [
        ("test_tools_custom", logging.DEBUG, "Test message 1"),
        ("test_tools_custom", logging.INFO, "Test message 2"),
        ("test_tools_custom", logging.DEBUG, "Test message 3"),
        ("test_tools_custom", logging.WARNING, "Test message 4"),
        ("test_tools_custom", logging.ERROR, "Test message 5"),
    ]


def test_tiered_formatter(caplog):
    """
    Test that the TieredFormatter formats the log record according to the level.
    """
    logger = logging.getLogger("test_tools_custom")
    logger.setLevel(logging.DEBUG)

    formatter = logger_extras.TieredFormatter(
        fmt="{levelname} - {message}",
        level_fmts={
            logging.DEBUG: "{levelname} - {funcName} - {message}",
            logging.INFO: "{message}",
        },
        style="{",
    )

    caplog.handler.setFormatter(formatter)
    caplog.set_level(logging.DEBUG)

    logger.debug("Test message 1")
    logger.info("Test message 2")
    logger.warning("Test message 3")

    print(caplog.text)
    assert caplog.text == (
        "DEBUG - test_tiered_formatter - Test message 1\n"
        "Test message 2\n"
        "WARNING - Test message 3\n"
    )
