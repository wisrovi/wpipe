"""
Timeout management for task execution in WPipe pipelines.

Provides timeout functionality for task execution to prevent hanging tasks
and ensure pipeline reliability.
"""

import asyncio
import signal
from functools import wraps
from typing import Any, Callable, Optional, TypeVar

T = TypeVar("T")


class TimeoutError(Exception):
    """Raised when a task execution exceeds timeout."""

    pass


def timeout_sync(seconds: Optional[float]) -> Callable:
    """
    Decorator for synchronous task timeout.

    Args:
        seconds: Timeout in seconds, None for no timeout

    Returns:
        Decorated function with timeout
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            if seconds is None:
                return func(*args, **kwargs)

            def _handle_timeout(signum: int, frame: Any) -> None:
                raise TimeoutError(
                    f"Task '{func.__name__}' exceeded timeout of {seconds}s"
                )

            old_handler = signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(int(seconds))

            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)

            return result

        return wrapper

    return decorator


async def timeout_async(seconds: Optional[float], coro: Any) -> Any:
    """
    Apply timeout to async coroutine.

    Args:
        seconds: Timeout in seconds, None for no timeout
        coro: Coroutine to execute

    Returns:
        Coroutine result

    Raises:
        TimeoutError: If coroutine exceeds timeout
    """
    if seconds is None:
        return await coro

    try:
        return await asyncio.wait_for(coro, timeout=seconds)
    except asyncio.TimeoutError:
        raise TimeoutError(f"Async task exceeded timeout of {seconds}s")


class TaskTimer:
    """Timer for tracking task execution time."""

    def __init__(self, task_name: str, timeout_seconds: Optional[float] = None):
        """
        Initialize task timer.

        Args:
            task_name: Name of the task
            timeout_seconds: Optional timeout limit
        """
        self.task_name = task_name
        self.timeout_seconds = timeout_seconds
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None

    def __enter__(self) -> "TaskTimer":
        """Enter context manager."""
        import time

        self.start_time = time.time()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context manager."""
        import time

        self.end_time = time.time()

    @property
    def elapsed_seconds(self) -> float:
        """Get elapsed time in seconds."""
        if self.start_time is None:
            return 0.0
        end = self.end_time if self.end_time else __import__("time").time()
        return end - self.start_time

    def exceeded_timeout(self) -> bool:
        """Check if timeout was exceeded."""
        if self.timeout_seconds is None:
            return False
        return self.elapsed_seconds > self.timeout_seconds
