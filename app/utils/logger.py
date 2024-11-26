'''
Logger utility module
---
Color mapping: https://sentry.io/answers/print-colored-text-to-terminal-with-python/
'''
import traceback
import logging

# Uvicorn logger instances
__info_logger = logging.getLogger("uvicorn.info")
__error_logger = logging.getLogger("uvicorn.error")
__warning_logger = logging.getLogger("uvicorn.warning")


def get_logger(prefix: str, color: int, type: str = "info"):
    """
    Create a logger with a specific prefix and color
    """
    if type == "error":
        return lambda message: __error_logger.error(f"\033[{color}m[{prefix}]\033[0m {message}\n\033[90m{traceback.format_exc()}\033[0m")
    elif type == "warning":
        return lambda message: __warning_logger.warning(f"\033[{color}m[{prefix}]\033[0m {message}")
    else:
        return lambda message: __info_logger.info(f"\033[{color}m[{prefix}]\033[0m {message}")
