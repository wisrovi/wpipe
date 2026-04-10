"""State: calculate_stats - Calculate statistics from processed records."""


def calculate_stats(data: dict) -> dict:
    records = data.get("processed_records", data.get("records", []))
    scores = [r.get("score", 0) for r in records if isinstance(r, dict)]
    return {
        "statistics": {
            "average": sum(scores) / len(scores) if scores else 0,
            "max": max(scores) if scores else 0,
            "min": min(scores) if scores else 0,
        }
    }
