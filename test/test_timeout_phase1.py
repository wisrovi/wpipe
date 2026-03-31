"""
Tests for Phase 1 timeout functionality.

Tests timeout_sync, timeout_async, and TaskTimer.
"""

import pytest
import asyncio
import time
from wpipe import timeout_sync, timeout_async, TaskTimer, TimeoutError


class TestTimeoutSync:
    """Test synchronous timeout decorator."""

    def test_function_completes_within_timeout(self):
        """Test function that completes within timeout."""
        @timeout_sync(seconds=5)
        def quick_task():
            time.sleep(0.1)
            return "success"
        
        result = quick_task()
        assert result == "success"

    def test_function_exceeds_timeout(self):
        """Test function that exceeds timeout."""
        @timeout_sync(seconds=1)
        def slow_task():
            time.sleep(3)
            return "success"
        
        with pytest.raises(TimeoutError):
            slow_task()

    def test_none_timeout_disables(self):
        """Test that None timeout disables timeout."""
        @timeout_sync(None)
        def task():
            time.sleep(0.1)
            return "success"
        
        result = task()
        assert result == "success"

    def test_timeout_error_message(self):
        """Test timeout error contains task name."""
        @timeout_sync(seconds=1)
        def my_task():
            time.sleep(2)
        
        with pytest.raises(TimeoutError) as exc_info:
            my_task()
        
        assert "my_task" in str(exc_info.value)


class TestTimeoutAsync:
    """Test asynchronous timeout."""

    @pytest.mark.asyncio
    async def test_coroutine_completes_within_timeout(self):
        """Test coroutine that completes within timeout."""
        async def quick_coro():
            await asyncio.sleep(0.1)
            return "success"
        
        result = await timeout_async(5, quick_coro())
        assert result == "success"

    @pytest.mark.asyncio
    async def test_coroutine_exceeds_timeout(self):
        """Test coroutine that exceeds timeout."""
        async def slow_coro():
            await asyncio.sleep(3)
            return "success"
        
        with pytest.raises(TimeoutError):
            await timeout_async(1, slow_coro())

    @pytest.mark.asyncio
    async def test_none_timeout_async_disables(self):
        """Test that None timeout disables async timeout."""
        async def coro():
            await asyncio.sleep(0.1)
            return "success"
        
        result = await timeout_async(None, coro())
        assert result == "success"


class TestTaskTimer:
    """Test TaskTimer context manager."""

    def test_elapsed_time_tracking(self):
        """Test elapsed time tracking."""
        with TaskTimer("test_task", timeout_seconds=10) as timer:
            time.sleep(0.2)
        
        assert timer.elapsed_seconds >= 0.2
        assert timer.elapsed_seconds < 0.5

    def test_timeout_not_exceeded(self):
        """Test timeout not exceeded detection."""
        with TaskTimer("test_task", timeout_seconds=5) as timer:
            time.sleep(0.1)
        
        assert not timer.exceeded_timeout()

    def test_timeout_exceeded(self):
        """Test timeout exceeded detection."""
        with TaskTimer("test_task", timeout_seconds=1) as timer:
            # Manually set end time to simulate timeout
            timer.end_time = timer.start_time + 2  # 2 seconds later
        
        assert timer.exceeded_timeout()

    def test_none_timeout_never_exceeds(self):
        """Test that None timeout never exceeds."""
        with TaskTimer("test_task", timeout_seconds=None) as timer:
            timer.end_time = timer.start_time + 1000  # Even after 1000 seconds
        
        assert not timer.exceeded_timeout()

    def test_task_name_stored(self):
        """Test task name is stored."""
        with TaskTimer("my_task", timeout_seconds=10) as timer:
            assert timer.task_name == "my_task"

    def test_properties_accessible(self):
        """Test properties are accessible."""
        with TaskTimer("test", timeout_seconds=10) as timer:
            time.sleep(0.1)
            elapsed = timer.elapsed_seconds
            exceeded = timer.exceeded_timeout()
        
        assert elapsed > 0
        assert isinstance(exceeded, bool)


class TestTimeoutIntegration:
    """Integration tests for timeout functionality."""

    def test_timeout_with_exceptions(self):
        """Test timeout doesn't interfere with normal exceptions."""
        @timeout_sync(seconds=5)
        def task_with_error():
            raise ValueError("Expected error")
        
        with pytest.raises(ValueError) as exc_info:
            task_with_error()
        
        assert "Expected error" in str(exc_info.value)

    def test_timeout_with_return_values(self):
        """Test timeout preserves return values."""
        @timeout_sync(seconds=5)
        def task_with_result():
            return {"key": "value", "number": 42}
        
        result = task_with_result()
        
        assert result == {"key": "value", "number": 42}

    def test_timeout_with_args_kwargs(self):
        """Test timeout with function arguments."""
        @timeout_sync(seconds=5)
        def task_with_args(a, b, c=None):
            return f"{a}-{b}-{c}"
        
        result = task_with_args(1, 2, c=3)
        
        assert result == "1-2-3"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
