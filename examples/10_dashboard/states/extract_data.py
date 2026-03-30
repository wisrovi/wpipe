"""State: extract_data - Extract data from source."""


def extract_data(data: dict) -> dict:
    return {"extracted": True, "records": list(range(100))}
