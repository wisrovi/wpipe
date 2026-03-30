"""State: process_records - Process fetched records."""


def process_records(data: dict) -> dict:
    records = data.get("records", [])
    processed = []
    for record in records:
        if isinstance(record, dict):
            processed.append(
                {
                    "id": record.get("id"),
                    "name": record.get("name"),
                    "score": record.get("score"),
                    "grade": "A"
                    if record.get("score", 0) >= 90
                    else "B"
                    if record.get("score", 0) >= 80
                    else "C"
                    if record.get("score", 0) >= 70
                    else "F",
                    "passed": record.get("score", 0) >= 70,
                }
            )
    return {"processed_records": processed, "total": len(processed)}
