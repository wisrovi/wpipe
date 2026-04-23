"""
Tests for API pipeline functionality.
"""

from typing import Dict, Any
from unittest.mock import Mock, patch

import pytest

from wpipe.api_client.api_client import APIClient
from wpipe.pipe import Pipeline


class TestAPIClient:
    """Tests for the APIClient class.

    This class contains tests to verify the functionality and initialization
    of the APIClient, ensuring it correctly handles base URLs, tokens, and
    HTTP methods.
    """

    def test_client_initialization(self) -> None:
        """Tests that the API client can be successfully initialized.

        Verifies that the base URL and authorization token are correctly set
        in the client's attributes and headers upon initialization.
        """
        base_url: str = "http://localhost"
        token: str = "test_token"
        client = APIClient(base_url=base_url, token=token)
        assert client.base_url == base_url
        assert token in client.headers["Authorization"]

    def test_client_headers_format(self) -> None:
        """Tests the correct formatting of API client headers.

        Ensures that the 'Content-Type' and 'Authorization' headers are
        formatted as expected upon client initialization, including the
        correct 'Bearer' prefix for the token.
        """
        base_url: str = "http://localhost"
        token: str = "my_token"
        client = APIClient(base_url=base_url, token=token)
        assert client.headers["Content-Type"] == "application/json"
        assert client.headers["Authorization"] == f"Bearer {token}"

    def test_register_worker_method_exists(self) -> None:
        """Tests the existence of the register_worker method in APIClient.

        Verifies that the APIClient instance has the 'register_worker' method available,
        indicating that the necessary functionality is implemented.
        """
        client = APIClient(base_url="http://localhost", token="test")
        assert hasattr(client, "register_worker")

    def test_healthcheck_worker_method_exists(self) -> None:
        """Tests the existence of the healthcheck_worker method in APIClient.

        Verifies that the APIClient instance has the 'healthcheck_worker' method available,
        indicating that the necessary functionality is implemented.
        """
        client = APIClient(base_url="http://localhost", token="test")
        assert hasattr(client, "healthcheck_worker")

    def test_register_process_method_exists(self) -> None:
        """Tests the existence of the register_process method in APIClient.

        Verifies that the APIClient instance has the 'register_process' method available,
        indicating that the necessary functionality is implemented.
        """
        client = APIClient(base_url="http://localhost", token="test")
        assert hasattr(client, "register_process")


class TestAPIClientHTTPMethods:
    """Tests for API client HTTP methods.

    This class validates the functionality of basic HTTP methods like GET and POST
    implemented within the APIClient, including error handling and success cases.
    """

    def test_send_post_without_base_url(self) -> None:
        """Tests that send_post raises an error when base_url is not set.

        Verifies that attempting to send a POST request without a configured
        base URL results in a ValueError or TypeError.
        """
        client = APIClient()
        with pytest.raises((ValueError, TypeError)):
            client.send_post("/endpoint", {"data": "test"})

    def test_send_get_without_base_url(self) -> None:
        """Tests that send_get raises an error when base_url is not set.

        Verifies that attempting to send a GET request without a configured
        base URL results in a ValueError or TypeError.
        """
        client = APIClient()
        with pytest.raises((ValueError, TypeError)):
            client.send_get("/endpoint")

    @patch("requests.post")
    def test_send_post_success(self, mock_post: Mock) -> None:
        """Tests a successful POST request using the API client.

        Mocks the requests.post method to simulate a successful response and
        asserts that the client returns the expected JSON data.
        """
        mock_response = Mock()
        mock_response.json.return_value = {"status": "success"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        client = APIClient(base_url="http://localhost", token="test")
        result = client.send_post("/test", {"data": "value"})

        assert result == {"status": "success"}

    @patch("requests.get")
    def test_send_get_success(self, mock_get: Mock) -> None:
        """Tests a successful GET request using the API client.

        Mocks the requests.get method to simulate a successful response and
        asserts that the client returns the expected JSON data.
        """
        mock_response = Mock()
        mock_response.json.return_value = {"data": "test"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = APIClient(base_url="http://localhost", token="test")
        result = client.send_get("/test")

        assert result == {"data": "test"}


class TestPipelineWithAPI:
    """Tests for Pipeline configuration with API settings.

    This class verifies that the Pipeline correctly handles API configurations,
    including enabling API communication when worker IDs are set and ensuring
    it is disabled when API configuration is absent.
    """

    def test_pipeline_api_config(self) -> None:
        """Tests that the pipeline correctly stores its API configuration.

        Asserts that the `api_config` dictionary passed during initialization
        is correctly assigned to the pipeline's attribute.
        """
        api_config: Dict[str, str] = {
            "base_url": "http://localhost:8418",
            "token": "test_token"
        }
        pipeline = Pipeline(api_config=api_config)
        assert pipeline.api_config == api_config

    def test_pipeline_send_to_api_enabled(self) -> None:
        """Tests that send_to_api is enabled when a worker ID is set.

        Verifies that setting a worker ID on a pipeline with API configuration
        activates the `send_to_api` flag, indicating readiness for API communication.
        """
        api_config: Dict[str, str] = {
            "base_url": "http://localhost:8418",
            "token": "test_token"
        }
        pipeline = Pipeline(api_config=api_config)
        pipeline.set_worker_id("worker123456")
        assert pipeline.send_to_api is True

    def test_pipeline_send_to_api_disabled_without_api_config(self) -> None:
        """Tests that send_to_api is disabled when no API configuration is provided.

        Ensures that if a Pipeline is initialized without an `api_config`, the
        `send_to_api` flag remains False, even after setting a worker ID.
        """
        pipeline = Pipeline()
        pipeline.set_worker_id("worker123456")
        assert pipeline.send_to_api is False


class TestAPIClientErrorHandling:
    """Tests for API client error handling.

    This class focuses on verifying how the APIClient handles various exceptions
    that may occur during HTTP requests, ensuring graceful failure and appropriate
    return values (e.g., None).
    """

    @patch("requests.post")
    def test_send_post_request_exception(self, mock_post: Mock) -> None:
        """Tests that send_post returns None on a requests.RequestException.

        Simulates a connection error during a POST request and asserts that
        the client method returns None, indicating failure.
        """
        import requests

        mock_post.side_effect = requests.exceptions.RequestException("Connection error")

        client = APIClient(base_url="http://localhost", token="test")
        result = client.send_post("/test", {"data": "value"})

        assert result is None

    @patch("requests.get")
    def test_send_get_request_exception(self, mock_get: Mock) -> None:
        """Tests that send_get returns None on a requests.RequestException.

        Simulates a connection error during a GET request and asserts that
        the client method returns None, indicating failure.
        """
        import requests

        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        client = APIClient(base_url="http://localhost", token="test")
        result = client.send_get("/test")

        assert result is None

    @patch("wpipe.api_client.api_client.requests.post")
    def test_register_worker_request_exception(self, mock_post: Mock) -> None:
        """Tests that register_worker returns None on a RequestException.

        Simulates an error during the registration of a worker and verifies
        that the method returns None.
        """
        import requests

        mock_post.side_effect = requests.exceptions.RequestException("Error")

        client = APIClient(base_url="http://localhost", token="test")
        result = client.register_worker({"name": "worker"})

        assert result is None

    @patch("wpipe.api_client.api_client.requests.post")
    def test_healthcheck_worker_request_exception(self, mock_post: Mock) -> None:
        """Tests that healthcheck_worker returns None on a RequestException.

        Simulates an error during a worker health check and verifies that
        the method returns None.
        """
        import requests

        mock_post.side_effect = requests.exceptions.RequestException("Error")

        client = APIClient(base_url="http://localhost", token="test")
        result = client.healthcheck_worker({"id": "123"})

        assert result is None

    @patch("wpipe.api_client.api_client.requests.post")
    def test_register_process_request_exception(self, mock_post: Mock) -> None:
        """Tests that register_process returns None on a RequestException.

        Simulates an error during the registration of a process and verifies
        that the method returns None.
        """
        import requests

        mock_post.side_effect = requests.exceptions.RequestException("Error")

        client = APIClient(base_url="http://localhost", token="test")
        result = client.register_process({"name": "process"})

        assert result is None

    @patch("wpipe.api_client.api_client.requests.post")
    def test_end_process_request_exception(self, mock_post: Mock) -> None:
        """Tests that end_process returns None on a RequestException.

        Simulates an error when ending a process and verifies that the method
        returns None.
        """
        import requests

        mock_post.side_effect = requests.exceptions.RequestException("Error")

        client = APIClient(base_url="http://localhost", token="test")
        result = client.end_process({"id": "123"})

        assert result is None

    @patch("wpipe.api_client.api_client.requests.post")
    def test_update_task_request_exception(self, mock_post: Mock) -> None:
        """Tests that update_task returns None on a RequestException.

        Simulates an error when updating a task and verifies that the method
        returns None.
        """
        import requests

        mock_post.side_effect = requests.exceptions.RequestException("Error")

        client = APIClient(base_url="http://localhost", token="test")
        result = client.update_task({"id": "123"})

        assert result is None

    @patch("wpipe.api_client.api_client.requests.get")
    def test_get_dashboard_workers_request_exception(self, mock_get: Mock) -> None:
        """Tests that get_dashboard_workers returns None on a RequestException.

        Simulates an error when fetching dashboard workers and verifies that
        the method returns None.
        """
        import requests

        mock_get.side_effect = requests.exceptions.RequestException("Error")

        client = APIClient(base_url="http://localhost", token="test")
        result = client.get_dashboard_workers()

        assert result is None