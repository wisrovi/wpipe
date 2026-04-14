"""
Example 06: Events and Annotations

Demonstrates how to add custom events and annotations to pipelines.
Events are visible in the dashboard timeline.
"""

from wpipe import Pipeline


def main():
    db_path = "../wpipe_dashboard.db"
    config_dir = "../configs"

    print("=" * 60)
    print("Example 09: Events and Annotations")
    print("=" * 60)

    pipeline = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="annotated_pipeline",
        verbose=True,
    )

    pipeline.set_steps(
        [
            (initialize, "initialize", "v1.0"),
            (process_batch_1, "process_batch_1", "v1.0"),
            (checkpoint, "checkpoint", "v1.0"),
            (process_batch_2, "process_batch_2", "v1.0"),
            (finalize, "finalize", "v1.0"),
        ]
    )

    print("\n[Running Pipeline...]\n")
    result = pipeline.run({"batch_size": 100})

    print(f"\n[Result] {result}")
    print(
        f"\n[Dashboard] Run: cd .. && python -m wpipe.dashboard --db wpipe_dashboard.db --config-dir configs --open"
    )


# Step functions with events
def initialize(d):
    """Initialize processing."""
    # Events will be added by the pipeline after this step
    print("  [initialize] System initialized")
    return {"initialized": True, "timestamp": "2024-01-01T00:00:00"}


def process_batch_1(d):
    """Process first batch."""
    batch_size = d.get("batch_size", 100)
    print(f"  [process_batch_1] Processing {batch_size} items...")
    return {"batch1_processed": batch_size}


def checkpoint(d):
    """Create a checkpoint."""
    print("  [checkpoint] Creating checkpoint...")
    return {"checkpoint": "completed"}


def process_batch_2(d):
    """Process second batch."""
    print("  [process_batch_2] Processing second batch...")
    return {"batch2_processed": 50}


def finalize(d):
    """Finalize processing."""
    print("  [finalize] Finalizing...")
    return {"finalized": True}


if __name__ == "__main__":
    main()
