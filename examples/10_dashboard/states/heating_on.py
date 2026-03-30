"""State: heating_on - Turn on heating system."""


def heating_on(data: dict) -> dict:
    return {"heating": "on", "temperature": data.get("temperature")}
