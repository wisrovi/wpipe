"""State: load_data - Load data to target."""


def load_data(data: dict) -> dict:
    return {"loaded": True, "count": len(data.get("records", []))}
