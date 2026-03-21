"""
Memory limit utilities for controlling resource usage.
"""

import platform
import resource
import sys
from typing import Callable


def memory_limit(percentage: float) -> None:
    """
    Set memory limit for the current process.

    Only works on Linux operating systems.

    Args:
        percentage: Percentage of available memory to limit (0.0 to 1.0).
    """
    if platform.system() != "Linux":
        print("Only works on linux!")
        return
    _, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(
        resource.RLIMIT_AS, (int(get_memory() * 1024 * percentage), int(hard))
    )


def get_memory() -> int:
    """
    Get available memory in KB.

    Returns:
        Available memory in kilobytes.
    """
    with open("/proc/meminfo", "r", encoding="utf-8") as mem:
        free_memory = 0
        for line in mem:
            sline = line.split()
            if str(sline[0]) in ("MemFree:", "Buffers:", "Cached:"):
                free_memory += int(sline[1])
    return free_memory


def memory(percentage: float = 0.8) -> Callable:
    """
    Decorator to limit memory usage of a function.

    Example:
        @memory(percentage=0.8)
        def main():
            print('My memory is limited to 80%.')

    Args:
        percentage: Memory limit percentage (default 0.8).

    Returns:
        Decorated function.
    """

    def decorator(function: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            memory_limit(percentage)
            try:
                return function(*args, **kwargs)
            except MemoryError:
                mem = get_memory() / 1024 / 1024
                print(f"Remain: {mem:.2f} GB")
                sys.stderr.write("\n\nERROR: Memory Exception\n")
                sys.exit(1)

        return wrapper

    return decorator
