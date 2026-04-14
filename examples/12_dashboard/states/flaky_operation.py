"""State: flaky_operation - Operation that might fail."""


def flaky_operation(data: dict) -> dict:
    import random

    if random.random() < 0.3:
        raise Exception("Random failure!")
    return {"success": True}
