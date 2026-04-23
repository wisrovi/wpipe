"""
Memory management module for the pipeline.
"""

from .ram import memory_limit, memory_limit_decorator, memory_storage

# Export the global memory storage instance as 'memory'
memory = memory_storage

__all__ = ["memory_limit", "memory_limit_decorator", "memory"]
