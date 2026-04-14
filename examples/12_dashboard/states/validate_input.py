"""State: validate_input - Validate input data."""


def validate_input(data: dict) -> dict:
    if data is None:
        raise ValueError("Input data cannot be None")
    return {"validated": True, "data": data}
