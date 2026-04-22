"""
API Client module for pipeline tracking and communication.
"""

import json
from typing import Optional

import requests


class APIClient:
    """Client for communicating with the pipeline API server."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
    ) -> None:
        """
        Initialize the API client.

        Args:
            base_url: Base URL for the API server.
            token: Authentication token.
        """
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def send_post(self, endpoint: str, data: dict) -> Optional[dict]:
        """
        Send a POST request to an endpoint.

        Args:
            endpoint: API endpoint path.
            data: Request payload.

        Returns:
            Response JSON or None on error.
        """
        if not self.base_url:
            raise ValueError("No 'base_url' defined.")

        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.post(url, headers=self.headers, data=json.dumps(data))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud POST a {url}: {e}")
            return None

    def send_get(self, endpoint: str) -> Optional[dict]:
        """
        Send a GET request to an endpoint.

        Args:
            endpoint: API endpoint path.

        Returns:
            Response JSON or None on error.
        """
        if not self.base_url:
            raise ValueError("No 'base_url' defined.")

        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud GET a {url}: {e}")
            return None

    def register_worker(self, data: dict) -> Optional[dict]:
        """Register a worker with the API server."""
        return self.send_post("/matricula", data)

    def healthcheck_worker(self, data: dict) -> Optional[dict]:
        """Perform worker health check."""
        return self.send_post("/healthchecker", data)

    def register_process(self, data: dict) -> Optional[dict]:
        """Register a new process with the API server."""
        return self.send_post("/newprocess", data)

    def end_process(self, data: dict) -> Optional[dict]:
        """End a process on the API server."""
        return self.send_post("/endprocess", data)

    def update_task(self, data: dict) -> Optional[dict]:
        """Update task status on the API server."""
        return self.send_post("/actualizar_task", data)

    def get_dashboard_workers(self) -> Optional[dict]:
        """Get workers dashboard information."""
        return self.send_get("/dashboard_workers")
