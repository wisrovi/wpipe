"""State: clean_data - Clean data."""


def clean_data(data: dict) -> dict:
    return {"cleaned": True, "records": data.get("records", [])}
