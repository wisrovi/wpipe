"""
This program has a functions that returns
a logger object.
"""

import os
import pathlib
import sys
from loguru import logger


def new_logger(
    process_name: str = "wpipe",
    path_file: str = ("/logs" if os.path.exists("/logs") else "logs"),
    filename_format: str = "{time:YYYY-MM-DD}",
):

    # for print in console
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green>"
        + "| <level>{level}</level> | <blue>{message}</blue>",
        filter=f"{process_name}",
        level="WARNING",
        colorize=True,
    )
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green>"
        + "| <level>{level}</level> | <blue>{message}</blue>",
        filter=f"{process_name}",
        level="INFO",
    )

    # for save in file
    logger.add(
        f"{path_file}/{process_name}_{filename_format}.log",
        colorize=True,
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {module}:{function}:{line} | {message}",
        rotation="50 MB",
        compression="zip",
        retention="10 days",
    )

    return logger
