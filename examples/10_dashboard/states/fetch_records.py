"""State: fetch_records - Fetch records from database."""


def fetch_records(data: dict) -> dict:
    return {"records": list(range(100)), "source": "db"}
