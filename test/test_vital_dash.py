import pytest
from unittest.mock import MagicMock, patch
import sys

def test_dashboard_startup_coverage():
    # Simulamos el arranque sin bloquear
    with patch("uvicorn.run") as mock_run:
        from wpipe.dashboard.main import start_dashboard
        start_dashboard(db_path="mock.db", port=9999)
        assert mock_run.called

def test_dashboard_api_mock():
    from wpipe.dashboard.main import create_app
    app = create_app("test.db")
    assert app.title == "wpipe Dashboard"
