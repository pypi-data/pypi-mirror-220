# logging_extras

A collection of useful logging tools for Python 3.

## Installation

The majority of the tools in this library require no additional dependencies. To install the library with the base functionality use the following command.

```bash
pip install logging-extras
```

To use the `MQTT*` classes, install the library with the following command.

```bash
pip install logging-extras[mqtt]
```

## Tools

- `RelativeTimeFilter` - A logging filter that adds a relative time to the log record.
- `DiffTimeFilter` - A logging filter that adds a time difference to the log record.
- `TieredFormatter` - A logging formatter that allows for different formatting based on the log level.
- `log_function_call` - A decorator that logs the arguments and return value of a function call.

Upcomming tools:

- `MQTThandler` - A logging handler that publishes logs to an MQTT broker.
- `MQTTSubscriber` - A logging listener that subscribes to an MQTT broker and logs messages.

## Examples

### `RelativeTimeFilter`

```python
import logging
from time import sleep

from logger_extras import RelativeTimeFilter

handler = logging.StreamHandler()
relative_time_filter = RelativeTimeFilter()
handler.addFilter(relative_time_filter)
handler.setFormatter(logging.Formatter("%(reltime).3f - %(message)s"))

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.info("Hello World!")
sleep(2)
logger.info("Hello World!")
relative_time_filter.reset_time_reference()
sleep(1)
logger.info("Hello World!")

# This will log the following:
# 0:00:00 - Hello World!
# 0:00:02 - Hello World!
# 0:00:01 - Hello World!
```

### `DiffTimeFilter`

```python
import logging
from time import sleep

from logger_extras import DiffTimeFilter

handler = logging.StreamHandler()
handler.addFilter(DiffTimeFilter())
handler.setFormatter(logging.Formatter("%(difftime).3f - %(message)s"))

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.info("Hello World!")
sleep(2)
logger.info("Hello World!")
sleep(1)
logger.info("Hello World!")

# This will log the following:
# 0:00:00 - Hello World!
# 0:00:02 - Hello World!
# 0:00:01 - Hello World!
```

### `TieredFormatter`

```python
import logging

from logger_extras import TieredFormatter

handler = logging.StreamHandler()
handler.setFormatter(
    TieredFormatter(
        fmt="%(levelname)s - %(message)s",
        level_fmts={
            logging.DEBUG: "%(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
            logging.INFO: "%(message)s",
        },
        datefmt=None,
        style="%",
        validate=True,
    )
)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.debug("Hello World!")
logger.info("Hello World!")
logger.warning("Hello World!")
logger.error("Hello World!")
logger.critical("Hello World!")

# This will log the following:
# DEBUG - __main__:19 - Hello World!
# Hello World!
# WARNING - Hello World!
# ERROR - Hello World!
# CRITICAL - Hello World!
```

### `log_function_call`

```python
from logger_extras import log_function_call

@log_function_call(level=logging.INFO)
def add(a, b):
    return a + b

_ = add(1, 2)
# This will log the following:
# 2021-08-03 12:00:00,000 - INFO - Calling __main__.add(a=1, b=2)
# 2021-08-03 12:00:00,000 - INFO - '__main__.add' returned 3
```
