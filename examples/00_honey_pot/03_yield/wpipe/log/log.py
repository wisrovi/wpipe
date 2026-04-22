"""
Logging utilities for wpipe.
"""

import os
import sys
from typing import Optional

from loguru import logger as loguru_logger


def new_logger(
    process_name: str = "wpipe",
    path_file: Optional[str] = None,
    filename_format: str = "{time:YYYY-MM-DD}",
):
    """
    Create and configure a new logger instance.

    Args:
        process_name: Name for the logger process.
        path_file: Directory path for log files.
        filename_format: Format string for log filename.

    Returns:
        Configured logger instance.
    """
    if path_file is None:
        path_file = "/logs" if os.path.exists("/logs") else "logs"

    loguru_logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green>"
        + "| <level>{level}</level> | <blue>{message}</blue>",
        filter=f"{process_name}",
        level="WARNING",
        colorize=True,
    )
    loguru_logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green>"
        + "| <level>{level}</level> | <blue>{message}</blue>",
        filter=f"{process_name}",
        level="INFO",
    )

    loguru_logger.add(
        f"{path_file}/{process_name}_{filename_format}.log",
        colorize=True,
        format="{time:YYYY-MM-DD at HH:mm:ss} | "
        + "{level} | {module}:{function}:{line} | {message}",
        rotation="50 MB",
        compression="zip",
        retention="10 days",
    )

    return loguru_logger
