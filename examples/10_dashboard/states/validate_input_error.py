"""State: eh_validate_input - Validate input, raise on None."""


def validate_input(data: dict) -> dict:
    if data is None:
        raise ValueError("Input data cannot be None")
    return {"validated": True, "data": data}
