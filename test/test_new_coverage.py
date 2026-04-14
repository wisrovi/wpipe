"""
Comprehensive tests for high coverage without calling external APIs.
"""

import os
import json
import sqlite3
import tempfile
import pytest
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from wpipe import PipelineExporter, ResourceMonitor, PipelineTracker
from wpipe.tracking.analysis import AnalysisManager
from wpipe.resource_monitor.monitor import ResourceMonitorRegistry

@pytest.fixture
def temp_db_path():
    """Create a temporary database with schema for tests."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Schema for pipelines
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pipelines (
            id TEXT PRIMARY KEY,
            name TEXT,
            status TEXT,
            total_duration_ms REAL,
            started_at TEXT,
            created_at TEXT
        )
    """)
    # Schema for system_metrics
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pipeline_id TEXT,
            cpu_percent REAL,
            memory_percent REAL,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()
    
    yield db_path
    if os.path.exists(db_path):
        os.unlink(db_path)

# --- PipelineExporter Tests ---

def test_pipeline_exporter_json(temp_db_path):
    """Test exporting logs to JSON."""
    conn = sqlite3.connect(temp_db_path)
    conn.execute("INSERT INTO pipelines (id, name, status) VALUES ('p1', 'pipe1', 'completed')")
    conn.commit()
    conn.close()
    
    exporter = PipelineExporter(temp_db_path)
    res = exporter.export_pipeline_logs(format="json")
    data = json.loads(res)
    assert len(data) == 1
    assert data[0]["id"] == "p1"

def test_pipeline_exporter_csv(temp_db_path):
    """Test exporting logs to CSV."""
    conn = sqlite3.connect(temp_db_path)
    conn.execute("INSERT INTO pipelines (id, name, status) VALUES ('p1', 'pipe1', 'completed')")
    conn.commit()
    conn.close()
    
    exporter = PipelineExporter(temp_db_path)
    res = exporter.export_pipeline_logs(format="csv")
    assert "id,name,status" in res
    assert "p1,pipe1,completed" in res

def test_pipeline_exporter_metrics(temp_db_path):
    """Test exporting metrics."""
    conn = sqlite3.connect(temp_db_path)
    conn.execute("INSERT INTO system_metrics (pipeline_id, cpu_percent) VALUES ('p1', 10.5)")
    conn.commit()
    conn.close()
    
    exporter = PipelineExporter(temp_db_path)
    res = exporter.export_metrics(format="json")
    data = json.loads(res)
    assert data[0]["cpu_percent"] == 10.5

def test_pipeline_exporter_stats(temp_db_path):
    """Test calculating statistics."""
    conn = sqlite3.connect(temp_db_path)
    conn.execute("INSERT INTO pipelines (id, status, total_duration_ms) VALUES ('p1', 'completed', 100.0)")
    conn.execute("INSERT INTO pipelines (id, status, total_duration_ms) VALUES ('p2', 'error', 50.0)")
    conn.commit()
    conn.close()
    
    exporter = PipelineExporter(temp_db_path)
    res = exporter.export_statistics(format="json")
    stats = json.loads(res)
    assert stats["total_executions"] == 2
    assert stats["successful_executions"] == 1
    assert stats["success_rate_percent"] == 50.0

def test_pipeline_exporter_invalid_format(temp_db_path):
    """Test invalid format raises ValueError."""
    exporter = PipelineExporter(temp_db_path)
    with pytest.raises(ValueError):
        exporter.export_pipeline_logs(format="xml")

# --- ResourceMonitor Tests ---

def test_resource_monitor_basic():
    """Test ResourceMonitor lifecycle."""
    monitor = ResourceMonitor("test_task")
    monitor.start()
    assert monitor._monitoring is True
    # Wait a bit for loop to run
    import time
    time.sleep(0.2)
    monitor.stop()
    assert monitor._monitoring is False
    assert monitor.end_time is not None
    
    summary = monitor.get_summary()
    assert summary["task_name"] == "test_task"
    assert "elapsed_seconds" in summary

def test_resource_monitor_context_manager():
    """Test ResourceMonitor as context manager."""
    with ResourceMonitor("ctx_task") as monitor:
        assert monitor._monitoring is True
    assert monitor._monitoring is False

def test_resource_monitor_db_save(temp_db_path):
    """Test saving metrics to DB."""
    monitor = ResourceMonitor("db_task", db_path=temp_db_path)
    monitor.start()
    time.sleep(0.1)
    monitor.stop()
    
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT task_name FROM resource_metrics")
    row = cursor.fetchone()
    assert row[0] == "db_task"
    conn.close()

def test_resource_monitor_registry():
    """Test ResourceMonitorRegistry."""
    registry = ResourceMonitorRegistry()
    m1 = ResourceMonitor("t1")
    m2 = ResourceMonitor("t2")
    
    registry.add("t1", m1)
    registry.add("t2", m2)
    
    summary = registry.get_summary()
    assert "t1" in summary
    assert "t2" in summary
    
    m1.peak_ram_mb = 100
    m2.peak_ram_mb = 200
    assert registry.get_peak_ram() == 200

# --- AnalysisManager Tests ---

def test_analysis_manager_stats():
    """Test AnalysisManager statistics calculation."""
    # Mock database objects
    db_p = MagicMock()
    # Create mock objects with proper attributes
    p1 = MagicMock()
    p1.status = "completed"
    p1.total_duration_ms = 100
    
    p2 = MagicMock()
    p2.status = "error"
    p2.total_duration_ms = None
    
    db_p.get_all.return_value = [p1, p2]
    
    db_s = MagicMock()
    db_s.get_all.return_value = []
    
    db_h = MagicMock()
    db_af = MagicMock()
    db_af.get_all.return_value = []
    
    analysis = AnalysisManager(db_p, db_s, db_h, db_af)
    stats = analysis.get_stats()
    
    assert stats["total_pipelines"] == 2
    assert stats["completed"] == 1
    assert stats["errors"] == 1
    assert stats["success_rate"] == 50.0

def test_analysis_manager_trends():
    """Test AnalysisManager trend data."""
    db_p = MagicMock()
    now = datetime.now()
    p1 = MagicMock()
    p1.started_at = now.isoformat()
    p1.status = "completed"
    p1.total_duration_ms = 100
    p1.name = "test"
    
    db_p.get_all.return_value = [p1]
    
    analysis = AnalysisManager(db_p, None, None, None)
    trends = analysis.get_trend_data(days=1)
    
    assert len(trends) == 1
    assert trends[0]["count"] == 1
    assert trends[0]["success"] == 1

import time
