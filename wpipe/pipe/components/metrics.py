"""
System metrics collection for WPipe pipelines.

This module provides utilities for monitoring CPU, memory, and disk usage
during pipeline execution.
"""

import os
import threading
from typing import Dict, Optional

from wpipe.tracking import PipelineTracker


def get_system_metrics() -> Dict[str, float]:
    """
    Get current system metrics.

    Returns:
        Dict[str, float]: A dictionary containing CPU, memory, and disk IO metrics.
    """
    try:
        import psutil  # pylint: disable=import-outside-toplevel

        process = psutil.Process(os.getpid())
        memory = psutil.virtual_memory()
        disk_io = psutil.disk_io_counters()

        return {
            "cpu_percent": float(process.cpu_percent(interval=0)),
            "memory_percent": float(memory.percent),
            "memory_used_mb": memory.used / 1024 / 1024,
            "memory_available_mb": memory.available / 1024 / 1024,
            "disk_io_read_mb": (disk_io.read_bytes / 1024 / 1024) if disk_io else 0.0,
            "disk_io_write_mb": (disk_io.write_bytes / 1024 / 1024) if disk_io else 0.0,
        }
    except (ImportError, AttributeError, PermissionError):
        return {}


class SystemMetricsCollector:
    """
    Collects system metrics during pipeline execution in a background thread.

    Attributes:
        tracker (PipelineTracker): Tracker to record metrics.
        pipeline_id (str): ID of the pipeline being monitored.
        interval (float): Seconds between metrics collection.
    """

    def __init__(
        self,
        tracker: PipelineTracker,
        pipeline_id: str,
        interval_seconds: float = 0.5
    ) -> None:
        """
        Initialize the metrics collector.

        Args:
            tracker: Tracker instance for recording data.
            pipeline_id: Identifier of the target pipeline.
            interval_seconds: Frequency of collection.
        """
        self.tracker: PipelineTracker = tracker
        self.pipeline_id: str = pipeline_id
        self.interval: float = interval_seconds
        self._stop_event: threading.Event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        """Start the background collection thread."""
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._collect_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop the background collection thread."""
        self._stop_event.set()

    def _collect_loop(self) -> None:
        """Continuous collection loop executed in the background thread."""
        while not self._stop_event.is_set():
            try:
                metrics = get_system_metrics()
                if metrics:
                    self.tracker.record_system_metrics(self.pipeline_id, metrics)
            except Exception:  # pylint: disable=broad-exception-caught
                pass
            # Wait for interval or until stop event is set
            self._stop_event.wait(self.interval)
