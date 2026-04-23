"""
API Client module for pipeline tracking and communication.
"""

import json
import logging
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)


class APIClient:
    """
    Client for communicating with the pipeline API server.

    Attributes:
        base_url (Optional[str]): Base URL for the API server.
        headers (Dict[str, str]): HTTP headers for requests, including authorization.
        timeout (int): Default timeout for HTTP requests in seconds.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        timeout: int = 10,
    ) -> None:
        """
        Initializes the API client.

        Args:
            base_url (Optional[str]): Base URL for the API server.
            token (Optional[str]): Authentication token.
            timeout (int): Request timeout in seconds. Defaults to 10.
        """
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        self.timeout = timeout

    def send_post(self, endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Sends a POST request to a specified endpoint.

        Args:
            endpoint (str): API endpoint path.
            data (Dict[str, Any]): Request payload.

        Returns:
            Optional[Dict[str, Any]]: Response JSON as a dictionary, or None on error.

        Raises:
            ValueError: If base_url is not defined.
        """
        if not self.base_url:
            raise ValueError("No 'base_url' defined.")

        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.post(
                url,
                headers=self.headers,
                data=json.dumps(data),
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("Error in POST request to %s: %s", url, e)
            return None

    def send_get(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """
        Sends a GET request to a specified endpoint.

        Args:
            endpoint (str): API endpoint path.

        Returns:
            Optional[Dict[str, Any]]: Response JSON as a dictionary, or None on error.

        Raises:
            ValueError: If base_url is not defined.
        """
        if not self.base_url:
            raise ValueError("No 'base_url' defined.")

        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("Error in GET request to %s: %s", url, e)
            return None

    def register_worker(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Registers a worker with the API server.

        Args:
            data (Dict[str, Any]): Worker registration data.

        Returns:
            Optional[Dict[str, Any]]: Server response.
        """
        return self.send_post("/matricula", data)

    def healthcheck_worker(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Performs a worker health check.

        Args:
            data (Dict[str, Any]): Health check data.

        Returns:
            Optional[Dict[str, Any]]: Server response.
        """
        return self.send_post("/healthchecker", data)

    def register_process(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Registers a new process with the API server.

        Args:
            data (Dict[str, Any]): Process registration data.

        Returns:
            Optional[Dict[str, Any]]: Server response.
        """
        return self.send_post("/newprocess", data)

    def end_process(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Signals the end of a process to the API server.

        Args:
            data (Dict[str, Any]): Process completion data.

        Returns:
            Optional[Dict[str, Any]]: Server response.
        """
        return self.send_post("/endprocess", data)

    def update_task(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Updates task status on the API server.

        Args:
            data (Dict[str, Any]): Task update data.

        Returns:
            Optional[Dict[str, Any]]: Server response.
        """
        return self.send_post("/actualizar_task", data)

    def get_dashboard_workers(self) -> Optional[Dict[str, Any]]:
        """
        Retrieves workers dashboard information.

        Returns:
            Optional[Dict[str, Any]]: Dashboard data.
        """
        return self.send_get("/dashboard_workers")
