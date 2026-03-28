"""
Tests for wpipe Dashboard module.
"""

import json
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import httpx


@pytest.fixture
def test_db_path():
    """Create a temporary test database."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    from wpipe import Wsqlite

    with Wsqlite(db_name=db_path) as db:
        db.input = {"test": "data"}
        db.output = {"result": "success"}

    yield db_path

    Path(db_path).unlink(missing_ok=True)


@pytest.fixture
def dashboard_base_url(test_db_path):
    """Start dashboard server and return base URL."""
    import threading
    from wpipe.dashboard.main import app, set_db_path
    import uvicorn

    set_db_path(test_db_path)

    config = uvicorn.Config(app, host="127.0.0.1", port=18765, log_level="error")
    server = uvicorn.Server(config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    import time

    time.sleep(1)

    yield "http://127.0.0.1:18765"


class TestDashboardConfig:
    """Tests for dashboard configuration."""

    def test_config_default_values(self):
        """Test default configuration values."""
        from wpipe.dashboard.main import config

        assert config.db_path == "register.db"

    def test_set_db_path(self):
        """Test setting database path."""
        from wpipe.dashboard.main import set_db_path, get_db_path

        set_db_path("custom.db")
        assert str(get_db_path()) == "custom.db"
        set_db_path("register.db")


class TestDashboardAPI:
    """Tests for dashboard API endpoints."""

    def test_health_endpoint(self, dashboard_base_url):
        """Test health check endpoint."""
        with httpx.Client() as client:
            response = client.get(f"{dashboard_base_url}/api/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"]["exists"] is True

    def test_records_endpoint(self, dashboard_base_url):
        """Test records endpoint."""
        with httpx.Client() as client:
            response = client.get(f"{dashboard_base_url}/api/records")

        assert response.status_code == 200
        data = response.json()
        assert "records" in data
        assert "total" in data
        assert data["total"] == 1

    def test_records_pagination(self, dashboard_base_url):
        """Test records pagination."""
        with httpx.Client() as client:
            response = client.get(f"{dashboard_base_url}/api/records?limit=5&offset=0")

        assert response.status_code == 200
        data = response.json()
        assert data["limit"] == 5
        assert data["offset"] == 0

    def test_record_by_id(self, dashboard_base_url):
        """Test getting a specific record."""
        with httpx.Client() as client:
            response = client.get(f"{dashboard_base_url}/api/records/1")

        assert response.status_code == 200
        data = response.json()
        assert "input" in data
        assert "output" in data

    def test_record_not_found(self, dashboard_base_url):
        """Test getting non-existent record."""
        with httpx.Client() as client:
            response = client.get(f"{dashboard_base_url}/api/records/9999")

        assert response.status_code == 404

    def test_stats_endpoint(self, dashboard_base_url):
        """Test statistics endpoint."""
        with httpx.Client() as client:
            response = client.get(f"{dashboard_base_url}/api/stats")

        assert response.status_code == 200
        data = response.json()
        assert "total_executions" in data
        assert "successful" in data
        assert "failed" in data

    def test_config_endpoint(self, dashboard_base_url):
        """Test config endpoint."""
        with httpx.Client() as client:
            response = client.get(f"{dashboard_base_url}/api/config")

        assert response.status_code == 200
        data = response.json()
        assert "db_path" in data


class TestDashboardHTML:
    """Tests for dashboard HTML response."""

    def test_dashboard_html(self, dashboard_base_url):
        """Test dashboard HTML loads."""
        with httpx.Client() as client:
            response = client.get(f"{dashboard_base_url}/")

        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
        assert "wpipe" in response.text.lower()


class TestDashboardNonExistentDB:
    """Tests for non-existent database."""

    @pytest.fixture
    def no_db_base_url(self):
        """Start dashboard server without database."""
        import threading
        from wpipe.dashboard.main import app, set_db_path
        import uvicorn

        set_db_path("nonexistent.db")

        config = uvicorn.Config(app, host="127.0.0.1", port=18766, log_level="error")
        server = uvicorn.Server(config)

        thread = threading.Thread(target=server.run, daemon=True)
        thread.start()

        import time

        time.sleep(1)

        yield "http://127.0.0.1:18766"

    def test_health_no_db(self, no_db_base_url):
        """Test health check with no database."""
        with httpx.Client() as client:
            response = client.get(f"{no_db_base_url}/api/health")

        assert response.status_code == 200
        data = response.json()
        assert data["database"]["exists"] is False

    def test_records_no_db(self, no_db_base_url):
        """Test records with no database."""
        with httpx.Client() as client:
            response = client.get(f"{no_db_base_url}/api/records")

        assert response.status_code == 200
        data = response.json()
        assert data["records"] == []
        assert data["total"] == 0
