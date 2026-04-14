"""
Example demonstrating pipeline checkpointing and resumption.

This example shows how to use checkpoints to pause and resume pipeline
execution from the last successful step, useful for long-running pipelines.
"""

import time

from wpipe import CheckpointManager, Pipeline


def slow_step_1(data: dict) -> dict:
    """Simulate slow data loading (5 seconds)."""
    print("[Step 1] Loading data...")
    time.sleep(2)
    return {"step_1_data": "loaded", "records": 1000}


def slow_step_2(data: dict) -> dict:
    """Simulate data processing (5 seconds)."""
    print("[Step 2] Processing data...")
    time.sleep(2)
    records = data.get("records", 0)
    return {"step_2_data": f"processed {records} records", "processed": records}


def slow_step_3(data: dict) -> dict:
    """Simulate data saving (5 seconds)."""
    print("[Step 3] Saving results...")
    time.sleep(2)
    return {"step_3_data": "saved successfully"}


def demo_checkpoint():
    """Demonstrate checkpoint functionality."""
    db_path = "checkpoint_demo.db"

    # Initialize checkpoint manager
    checkpoint_mgr = CheckpointManager(db_path)

    # Create pipeline
    pipeline = Pipeline(
        tracking_db=db_path,
        pipeline_name="checkpoint_demo",
        verbose=True,
    )

    pipeline.set_steps(
        [
            (slow_step_1, "load_data", "v1.0"),
            (slow_step_2, "process_data", "v1.0"),
            (slow_step_3, "save_data", "v1.0"),
        ]
    )

    pipeline_id = "demo_pipeline_checkpoint_001"

    # Check if we can resume
    if checkpoint_mgr.can_resume(pipeline_id):
        last_checkpoint = checkpoint_mgr.get_last_checkpoint(pipeline_id)
        print(f"\n✓ Found checkpoint at step: {last_checkpoint['step_name']}")
        print(f"  Step order: {last_checkpoint['step_order']}")
        print(f"  Created at: {last_checkpoint['created_at']}")
        print(f"  Data: {last_checkpoint['data']}\n")
    else:
        print("\n→ No checkpoint found, starting fresh...\n")

    # Run pipeline
    print("=" * 60)
    print("Running pipeline with checkpointing...")
    print("=" * 60 + "\n")

    try:
        result = pipeline.run({"test_data": "initial"})
        print(f"\n✓ Pipeline completed successfully!")
        print(f"Final result: {result}\n")

        # Save checkpoint after success
        checkpoint_mgr.save_checkpoint(
            pipeline_id=pipeline_id,
            step_order=3,
            step_name="save_data",
            status="success",
            data=result,
        )

    except KeyboardInterrupt:
        print("\n⚠ Pipeline interrupted!")
        print(
            "Checkpoint saved. You can resume later with checkpoint_mgr.can_resume()\n"
        )

    # Show checkpoint statistics
    stats = checkpoint_mgr.get_checkpoint_stats(pipeline_id)
    print("\n" + "=" * 60)
    print("Checkpoint Statistics:")
    print("=" * 60)
    print(f"Total checkpoints: {stats['total_checkpoints']}")
    print(f"Successful: {stats['successful']}")
    print(f"Failed: {stats['failed']}")
    print(f"Last checkpoint: {stats['last_checkpoint']}\n")


if __name__ == "__main__":
    demo_checkpoint()
