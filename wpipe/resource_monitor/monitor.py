"""
Resource monitoring for pipeline task execution.

Tracks RAM, CPU, and other system metrics during pipeline execution.
"""

import threading
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import psutil
from wsqlite import WSQLite

from wpipe.sqlite.tables_dto.tracker_models import ResourceMetricsModel


class ResourceMonitor:
    """Monitor system resources during task execution."""

    # pylint: disable=too-many-instance-attributes
    def __init__(self, task_name: str, db_path: Optional[str] = None):
        """
        Initialize the resource monitor.

        Args:
            task_name: Name of the task being monitored.
            db_path: Optional path to store metrics in SQLite.
        """
        self.task_name = task_name
        self.db_path = db_path
        try:
            self.process = psutil.Process()
        except psutil.NoSuchProcess:
            self.process = None

        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None

        self.start_ram_mb: float = 0.0
        self.peak_ram_mb: float = 0.0
        self.end_ram_mb: float = 0.0

        self.start_cpu_percent: float = 0.0
        self.avg_cpu_percent: float = 0.0
        self.start_cpu_total: float = 0.0

        self.metrics: List[Dict[str, Any]] = []
        self._monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None

    @property
    def is_running(self) -> bool:
        """
        Check if monitoring is currently active.

        Returns:
            True if monitoring is active, False otherwise.
        """
        return self._monitoring

    def get_current_reading(self) -> Dict[str, float]:
        """
        Get current resource usage.

        Returns:
            Dictionary with current CPU and RAM usage.
        """
        if not self.process:
            return {"cpu_percent": 0.0, "ram_percent": 0.0}

        try:
            cpu_percent = self.process.cpu_percent(interval=None)
            ram_mb = self.process.memory_info().rss / (1024 * 1024)
            # Calculate RAM percentage based on total available memory
            total_ram = psutil.virtual_memory().total / (1024 * 1024)
            ram_percent = (ram_mb / total_ram) * 100 if total_ram > 0 else 0.0
            return {
                "cpu_percent": cpu_percent,
                "ram_percent": ram_percent
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return {
                "cpu_percent": 0.0,
                "ram_percent": 0.0
            }

    def __enter__(self) -> "ResourceMonitor":
        """
        Enter context manager.

        Returns:
            The ResourceMonitor instance.
        """
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Exit context manager.

        Args:
            exc_type: Exception type.
            exc_val: Exception value.
            exc_tb: Exception traceback.
        """
        self.stop()

    def start(self) -> None:
        """Start resource monitoring."""
        if not self.process:
            return

        self.start_time = time.time()
        try:
            self.start_ram_mb = self.process.memory_info().rss / (1024 * 1024)
            self.peak_ram_mb = self.start_ram_mb

            # Save initial CPU times (user + system)
            cpu_times = self.process.cpu_times()
            self.start_cpu_total = cpu_times.user + cpu_times.system
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

        self._monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()

    def stop(self) -> None:
        """Stop resource monitoring."""
        if not self.process:
            self._monitoring = False
            return

        self._monitoring = False

        self.end_time = time.time()
        try:
            self.end_ram_mb = self.process.memory_info().rss / (1024 * 1024)

            # Calculate real CPU consumption based on accumulated times
            cpu_times = self.process.cpu_times()
            end_cpu_total = cpu_times.user + cpu_times.system

            delta_cpu = end_cpu_total - self.start_cpu_total
            duration = self.end_time - (self.start_time or self.end_time)

            if duration > 0:
                # Percentage = (cpu_time_used / real_time) * 100
                self.avg_cpu_percent = (delta_cpu / duration) * 100
            else:
                self.avg_cpu_percent = 0.0
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

        if self.db_path:
            self._save_to_db()

    def _monitor_loop(self) -> None:
        """Internal monitoring loop."""
        if not self.process:
            return

        while self._monitoring:
            try:
                ram_mb = self.process.memory_info().rss / (1024 * 1024)
                cpu_percent = self.process.cpu_percent(interval=None)

                self.peak_ram_mb = max(self.peak_ram_mb, ram_mb)

                self.metrics.append(
                    {
                        "timestamp": time.time(),
                        "ram_mb": ram_mb,
                        "cpu_percent": cpu_percent,
                    }
                )

                time.sleep(0.5)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                break

    @property
    def elapsed_seconds(self) -> float:
        """
        Get elapsed time in seconds.

        Returns:
            Elapsed time since monitoring started.
        """
        if self.start_time is None:
            return 0.0
        end = self.end_time if self.end_time else time.time()
        return end - self.start_time

    @property
    def ram_increase_mb(self) -> float:
        """
        Get RAM increase in MB.

        Returns:
            Difference between end RAM and start RAM.
        """
        return self.end_ram_mb - self.start_ram_mb

    def get_summary(self) -> Dict[str, Any]:
        """
        Get monitoring summary.

        Returns:
            Dictionary with aggregated metrics summary.
        """
        return {
            "task_name": self.task_name,
            "elapsed_seconds": round(self.elapsed_seconds, 2),
            "start_ram_mb": round(self.start_ram_mb, 2),
            "peak_ram_mb": round(self.peak_ram_mb, 2),
            "end_ram_mb": round(self.end_ram_mb, 2),
            "ram_increase_mb": round(self.ram_increase_mb, 2),
            "avg_cpu_percent": round(self.avg_cpu_percent, 2),
            "start_time": (
                datetime.fromtimestamp(self.start_time).isoformat()
                if self.start_time
                else None
            ),
            "end_time": (
                datetime.fromtimestamp(self.end_time).isoformat()
                if self.end_time
                else None
            ),
        }

    def _save_to_db(self) -> None:
        """Save metrics to SQLite database using WSQLite."""
        if not self.db_path:
            return

        try:
            db = WSQLite(ResourceMetricsModel, self.db_path)

            metric_data = ResourceMetricsModel(
                task_name=self.task_name,
                start_ram_mb=self.start_ram_mb,
                peak_ram_mb=self.peak_ram_mb,
                end_ram_mb=self.end_ram_mb,
                avg_cpu_percent=self.avg_cpu_percent,
                elapsed_seconds=self.elapsed_seconds
            )

            db.insert(metric_data)
        except (AttributeError, RuntimeError, ValueError) as e:
            print(f"Warning: Could not save metrics to DB: {e}")


class ResourceMonitorRegistry:
    """Registry for managing multiple resource monitors."""

    def __init__(self):
        """Initialize the registry."""
        self.monitors: Dict[str, ResourceMonitor] = {}

    def add(self, task_name: str, monitor: ResourceMonitor) -> None:
        """
        Add a monitor to the registry.

        Args:
            task_name: Name of the task.
            monitor: ResourceMonitor instance.
        """
        self.monitors[task_name] = monitor

    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary of all monitored tasks.

        Returns:
            Dictionary mapping task names to their summaries.
        """
        return {
            task_name: monitor.get_summary()
            for task_name, monitor in self.monitors.items()
        }

    def get_peak_ram(self) -> float:
        """
        Get peak RAM usage across all tasks.

        Returns:
            The maximum peak RAM usage observed.
        """
        if not self.monitors:
            return 0.0
        return max(m.peak_ram_mb for m in self.monitors.values())

    def get_total_cpu_time(self) -> float:
        """
        Get total CPU time across all tasks.

        Returns:
            Aggregated CPU time in percentage-seconds.
        """
        return sum(
            m.avg_cpu_percent * m.elapsed_seconds for m in self.monitors.values()
        )
