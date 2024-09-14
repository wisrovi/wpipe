"""
This program has a functions that returns
a logger object.
"""

import sys
from loguru import logger


def new_logger(process_name: str, path_file: str = "/logs/file_{time}.log"):

    # for print in console
    logger.add(
        sys.stderr,
        format="{time} {level} {message}",
        filter=f"{process_name}",
        level="INFO",
    )

    # for save in file
    logger.add(
        path_file,
        colorize=True,
        format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green>"
        + "| <level>{level}</level> | <blue>{message}</blue>",
        rotation="50 MB",
        compression="zip",
        retention="10 days",
    )

    return logger
