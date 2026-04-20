import pytest
from wpipe.api_client.api_client import APIClient
from unittest.mock import MagicMock, patch

def test_api_client_coverage():
    client = APIClient(base_url="http://mock", token="test")
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"status": "ok"}
        client.register_worker("W1")
        client.register_process("P1", "PIPE-1")
        client.update_task("PIPE-1", "T1", "success")
        client.end_process("PIPE-1")
