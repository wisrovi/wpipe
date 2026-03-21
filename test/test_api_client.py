"""
Tests for API client functionality.
"""

import pytest
from unittest.mock import Mock, patch
from wpipe.api_client.api_client import APIClient


class TestAPIClient:
    """Test APIClient class."""

    def test_client_initialization(self):
        """Test API client can be initialized."""
        client = APIClient(base_url="http://localhost", token="test_token")
        assert client.base_url == "http://localhost"
        assert "test_token" in client.headers["Authorization"]

    def test_client_headers_format(self):
        """Test API client has correct headers."""
        client = APIClient(base_url="http://localhost", token="my_token")
        assert client.headers["Content-Type"] == "application/json"
        assert client.headers["Authorization"] == "Bearer my_token"


class TestAPIClientEndpoints:
    """Test API client endpoint methods."""

    def test_register_worker_endpoint(self):
        """Test register_worker method exists."""
        client = APIClient(base_url="http://localhost", token="test")
        assert hasattr(client, "register_worker")
        assert callable(client.register_worker)

    def test_healthcheck_worker_endpoint(self):
        """Test healthcheck_worker method exists."""
        client = APIClient(base_url="http://localhost", token="test")
        assert hasattr(client, "healthcheck_worker")
        assert callable(client.healthcheck_worker)

    def test_register_process_endpoint(self):
        """Test register_process method exists."""
        client = APIClient(base_url="http://localhost", token="test")
        assert hasattr(client, "register_process")
        assert callable(client.register_process)

    def test_end_process_endpoint(self):
        """Test end_process method exists."""
        client = APIClient(base_url="http://localhost", token="test")
        assert hasattr(client, "end_process")
        assert callable(client.end_process)

    def test_update_task_endpoint(self):
        """Test update_task method exists."""
        client = APIClient(base_url="http://localhost", token="test")
        assert hasattr(client, "update_task")
        assert callable(client.update_task)

    def test_get_dashboard_workers_endpoint(self):
        """Test get_dashboard_workers method exists."""
        client = APIClient(base_url="http://localhost", token="test")
        assert hasattr(client, "get_dashboard_workers")
        assert callable(client.get_dashboard_workers)


class TestAPIClientMethods:
    """Test API client HTTP methods."""

    def test_send_post_without_base_url(self):
        """Test send_post raises error without base_url."""
        client = APIClient()
        with pytest.raises(Exception):
            client.send_post("/endpoint", {"data": "test"})

    def test_send_get_without_base_url(self):
        """Test send_get raises error without base_url."""
        client = APIClient()
        with pytest.raises(Exception):
            client.send_get("/endpoint")

    @patch("requests.post")
    def test_send_post_success(self, mock_post):
        """Test successful POST request."""
        mock_response = Mock()
        mock_response.json.return_value = {"status": "success"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        client = APIClient(base_url="http://localhost", token="test")
        result = client.send_post("/test", {"data": "value"})

        assert result == {"status": "success"}
        mock_post.assert_called_once()

    @patch("requests.get")
    def test_send_get_success(self, mock_get):
        """Test successful GET request."""
        mock_response = Mock()
        mock_response.json.return_value = {"data": "test"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = APIClient(base_url="http://localhost", token="test")
        result = client.send_get("/test")

        assert result == {"data": "test"}
        mock_get.assert_called_once()
