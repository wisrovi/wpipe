"""State: fan_high - Set fan to high speed."""


def fan_high(data: dict) -> dict:
    return {"fan": "high", "action": data.get("cooling") or data.get("heating")}
