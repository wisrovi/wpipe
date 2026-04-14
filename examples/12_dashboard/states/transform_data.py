"""State: transform_data - Transform data."""


def transform_data(data: dict) -> dict:
    return {"transformed": True, "records": data.get("records", [])}
