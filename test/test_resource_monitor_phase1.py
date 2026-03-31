"""
Tests for Phase 1 resource monitoring functionality.

Tests ResourceMonitor and ResourceMonitorRegistry.
"""

import pytest
import time
import tempfile
from pathlib import Path
from wpipe import ResourceMonitor, ResourceMonitorRegistry


class TestResourceMonitor:
    """Test ResourceMonitor class."""

    def test_initialization(self):
        """Test monitor initialization."""
        monitor = ResourceMonitor("test_task")
        assert monitor.task_name == "test_task"
        assert monitor.start_time is None

    def test_context_manager(self):
        """Test using monitor as context manager."""
        with ResourceMonitor("test_task") as monitor:
            time.sleep(0.1)
        
        assert monitor.start_time is not None
        assert monitor.end_time is not None

    def test_elapsed_time(self):
        """Test elapsed time calculation."""
        with ResourceMonitor("test_task") as monitor:
            time.sleep(0.2)
        
        elapsed = monitor.elapsed_seconds
        assert elapsed >= 0.2
        assert elapsed < 0.5

    def test_ram_tracking(self):
        """Test RAM usage tracking."""
        with ResourceMonitor("test_task") as monitor:
            # Create some memory usage
            data = list(range(100000))
            time.sleep(0.1)
        
        summary = monitor.get_summary()
        assert summary["start_ram_mb"] > 0
        assert summary["peak_ram_mb"] >= summary["start_ram_mb"]
        assert summary["end_ram_mb"] > 0

    def test_cpu_tracking(self):
        """Test CPU usage tracking."""
        with ResourceMonitor("test_task") as monitor:
            # CPU intensive work
            result = 0
            for i in range(1000000):
                result += i
            time.sleep(0.1)
        
        summary = monitor.get_summary()
        assert "avg_cpu_percent" in summary

    def test_get_summary(self):
        """Test getting monitor summary."""
        with ResourceMonitor("test_task", timeout_seconds=5) as monitor:
            time.sleep(0.1)
        
        summary = monitor.get_summary()
        
        assert summary["task_name"] == "test_task"
        assert summary["elapsed_seconds"] > 0
        assert summary["start_ram_mb"] > 0
        assert summary["peak_ram_mb"] > 0
        assert summary["end_ram_mb"] > 0
        assert "start_time" in summary
        assert "end_time" in summary

    def test_ram_increase(self):
        """Test RAM increase calculation."""
        with ResourceMonitor("test_task") as monitor:
            data = list(range(10000))
        
        ram_increase = monitor.ram_increase_mb
        assert isinstance(ram_increase, float)

    def test_manual_start_stop(self):
        """Test manual start/stop."""
        monitor = ResourceMonitor("test_task")
        
        monitor.start()
        time.sleep(0.1)
        monitor.stop()
        
        assert monitor.elapsed_seconds >= 0.1

    @pytest.mark.skipif(not True, reason="psutil may not be available")
    def test_with_database_storage(self):
        """Test storing metrics in database."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as f:
            db_path = f.name
        
        try:
            with ResourceMonitor("test_task", db_path=db_path) as monitor:
                time.sleep(0.1)
            
            # Check that database file was created and has data
            assert Path(db_path).exists()
            assert Path(db_path).stat().st_size > 0
        finally:
            Path(db_path).unlink(missing_ok=True)


class TestResourceMonitorRegistry:
    """Test ResourceMonitorRegistry class."""

    def test_initialization(self):
        """Test registry initialization."""
        registry = ResourceMonitorRegistry()
        assert len(registry.monitors) == 0

    def test_add_monitor(self):
        """Test adding monitors to registry."""
        registry = ResourceMonitorRegistry()
        monitor1 = ResourceMonitor("task1")
        monitor2 = ResourceMonitor("task2")
        
        registry.add("task1", monitor1)
        registry.add("task2", monitor2)
        
        assert len(registry.monitors) == 2

    def test_get_summary(self):
        """Test getting summary from registry."""
        registry = ResourceMonitorRegistry()
        
        with ResourceMonitor("task1") as m1:
            time.sleep(0.1)
        registry.add("task1", m1)
        
        with ResourceMonitor("task2") as m2:
            time.sleep(0.1)
        registry.add("task2", m2)
        
        summary = registry.get_summary()
        
        assert "task1" in summary
        assert "task2" in summary
        assert summary["task1"]["task_name"] == "task1"
        assert summary["task2"]["task_name"] == "task2"

    def test_get_peak_ram(self):
        """Test getting peak RAM across all tasks."""
        registry = ResourceMonitorRegistry()
        
        with ResourceMonitor("task1") as m1:
            data = list(range(100000))
        registry.add("task1", m1)
        
        with ResourceMonitor("task2") as m2:
            time.sleep(0.1)
        registry.add("task2", m2)
        
        peak_ram = registry.get_peak_ram()
        
        assert peak_ram > 0
        assert peak_ram >= m1.peak_ram_mb

    def test_get_total_cpu_time(self):
        """Test getting total CPU time."""
        registry = ResourceMonitorRegistry()
        
        with ResourceMonitor("task1") as m1:
            result = sum(range(1000000))
        registry.add("task1", m1)
        
        cpu_time = registry.get_total_cpu_time()
        
        assert isinstance(cpu_time, float)


class TestResourceMonitorIntegration:
    """Integration tests for resource monitoring."""

    def test_multiple_tasks_tracking(self):
        """Test tracking multiple concurrent/sequential tasks."""
        registry = ResourceMonitorRegistry()
        
        tasks = ["data_processing", "analysis", "reporting"]
        
        for task_name in tasks:
            with ResourceMonitor(task_name) as monitor:
                # Simulate work
                data = list(range(50000))
                time.sleep(0.1)
            
            registry.add(task_name, monitor)
        
        summary = registry.get_summary()
        
        assert len(summary) == 3
        for task_name in tasks:
            assert task_name in summary
            assert summary[task_name]["elapsed_seconds"] > 0

    def test_resource_monitor_with_exceptions(self):
        """Test that monitor still works even if task fails."""
        monitor = ResourceMonitor("failing_task")
        
        try:
            with monitor:
                time.sleep(0.1)
                raise ValueError("Task failed")
        except ValueError:
            pass
        
        # Monitor should still have valid data
        summary = monitor.get_summary()
        assert summary["elapsed_seconds"] > 0

    def test_nested_monitoring(self):
        """Test monitoring at different levels."""
        registry = ResourceMonitorRegistry()
        
        # Outer monitor
        with ResourceMonitor("pipeline") as pipeline_monitor:
            # Inner monitors
            with ResourceMonitor("step_1") as step1_monitor:
                time.sleep(0.05)
            registry.add("step_1", step1_monitor)
            
            with ResourceMonitor("step_2") as step2_monitor:
                time.sleep(0.05)
            registry.add("step_2", step2_monitor)
        
        registry.add("pipeline", pipeline_monitor)
        
        # Pipeline should show total time
        summary = registry.get_summary()
        
        pipeline_time = summary["pipeline"]["elapsed_seconds"]
        step1_time = summary["step_1"]["elapsed_seconds"]
        step2_time = summary["step_2"]["elapsed_seconds"]
        
        assert pipeline_time >= step1_time + step2_time


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
