"""State: read_temp - Read temperature from sensor."""


def read_temp(data: dict) -> dict:
    import random

    return {"temperature": data.get("temperature", random.randint(15, 35))}
