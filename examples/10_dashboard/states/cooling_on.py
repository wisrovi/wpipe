"""State: cooling_on - Turn on cooling system."""


def cooling_on(data: dict) -> dict:
    return {"cooling": "on", "temperature": data.get("temperature")}
