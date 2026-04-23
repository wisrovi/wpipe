"""
Memory limit utilities and shared memory storage for the pipeline.
"""

import platform
import resource
import sys
from typing import Any, Callable, Dict


class SharedMemory:
    """Simple key-value storage for sharing data across pipeline runs."""

    def __init__(self) -> None:
        """Initialize shared memory storage."""
        self._data: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        """
        Store a value in shared memory.

        Args:
            key: The key to store the value under.
            value: The value to store.
        """
        self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a value from shared memory.

        Args:
            key: The key to retrieve.
            default: The default value to return if key is not found.

        Returns:
            The stored value or default.
        """
        return self._data.get(key, default)

    def clear(self) -> None:
        """Clear all data from shared memory."""
        self._data.clear()

    def __repr__(self) -> str:
        """Return string representation of SharedMemory."""
        return f"SharedMemory({self._data})"


# Global instance for shared memory access
memory_storage = SharedMemory()


def memory_limit(percentage: float) -> None:
    """
    Set memory limit for the current process.

    Only works on Linux operating systems.

    Args:
        percentage: Percentage of available memory to limit (0.0 to 1.0).
    """
    if platform.system() != "Linux":
        print("Memory limits are only supported on Linux!")
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
    with open("/proc/meminfo", encoding="utf-8") as mem:
        free_memory = 0
        for line in mem:
            sline = line.split()
            if str(sline[0]) in ("MemFree:", "Buffers:", "Cached:"):
                free_memory += int(sline[1])
    return free_memory


def memory_limit_decorator(percentage: float = 0.8) -> Callable:
    """
    Decorator to limit memory usage of a function.

    Example:
        @memory_limit_decorator(percentage=0.8)
        def main():
            print('My memory is limited to 80%.')

    Args:
        percentage: Memory limit percentage (default 0.8).

    Returns:
        Decorated function.
    """

    def decorator(function: Callable) -> Callable:
        """Decorator function."""

        def wrapper(*args, **kwargs) -> Any:
            """Wrapper that applies memory limit."""
            memory_limit(percentage)
            try:
                return function(*args, **kwargs)
            except MemoryError:
                mem = get_memory() / 1024 / 1024
                print(f"Remaining memory: {mem:.2f} GB")
                sys.stderr.write("\n\nERROR: Memory Exception\n")
                sys.exit(1)

        return wrapper

    return decorator
