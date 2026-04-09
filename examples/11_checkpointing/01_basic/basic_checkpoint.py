"""
Basic checkpointing example.

Demonstrates saving and retrieving checkpoints in a simple pipeline.
"""

from wpipe import Pipeline, CheckpointManager

# Initialize checkpoint manager
db_path = "checkpoint_example.db"
checkpoint_mgr = CheckpointManager(db_path)

# Create a simple pipeline
pipeline = Pipeline()

def step_1(context):
    """First step: data preparation."""
    print("Step 1: Preparing data...")
    return {"data": [1, 2, 3, 4, 5], "status": "prepared"}

def step_2(context):
    """Second step: processing."""
    print("Step 2: Processing data...")
    data = context["data"]
    result = sum(data)
    return {"result": result, "status": "processed"}

def step_3(context):
    """Third step: finalization."""
    print("Step 3: Finalizing...")
    return {"final_result": context["result"], "status": "complete"}

# Add steps to pipeline
pipeline.add_state("step_1", step_1)
pipeline.add_state("step_2", step_2)
pipeline.add_state("step_3", step_3)

def run_with_checkpoints(pipeline_id="demo_pipeline"):
    """Run pipeline with checkpoint support."""
    
    context = {}
    
    for i, step in enumerate(pipeline.steps):
        try:
            print(f"\n--- Executing {step.name} ---")
            result = step.run(context)
            context.update(result)
            
            # Save checkpoint after successful step
            checkpoint_mgr.save_checkpoint(
                pipeline_id=pipeline_id,
                step_order=i,
                step_name=step.name,
                status="success",
                data=result
            )
            print(f"✓ Checkpoint saved for {step.name}")
            
        except Exception as e:
            print(f"✗ Error in {step.name}: {e}")
            
            # Save failed checkpoint
            checkpoint_mgr.save_checkpoint(
                pipeline_id=pipeline_id,
                step_order=i,
                step_name=step.name,
                status="failed"
            )
            raise

if __name__ == "__main__":
    print("=== Basic Checkpointing Example ===\n")
    
    try:
        run_with_checkpoints()
        
        # Show checkpoint statistics
        stats = checkpoint_mgr.get_checkpoint_stats("demo_pipeline")
        print(f"\n--- Checkpoint Statistics ---")
        print(f"Total checkpoints: {stats['total_checkpoints']}")
        print(f"Successful: {stats['successful']}")
        print(f"Failed: {stats['failed']}")
        print(f"Last checkpoint: {stats['last_checkpoint']}")
        
    except Exception as e:
        print(f"\nPipeline failed: {e}")
