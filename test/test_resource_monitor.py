"""
Unit tests for resource monitor.
"""

import unittest
from unittest.mock import MagicMock, patch
import time
import os
import sqlite3
import tempfile
import shutil
from wpipe.resource_monitor.monitor import ResourceMonitor, ResourceMonitorRegistry


class TestResourceMonitor(unittest.TestCase):
    """Test ResourceMonitor functionality."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_metrics.db")

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    @patch("psutil.Process")
    def test_monitor_basic(self, mock_process_class):
        """Test basic monitoring functionality."""
        # Mock psutil Process
        mock_process = MagicMock()
        mock_process_class.return_value = mock_process
        
        # Mock memory_info().rss
        mock_process.memory_info.return_value.rss = 100 * 1024 * 1024 # 100 MB
        # Mock cpu_percent
        mock_process.cpu_percent.return_value = 5.0
        
        monitor = ResourceMonitor("test_task")
        
        with monitor:
            # Should have started monitoring
            self.assertTrue(monitor._monitoring)
            self.assertEqual(monitor.start_ram_mb, 100.0)
            time.sleep(0.2) # Give monitor thread some time to run
        
        # Should have stopped monitoring
        self.assertFalse(monitor._monitoring)
        self.assertIsNotNone(monitor.end_time)
        self.assertEqual(monitor.end_ram_mb, 100.0)
        
        summary = monitor.get_summary()
        self.assertEqual(summary["task_name"], "test_task")
        self.assertEqual(summary["start_ram_mb"], 100.0)

    @patch("psutil.Process")
    def test_monitor_db_save(self, mock_process_class):
        """Test saving metrics to SQLite."""
        mock_process = MagicMock()
        mock_process_class.return_value = mock_process
        mock_process.memory_info.return_value.rss = 50 * 1024 * 1024
        mock_process.cpu_percent.return_value = 2.0

        monitor = ResourceMonitor("db_task", db_path=self.db_path)
        with monitor:
            time.sleep(0.1)
        
        # Verify DB exists and has data
        self.assertTrue(os.path.exists(self.db_path))
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM resource_metrics WHERE task_name = 'db_task'")
            row = cursor.fetchone()
            self.assertIsNotNone(row)
            self.assertEqual(row[1], "db_task")
            self.assertEqual(row[2], 50.0) # start_ram_mb

    @patch("psutil.Process")
    def test_monitor_registry(self, mock_process_class):
        """Test ResourceMonitorRegistry."""
        mock_process = MagicMock()
        mock_process_class.return_value = mock_process
        mock_process.memory_info.return_value.rss = 10 * 1024 * 1024
        mock_process.cpu_percent.return_value = 1.0

        registry = ResourceMonitorRegistry()
        
        m1 = ResourceMonitor("task1")
        m2 = ResourceMonitor("task2")
        
        m1.start_ram_mb = 10.0
        m1.peak_ram_mb = 20.0
        m1.avg_cpu_percent = 5.0
        m1.start_time = time.time() - 10
        m1.end_time = time.time()
        
        m2.start_ram_mb = 15.0
        m2.peak_ram_mb = 25.0
        m2.avg_cpu_percent = 10.0
        m2.start_time = time.time() - 20
        m2.end_time = time.time()

        registry.add("task1", m1)
        registry.add("task2", m2)
        
        summary = registry.get_summary()
        self.assertIn("task1", summary)
        self.assertIn("task2", summary)
        
        self.assertEqual(registry.get_peak_ram(), 25.0)
        # total_cpu_time = (5 * 10) + (10 * 20) = 50 + 200 = 250
        self.assertAlmostEqual(registry.get_total_cpu_time(), 250.0, places=1)

    @patch("psutil.Process")
    def test_elapsed_seconds(self, mock_process_class):
        """Test elapsed_seconds property."""
        monitor = ResourceMonitor("test")
        self.assertEqual(monitor.elapsed_seconds, 0.0)
        
        monitor.start_time = time.time() - 5
        self.assertAlmostEqual(monitor.elapsed_seconds, 5.0, places=1)
        
        monitor.end_time = monitor.start_time + 10
        self.assertEqual(monitor.elapsed_seconds, 10.0)

    @patch("psutil.Process")
    def test_ram_increase(self, mock_process_class):
        """Test ram_increase_mb property."""
        monitor = ResourceMonitor("test")
        monitor.start_ram_mb = 100.0
        monitor.end_ram_mb = 150.0
        self.assertEqual(monitor.ram_increase_mb, 50.0)

    @patch("psutil.Process")
    def test_monitor_exception_in_loop(self, mock_process_class):
        """Test that monitor loop handles psutil exceptions."""
        import psutil
        mock_process = MagicMock()
        mock_process_class.return_value = mock_process
        
        # Make memory_info raise NoSuchProcess in the loop
        mock_process.memory_info.side_effect = [
            MagicMock(rss=10 * 1024 * 1024), # for start()
            psutil.NoSuchProcess(1234),      # for _monitor_loop
            MagicMock(rss=10 * 1024 * 1024)  # for stop()
        ]
        
        monitor = ResourceMonitor("exception_task")
        monitor.start()
        time.sleep(0.2)
        # Loop should have terminated
        self.assertFalse(monitor._monitor_thread.is_alive())
        monitor.stop()


if __name__ == "__main__":
    unittest.main()
