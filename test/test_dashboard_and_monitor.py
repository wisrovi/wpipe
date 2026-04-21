import pytest
import time
from fastapi.testclient import TestClient
from wpipe.dashboard.main import create_app
from wpipe.resource_monitor.monitor import ResourceMonitor

@pytest.fixture
def client(tmp_path):
    # Initialize dashboard with temporary db
    db_path = str(tmp_path / "dashboard.db")
    app = create_app(db_path=db_path, config_dir=str(tmp_path))
    return TestClient(app)

def test_dashboard_routes(client):
    # Test main routes
    res_index = client.get("/")
    assert res_index.status_code == 200

def test_dashboard_api(client):
    # Test API endpoints
    res_health = client.get("/api/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "healthy"
    
    res_stats = client.get("/api/stats")
    assert res_stats.status_code == 200
    
    res_trends = client.get("/api/trends")
    assert res_trends.status_code == 200
    
    res_alerts = client.get("/api/alerts")
    assert res_alerts.status_code == 200

def test_resource_monitor():
    monitor = ResourceMonitor()

    
    # Test single reading
    reading = monitor.get_current_reading()
    assert "cpu_percent" in reading
    assert "ram_percent" in reading
    
    # Test background monitoring
    monitor.start()
    assert monitor.is_running
    time.sleep(0.2)
    monitor.stop()
    assert not monitor.is_running
    
    # Test summary
    summary = monitor.get_summary()
    assert "peak_ram_mb" in summary
    assert "avg_cpu_percent" in summary
    assert "readings_count" in summary
    
    # Test formatting
    text = monitor.format_summary(summary)
    assert "Resource Summary" in text
    
    # Empty summary
    empty_monitor = ResourceMonitor()
    empty_summary = empty_monitor.get_summary()
    assert empty_summary["readings_count"] == 0
    assert empty_summary["avg_cpu_percent"] == 0.0
