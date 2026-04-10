"""
Pipeline tracking module for storing execution data.

Provides functionality to track pipeline execution history,
step timings, and error information.
"""

from .tracker import PipelineTracker, Metric, Severity

__all__ = ["PipelineTracker", "Metric", "Severity"]
