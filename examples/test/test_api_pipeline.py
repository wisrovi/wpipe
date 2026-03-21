"""
Tests for API pipeline functionality.
"""

import pytest
from unittest.mock import Mock, patch
from wpipe.pipe import Pipeline
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

    def test_register_worker_method_exists(self):
        """Test register_worker method exists."""
        client = APIClient(base_url="http://localhost", token="test")
        assert hasattr(client, "register_worker")

    def test_healthcheck_worker_method_exists(self):
        """Test healthcheck_worker method exists."""
        client = APIClient(base_url="http://localhost", token="test")
        assert hasattr(client, "healthcheck_worker")

    def test_register_process_method_exists(self):
        """Test register_process method exists."""
        client = APIClient(base_url="http://localhost", token="test")
        assert hasattr(client, "register_process")


class TestAPIClientHTTPMethods:
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


class TestPipelineWithAPI:
    """Test pipeline with API configuration."""

    def test_pipeline_api_config(self):
        """Test pipeline with API config."""
        api_config = {"base_url": "http://localhost:8418", "token": "test_token"}
        pipeline = Pipeline(api_config=api_config)
        assert pipeline.api_config == api_config

    def test_pipeline_send_to_api_enabled(self):
        """Test send_to_api is enabled after setting worker_id."""
        api_config = {"base_url": "http://localhost:8418", "token": "test_token"}
        pipeline = Pipeline(api_config=api_config)
        pipeline.set_worker_id("worker123456")
        assert pipeline.send_to_api is True

    def test_pipeline_send_to_api_disabled_without_api_config(self):
        """Test send_to_api is disabled without API config."""
        pipeline = Pipeline()
        pipeline.set_worker_id("worker123456")
        assert pipeline.send_to_api is False


class TestAPIClientErrorHandling:
    """Test API client error handling."""

    @patch("requests.post")
    def test_send_post_request_exception(self, mock_post):
        """Test POST handles RequestException."""
        import requests

        mock_post.side_effect = requests.exceptions.RequestException("Connection error")

        client = APIClient(base_url="http://localhost", token="test")
        result = client.send_post("/test", {"data": "value"})

        assert result is None

    @patch("requests.get")
    def test_send_get_request_exception(self, mock_get):
        """Test GET handles RequestException."""
        import requests

        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        client = APIClient(base_url="http://localhost", token="test")
        result = client.send_get("/test")

        assert result is None

    @patch("wpipe.api_client.api_client.requests.post")
    def test_register_worker_request_exception(self, mock_post):
        """Test register_worker handles RequestException."""
        import requests

        mock_post.side_effect = requests.exceptions.RequestException("Error")

        client = APIClient(base_url="http://localhost", token="test")
        result = client.register_worker({"name": "worker"})

        assert result is None

    @patch("wpipe.api_client.api_client.requests.post")
    def test_healthcheck_worker_request_exception(self, mock_post):
        """Test healthcheck_worker handles RequestException."""
        import requests

        mock_post.side_effect = requests.exceptions.RequestException("Error")

        client = APIClient(base_url="http://localhost", token="test")
        result = client.healthcheck_worker({"id": "123"})

        assert result is None

    @patch("wpipe.api_client.api_client.requests.post")
    def test_register_process_request_exception(self, mock_post):
        """Test register_process handles RequestException."""
        import requests

        mock_post.side_effect = requests.exceptions.RequestException("Error")

        client = APIClient(base_url="http://localhost", token="test")
        result = client.register_process({"name": "process"})

        assert result is None

    @patch("wpipe.api_client.api_client.requests.post")
    def test_end_process_request_exception(self, mock_post):
        """Test end_process handles RequestException."""
        import requests

        mock_post.side_effect = requests.exceptions.RequestException("Error")

        client = APIClient(base_url="http://localhost", token="test")
        result = client.end_process({"id": "123"})

        assert result is None

    @patch("wpipe.api_client.api_client.requests.post")
    def test_update_task_request_exception(self, mock_post):
        """Test update_task handles RequestException."""
        import requests

        mock_post.side_effect = requests.exceptions.RequestException("Error")

        client = APIClient(base_url="http://localhost", token="test")
        result = client.update_task({"id": "123"})

        assert result is None

    @patch("wpipe.api_client.api_client.requests.get")
    def test_get_dashboard_workers_request_exception(self, mock_get):
        """Test get_dashboard_workers handles RequestException."""
        import requests

        mock_get.side_effect = requests.exceptions.RequestException("Error")

        client = APIClient(base_url="http://localhost", token="test")
        result = client.get_dashboard_workers()

        assert result is None
