"""
Unit tests for timeout functionality.
"""

import asyncio
import time
import unittest

from wpipe.timeout import TaskTimer, TimeoutError, timeout_async, timeout_sync


class TestTimeoutSync(unittest.TestCase):
    """Test synchronous timeout decorator."""

    def test_timeout_sync_completes_in_time(self):
        """Test that task completes when under timeout."""

        @timeout_sync(2)
        def fast_task():
            time.sleep(0.1)
            return "success"

        result = fast_task()
        self.assertEqual(result, "success")

    def test_timeout_sync_no_timeout(self):
        """Test that no timeout parameter skips timeout check."""

        @timeout_sync(None)
        def task():
            time.sleep(0.1)
            return "success"

        result = task()
        self.assertEqual(result, "success")


class TestTimeoutAsync(unittest.TestCase):
    """Test asynchronous timeout handling."""

    def test_timeout_async_completes_in_time(self):
        """Test that async task completes when under timeout."""

        async def fast_task():
            await asyncio.sleep(0.1)
            return "success"

        result = asyncio.run(timeout_async(2, fast_task()))
        self.assertEqual(result, "success")

    def test_timeout_async_no_timeout(self):
        """Test that no timeout parameter skips timeout check."""

        async def task():
            await asyncio.sleep(0.1)
            return "success"

        result = asyncio.run(timeout_async(None, task()))
        self.assertEqual(result, "success")


class TestTaskTimer(unittest.TestCase):
    """Test TaskTimer context manager."""

    def test_task_timer_basic(self):
        """Test basic task timer functionality."""
        with TaskTimer("test_task", timeout_seconds=5) as timer:
            time.sleep(0.1)

        self.assertGreater(timer.elapsed_seconds, 0.05)
        self.assertLess(timer.elapsed_seconds, 1.0)

    def test_task_timer_exceeded_timeout(self):
        """Test timeout exceeded detection."""
        with TaskTimer("test_task", timeout_seconds=0.05) as timer:
            time.sleep(0.2)

        self.assertTrue(timer.exceeded_timeout())

    def test_task_timer_no_timeout(self):
        """Test timer without timeout limit."""
        with TaskTimer("test_task", timeout_seconds=None) as timer:
            time.sleep(0.1)

        self.assertFalse(timer.exceeded_timeout())


if __name__ == "__main__":
    unittest.main()
