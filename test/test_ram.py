"""
Tests for RAM memory utilities.
"""

import pytest

from wpipe.ram import memory
from wpipe.ram.ram import get_memory


class TestMemoryFunctions:
    """Test memory-related functions."""

    def test_get_memory_returns_number(self):
        """Test get_memory returns a numeric value."""
        memory_val = get_memory()
        assert isinstance(memory_val, int)
        assert memory_val > 0

    def test_memory_decorator_basic(self):
        """Test memory decorator can be applied to a function."""

        @memory(percentage=0.5)
        def test_function():
            return {"status": "ok"}

        result = test_function()
        assert result == {"status": "ok"}

    def test_memory_decorator_default_percentage(self):
        """Test memory decorator with default percentage."""

        @memory()
        def test_function():
            return True

        result = test_function()
        assert result is True
