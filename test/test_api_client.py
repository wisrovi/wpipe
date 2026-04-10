"""
Comprehensive tests for API client functionality.
"""

from unittest.mock import MagicMock, Mock, patch

import pytest

from wpipe import Pipeline
from wpipe.api_client.api_client import APIClient


class TestAPIClientInit:
    """Test APIClient initialization."""

    def test_init_with_all_params(self):
        """Test initialization with all parameters."""
        client = APIClient(base_url="http://test.com", token="secret")
        assert client.base_url == "http://test.com"
        assert "secret" in client.headers["Authorization"]

    def test_init_without_base_url(self):
        """Test initialization without base_url."""
        client = APIClient(token="secret")
        assert client.base_url is None
        assert "secret" in client.headers["Authorization"]

    def test_init_without_token(self):
        """Test initialization without token."""
        client = APIClient(base_url="http://test.com")
        assert client.base_url == "http://test.com"
        assert "Bearer None" in client.headers["Authorization"]

    def test_default_headers(self):
        """Test default headers are set correctly."""
        client = APIClient(base_url="http://test.com", token="token")
        assert client.headers["Content-Type"] == "application/json"
        assert "Authorization" in client.headers


class TestAPIClientEndpoints:
    """Test API client endpoint methods."""

    def test_register_worker(self):
        """Test register_worker endpoint."""
        client = APIClient(base_url="http://test.com", token="test")
        assert hasattr(client, "register_worker")

    def test_healthcheck_worker(self):
        """Test healthcheck_worker endpoint."""
        client = APIClient(base_url="http://test.com", token="test")
        assert hasattr(client, "healthcheck_worker")

    def test_register_process(self):
        """Test register_process endpoint."""
        client = APIClient(base_url="http://test.com", token="test")
        assert hasattr(client, "register_process")

    def test_end_process(self):
        """Test end_process endpoint."""
        client = APIClient(base_url="http://test.com", token="test")
        assert hasattr(client, "end_process")

    def test_update_task(self):
        """Test update_task endpoint."""
        client = APIClient(base_url="http://test.com", token="test")
        assert hasattr(client, "update_task")

    def test_get_dashboard_workers(self):
        """Test get_dashboard_workers endpoint."""
        client = APIClient(base_url="http://test.com", token="test")
        assert hasattr(client, "get_dashboard_workers")


class TestAPIClientSendPost:
    """Test send_post method."""

    def test_send_post_without_base_url_raises(self):
        """Test send_post raises without base_url."""
        client = APIClient()
        with pytest.raises(ValueError, match="No 'base_url' defined"):
            client.send_post("/endpoint", {"data": "test"})

    @patch("wpipe.api_client.api_client.requests.post")
    def test_send_post_success(self, mock_post):
        """Test successful POST request."""
        mock_response = Mock()
        mock_response.json.return_value = {"status": "success", "id": "123"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        client = APIClient(base_url="http://localhost:8418", token="test")
        result = client.send_post("/test", {"data": "value"})

        assert result == {"status": "success", "id": "123"}
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert "http://localhost:8418/test" in str(call_args)

    @patch("wpipe.api_client.api_client.requests.post")
    def test_send_post_connection_error(self, mock_post):
        """Test POST with connection error returns None."""
        import requests as req

        mock_post.side_effect = req.exceptions.ConnectionError("Connection refused")

        client = APIClient(base_url="http://localhost:8418", token="test")
        result = client.send_post("/test", {"data": "value"})

        assert result is None

    @patch("wpipe.api_client.api_client.requests.post")
    def test_send_post_timeout_error(self, mock_post):
        """Test POST with timeout error."""
        import requests

        mock_post.side_effect = requests.exceptions.Timeout("Timeout")

        client = APIClient(base_url="http://localhost:8418", token="test")
        result = client.send_post("/test", {"data": "value"})

        assert result is None

    @patch("wpipe.api_client.api_client.requests.post")
    def test_send_post_http_error(self, mock_post):
        """Test POST with HTTP error."""
        import requests as req

        mock_response = Mock()
        mock_response.raise_for_status.side_effect = req.exceptions.HTTPError(
            "404 Not Found"
        )
        mock_post.return_value = mock_response

        client = APIClient(base_url="http://localhost:8418", token="test")
        result = client.send_post("/test", {"data": "value"})

        assert result is None


class TestAPIClientSendGet:
    """Test send_get method."""

    def test_send_get_without_base_url_raises(self):
        """Test send_get raises without base_url."""
        client = APIClient()
        with pytest.raises(ValueError, match="No 'base_url' defined"):
            client.send_get("/endpoint")

    @patch("wpipe.api_client.api_client.requests.get")
    def test_send_get_success(self, mock_get):
        """Test successful GET request."""
        mock_response = Mock()
        mock_response.json.return_value = {"workers": []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = APIClient(base_url="http://localhost:8418", token="test")
        result = client.send_get("/dashboard_workers")

        assert result == {"workers": []}
        mock_get.assert_called_once()

    @patch("wpipe.api_client.api_client.requests.get")
    def test_send_get_connection_error(self, mock_get):
        """Test GET with connection error returns None."""
        import requests as req

        mock_get.side_effect = req.exceptions.ConnectionError("Connection refused")

        client = APIClient(base_url="http://localhost:8418", token="test")
        result = client.send_get("/dashboard_workers")

        assert result is None


class TestAPIClientWorkerEndpoints:
    """Test worker-related endpoints."""

    @patch.object(APIClient, "send_post")
    def test_register_worker_calls_send_post(self, mock_send):
        """Test register_worker calls send_post with correct endpoint."""
        mock_send.return_value = {"id": "worker_123"}
        client = APIClient(base_url="http://test.com", token="test")

        result = client.register_worker({"name": "test_worker", "version": "1.0"})

        assert result == {"id": "worker_123"}
        mock_send.assert_called_once_with(
            "/matricula", {"name": "test_worker", "version": "1.0"}
        )

    @patch.object(APIClient, "send_post")
    def test_healthcheck_worker_calls_send_post(self, mock_send):
        """Test healthcheck_worker calls send_post."""
        mock_send.return_value = {"status": "healthy"}
        client = APIClient(base_url="http://test.com", token="test")

        result = client.healthcheck_worker({"worker_id": "123"})

        assert result == {"status": "healthy"}
        mock_send.assert_called_once_with("/healthchecker", {"worker_id": "123"})

    @patch.object(APIClient, "send_post")
    def test_register_process_calls_send_post(self, mock_send):
        """Test register_process calls send_post."""
        mock_send.return_value = {"process_id": "proc_123"}
        client = APIClient(base_url="http://test.com", token="test")

        result = client.register_process({"name": "test_process"})

        assert result == {"process_id": "proc_123"}
        mock_send.assert_called_once_with("/newprocess", {"name": "test_process"})

    @patch.object(APIClient, "send_post")
    def test_end_process_calls_send_post(self, mock_send):
        """Test end_process calls send_post."""
        mock_send.return_value = {"status": "ended"}
        client = APIClient(base_url="http://test.com", token="test")

        result = client.end_process({"process_id": "proc_123"})

        assert result == {"status": "ended"}
        mock_send.assert_called_once_with("/endprocess", {"process_id": "proc_123"})

    @patch.object(APIClient, "send_post")
    def test_update_task_calls_send_post(self, mock_send):
        """Test update_task calls send_post."""
        mock_send.return_value = {"status": "updated"}
        client = APIClient(base_url="http://test.com", token="test")

        result = client.update_task({"task_id": "task_123", "status": "done"})

        assert result == {"status": "updated"}
        mock_send.assert_called_once_with(
            "/actualizar_task", {"task_id": "task_123", "status": "done"}
        )


class TestAPIClientDashboard:
    """Test dashboard endpoint."""

    @patch.object(APIClient, "send_get")
    def test_get_dashboard_workers_calls_send_get(self, mock_get):
        """Test get_dashboard_workers calls send_get."""
        mock_get.return_value = {"workers": [{"id": "1"}, {"id": "2"}]}
        client = APIClient(base_url="http://test.com", token="test")

        result = client.get_dashboard_workers()

        assert result == {"workers": [{"id": "1"}, {"id": "2"}]}
        mock_get.assert_called_once_with("/dashboard_workers")


class TestAPIClientEdgeCases:
    """Test edge cases."""

    @patch("wpipe.api_client.api_client.requests.post")
    def test_send_post_with_empty_data(self, mock_post):
        """Test POST with empty data dict."""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        client = APIClient(base_url="http://test.com", token="test")
        result = client.send_post("/endpoint", {})

        assert result == {}

    @patch("wpipe.api_client.api_client.requests.post")
    def test_send_post_with_special_characters(self, mock_post):
        """Test POST with special characters in data."""
        mock_response = Mock()
        mock_response.json.return_value = {"status": "ok"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        client = APIClient(base_url="http://test.com", token="test")
        result = client.send_post("/endpoint", {"name": "Test <>&\"'"})

        assert result == {"status": "ok"}

    @patch("wpipe.api_client.api_client.requests.post")
    def test_send_post_with_unicode(self, mock_post):
        """Test POST with unicode characters."""
        mock_response = Mock()
        mock_response.json.return_value = {"status": "ok"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        client = APIClient(base_url="http://test.com", token="test")
        result = client.send_post("/endpoint", {"text": "Hola mundo 🌍"})

        assert result == {"status": "ok"}

    @patch("wpipe.api_client.api_client.requests.post")
    def test_send_post_with_nested_data(self, mock_post):
        """Test POST with nested data structure."""
        mock_response = Mock()
        mock_response.json.return_value = {"status": "ok"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        client = APIClient(base_url="http://test.com", token="test")
        result = client.send_post(
            "/endpoint",
            {
                "user": {"name": "John", "settings": {"theme": "dark"}},
                "items": [1, 2, 3],
            },
        )

        assert result == {"status": "ok"}


class TestAPIClientPipeline:
    """Test APIClient integration with Pipeline."""

    @patch("wpipe.api_client.api_client.requests.post")
    def test_pipeline_with_mock_api(self, mock_post):
        """Test Pipeline works with mocked API."""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "worker_123"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        pipeline = Pipeline(
            worker_name="test_worker",
            api_config={"base_url": "http://localhost:8418", "token": "test"},
            verbose=False,
        )

        pipeline.set_steps([(lambda d: {"result": d.get("x", 0) * 2}, "Test", "v1")])

        def process(data):
            return {"result": data.get("x", 0) * 2}

        pipeline.set_steps([(process, "Test", "v1")])
        result = pipeline.run({"x": 5})

        assert result["result"] == 10

    def test_pipeline_without_api_config(self):
        """Test Pipeline works without api_config."""
        pipeline = Pipeline(verbose=False)

        def process(data):
            return {"result": data.get("x", 0) * 2}

        pipeline.set_steps([(process, "Test", "v1")])
        result = pipeline.run({"x": 5})

        assert result["result"] == 10

    @patch("wpipe.api_client.api_client.requests.post")
    def test_pipeline_with_invalid_api_still_works(self, mock_post):
        """Test Pipeline continues even with invalid API."""
        mock_post.side_effect = Exception("Connection refused")

        api_config = {"base_url": "http://invalid:9999", "token": "invalid"}
        pipeline = Pipeline(
            worker_name="test_worker", api_config=api_config, verbose=False
        )

        def process(data):
            return {"result": data.get("x", 0) * 2}

        pipeline.set_steps([(process, "Test", "v1")])
        result = pipeline.run({"x": 5})

        assert result["result"] == 10


class TestAPIClientHeaders:
    """Test header handling."""

    def test_authorization_header_format(self):
        """Test Authorization header format."""
        client = APIClient(base_url="http://test.com", token="my_token")
        assert client.headers["Authorization"] == "Bearer my_token"

    def test_content_type_header(self):
        """Test Content-Type header."""
        client = APIClient(base_url="http://test.com", token="test")
        assert client.headers["Content-Type"] == "application/json"

    def test_headers_are_dict(self):
        """Test headers is a dictionary."""
        client = APIClient(base_url="http://test.com", token="test")
        assert isinstance(client.headers, dict)
