"""State: fetch_data - Fetch data from external source."""


def fetch_data(data: dict) -> dict:
    return {
        "source": "api",
        "records": [
            {"id": 1, "name": "Alice", "score": 95},
            {"id": 2, "name": "Bob", "score": 87},
            {"id": 3, "name": "Charlie", "score": 72},
        ],
    }
