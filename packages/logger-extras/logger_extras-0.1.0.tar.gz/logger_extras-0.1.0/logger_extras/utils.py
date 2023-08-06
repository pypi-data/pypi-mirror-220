"""
A collection of logging utilities, including:
log_function_call - A decorator that logs the arguments and return value of a function call.
"""
from __future__ import annotations

import logging
import sys
from functools import wraps
from typing import Callable, TypeVar

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec
Param = ParamSpec("Param")
RetType = TypeVar("RetType")


def log_function_call(
    level: int = logging.DEBUG, *, fixed_logger: logging.Logger | None = None,
) -> Callable[[Callable[Param, RetType]], Callable[Param, RetType]]:
    """
    A decorator that logs the arguments and return value of a function call.

    :param level: The logging level to use.
    :param fixed_logger: A logger to use instead of the one from the function's module.
    :return: A decorator that logs the arguments and return value of a function call.
    """
    def decorator(func: Callable[Param, RetType]) -> Callable[Param, RetType]:
        if fixed_logger:
            logger = fixed_logger
        else:
            logger = logging.getLogger(func.__module__)

        @wraps(func)
        def wrapper_func(*args: Param.args, **kwargs: Param.kwargs) -> RetType:
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)

            logger.log(level, f"Calling {func.__qualname__}({signature})")
            value = func(*args, **kwargs)
            logger.log(level, f"{func.__qualname__!r} returned {value!r}")

            return value
        return wrapper_func
    return decorator
