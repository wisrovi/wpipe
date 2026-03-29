"""
Example 14: API Sending

Demonstrates how to send pipeline execution results to external APIs.
Useful for notifications, webhooks, and integration with other systems.
"""

import time
from wpipe import Pipeline, PipelineTracker


def main():
    db_path = "../wpipe_dashboard.db"
    config_dir = "../configs"

    print("=" * 60)
    print("Example 14: API Sending")
    print("=" * 60)

    tracker = PipelineTracker(db_path, config_dir)

    pipeline = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="api_notification",
        verbose=False,
    )

    pipeline.set_steps(
        [
            (fetch_data, "fetch_data", "v1.0"),
            (process_data, "process_data", "v1.0"),
            (notify_webhook, "notify_webhook", "v1.0"),
        ]
    )

    result = pipeline.run(
        {
            "records": [
                {"id": 1, "name": "Alice", "score": 95},
                {"id": 2, "name": "Bob", "score": 87},
            ]
        }
    )

    print(f"\n[Result] {result}")
    print("\n[API] Results sent to webhook endpoint")

    pipeline.add_event(
        event_type="notification",
        event_name="api_sent",
        message="Results sent to external APIs",
    )

    print("\n" + "=" * 60)
    print(
        "[Dashboard] Run: cd .. && python -m wpipe.dashboard --db wpipe_dashboard.db --config-dir configs --open"
    )
    print("=" * 60)


def fetch_data(d):
    """Fetch initial data."""
    return {
        "source": "api_fetch",
        "records": d.get("records", []),
    }


def process_data(d):
    """Process the fetched data."""
    records = d.get("records", [])
    return {
        "processed": True,
        "count": len(records),
        "avg_score": sum(r.get("score", 0) for r in records) / len(records)
        if records
        else 0,
    }


def notify_webhook(d):
    """Simulate sending notification."""
    print("  [API] Webhook notification sent")
    return {"status": "sent"}


if __name__ == "__main__":
    main()
