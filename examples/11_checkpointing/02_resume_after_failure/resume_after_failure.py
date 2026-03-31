"""
Resume after failure example.

Demonstrates resuming from a checkpoint after a simulated failure.
"""

from wpipe import Pipeline, CheckpointManager
import time

db_path = "checkpoint_resume.db"
checkpoint_mgr = CheckpointManager(db_path)

def expensive_step(context):
    """Expensive operation - takes time."""
    print("Running expensive operation...")
    time.sleep(2)
    return {"expensive_result": "computed_value"}

def validation_step(context):
    """Validate data."""
    print("Validating...")
    result = context.get("expensive_result")
    if not result:
        raise ValueError("No data to validate")
    return {"validated": True}

def final_step(context):
    """Finalize."""
    print("Finalizing...")
    return {"status": "complete"}

def run_or_resume(pipeline_id="resume_demo"):
    """Run pipeline or resume from checkpoint."""
    
    # Check if we can resume
    if checkpoint_mgr.can_resume(pipeline_id):
        print("⟲ Resuming from checkpoint...")
        last = checkpoint_mgr.get_last_checkpoint(pipeline_id)
        start_from_step = last["step_order"] + 1
        print(f"  Last successful step: {last['step_name']} (order {last['step_order']})")
        print(f"  Resuming from step {start_from_step}")
    else:
        print("⊘ No checkpoint found, starting from beginning...")
        start_from_step = 0
    
    steps = [
        ("expensive_step", expensive_step),
        ("validation_step", validation_step),
        ("final_step", final_step),
    ]
    
    context = {}
    
    for i, (name, func) in enumerate(steps):
        if i < start_from_step:
            print(f"⊘ Skipping {name} (already completed)")
            # Load data from checkpoint
            checkpoint = checkpoint_mgr.get_last_checkpoint(pipeline_id)
            if checkpoint and checkpoint["step_order"] == i - 1:
                context.update(checkpoint["data"] or {})
            continue
        
        try:
            print(f"\n→ Executing {name}...")
            result = func(context)
            context.update(result)
            
            checkpoint_mgr.save_checkpoint(
                pipeline_id=pipeline_id,
                step_order=i,
                step_name=name,
                status="success",
                data=result
            )
            print(f"✓ Checkpoint saved")
            
        except Exception as e:
            print(f"✗ Error: {e}")
            checkpoint_mgr.save_checkpoint(
                pipeline_id=pipeline_id,
                step_order=i,
                step_name=name,
                status="failed"
            )
            print(f"\nTo resume, run the script again.")
            raise

if __name__ == "__main__":
    print("=== Resume After Failure Example ===\n")
    
    try:
        run_or_resume()
        print("\n✓ Pipeline completed successfully!")
        
    except Exception as e:
        print(f"\nPipeline interrupted: {e}")
        print("Run the script again to resume from the last successful step.")
