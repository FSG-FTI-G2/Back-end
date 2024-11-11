'''
Logger utility module
---
Color mapping:
    - 96: Cyan
    - 95: Header
    - 94: Blue
    - 93: Yellow
    - 92: Green
    - 91: Red
    - 90: Grey
    - 0: Reset
    - 1: Bold
    - 4: Underline
'''

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
        return lambda message: __error_logger.error(f"\033[{color}m[{prefix}]\033[0m {message}")
    elif type == "warning":
        return lambda message: __warning_logger.warning(f"\033[{color}m[{prefix}]\033[0m {message}")
    else:
        return lambda message: __info_logger.info(f"\033[{color}m[{prefix}]\033[0m {message}")
