"""
Phase 1 Complete Honey Pot Example

Comprehensive example demonstrating ALL Phase 1 features:
1. Checkpointing & Resume
2. Task Timeouts  
3. Type Hinting & Validation
4. Resource Monitoring
5. Export & Analytics

This example simulates a complete data processing pipeline with
all reliability and observability features enabled.
"""

from typing import TypedDict, Dict, Any
from wpipe import (
    Pipeline,
    CheckpointManager,
    ResourceMonitor,
    ResourceMonitorRegistry,
    PipelineExporter,
    timeout_sync,
    TaskTimer,
    TypeValidator,
    PipelineContext,
    TimeoutError,
)
import time
import random
import json
from pathlib import Path

# ============================================================================
# STEP 1: Define typed context for the pipeline
# ============================================================================

class DataContext(PipelineContext):
    """Typed context for data processing pipeline."""
    dataset_id: int
    raw_data: list
    processed_data: list
    statistics: Dict[str, Any]
    validated: bool
    exported: bool

# ============================================================================
# STEP 2: Define pipeline steps with timeouts and type validation
# ============================================================================

@timeout_sync(seconds=5)
def fetch_data_step(context: dict) -> dict:
    """Step 1: Fetch raw data (with timeout)."""
    print("  [FETCH] Loading dataset...")
    time.sleep(0.5)
    
    # Simulate fetching data
    raw_data = [random.randint(1, 100) for _ in range(100)]
    
    return {
        "dataset_id": 1,
        "raw_data": raw_data,
        "processed_data": [],
        "statistics": {},
        "validated": False,
        "exported": False,
    }

def validate_data_step(context: dict) -> dict:
    """Step 2: Validate data using type hinting."""
    print("  [VALIDATE] Checking data types...")
    
    # Validate context structure
    schema = {
        "dataset_id": int,
        "raw_data": list,
        "processed_data": list,
    }
    
    try:
        TypeValidator.validate_dict(context, schema)
        print("    ✓ Data structure validated")
    except (TypeError, KeyError) as e:
        print(f"    ✗ Validation failed: {e}")
        raise
    
    return {"validated": True}

@timeout_sync(seconds=10)
def process_data_step(context: dict) -> dict:
    """Step 3: Process data with timeout."""
    print("  [PROCESS] Processing data...")
    time.sleep(1)
    
    # Simulate data processing
    raw_data = context["raw_data"]
    processed = [x * 2 + 1 for x in raw_data]  # Simple transformation
    
    # Calculate statistics
    stats = {
        "count": len(processed),
        "min": min(processed),
        "max": max(processed),
        "mean": sum(processed) / len(processed),
        "sum": sum(processed),
    }
    
    return {
        "processed_data": processed,
        "statistics": stats,
    }

def monitor_resources_step(context: dict) -> dict:
    """Step 4: Resource-intensive analysis."""
    print("  [RESOURCES] Analyzing resource usage...")
    time.sleep(0.5)
    
    # Simulate resource usage
    data = context["processed_data"]
    analysis = {
        "percentile_95": sorted(data)[int(len(data) * 0.95)],
        "percentile_75": sorted(data)[int(len(data) * 0.75)],
        "percentile_50": sorted(data)[int(len(data) * 0.50)],
    }
    
    return {"analysis": analysis}

def export_results_step(context: dict) -> dict:
    """Step 5: Export results."""
    print("  [EXPORT] Exporting results...")
    
    export_dir = Path("honey_pot_phase1_output")
    export_dir.mkdir(exist_ok=True)
    
    # Export data as JSON
    output_file = export_dir / "results.json"
    output_file.write_text(json.dumps({
        "dataset_id": context["dataset_id"],
        "record_count": len(context["processed_data"]),
        "statistics": context["statistics"],
    }, indent=2))
    
    print(f"    ✓ Exported to {output_file}")
    
    return {
        "exported": True,
        "export_path": str(output_file),
    }

# ============================================================================
# STEP 3: Setup Phase 1 infrastructure
# ============================================================================

def setup_phase1_infrastructure():
    """Initialize all Phase 1 components."""
    db_path = "honey_pot_phase1.db"
    
    checkpoint_mgr = CheckpointManager(db_path)
    exporter = PipelineExporter(db_path)
    registry = ResourceMonitorRegistry()
    
    return {
        "db_path": db_path,
        "checkpoint_mgr": checkpoint_mgr,
        "exporter": exporter,
        "registry": registry,
    }

# ============================================================================
# STEP 4: Execute pipeline with all Phase 1 features
# ============================================================================

def run_phase1_pipeline(infrastructure: dict, pipeline_id: str = "honey_pot_phase1"):
    """Execute the complete pipeline with all Phase 1 features."""
    
    checkpoint_mgr = infrastructure["checkpoint_mgr"]
    exporter = infrastructure["exporter"]
    registry = infrastructure["registry"]
    
    steps = [
        ("fetch_data", fetch_data_step),
        ("validate_data", validate_data_step),
        ("process_data", process_data_step),
        ("monitor_resources", monitor_resources_step),
        ("export_results", export_results_step),
    ]
    
    context: Dict[str, Any] = {}
    completed_steps = 0
    
    # Check if we can resume
    if checkpoint_mgr.can_resume(pipeline_id):
        print(f"\n⟲ Resuming from checkpoint...")
        last = checkpoint_mgr.get_last_checkpoint(pipeline_id)
        print(f"  Last completed: {last['step_name']} (order {last['step_order']})")
        start_from = last["step_order"] + 1
        context = last.get("data", {})
    else:
        print(f"\n→ Starting new pipeline execution...")
        start_from = 0
    
    # Execute steps with full Phase 1 support
    with ResourceMonitor(f"pipeline_{pipeline_id}", db_path=infrastructure["db_path"]) as pipeline_monitor:
        
        for i, (step_name, step_func) in enumerate(steps):
            if i < start_from:
                print(f"\n  ⊘ Skipping {step_name} (already completed)")
                continue
            
            print(f"\n  → Executing step: {step_name}")
            
            # Create per-step resource monitor
            with ResourceMonitor(step_name, db_path=infrastructure["db_path"]) as step_monitor:
                try:
                    # Execute step with timeout protection
                    with TaskTimer(step_name, timeout_seconds=15) as timer:
                        result = step_func(context)
                        context.update(result)
                    
                    # Save checkpoint
                    checkpoint_mgr.save_checkpoint(
                        pipeline_id=pipeline_id,
                        step_order=i,
                        step_name=step_name,
                        status="success",
                        data=result
                    )
                    
                    completed_steps += 1
                    
                    # Get step metrics
                    step_summary = step_monitor.get_summary()
                    registry.add(step_name, step_monitor)
                    
                    print(f"    ✓ Completed in {step_summary['elapsed_seconds']:.2f}s")
                    print(f"    ✓ Peak RAM: {step_summary['peak_ram_mb']:.2f} MB")
                    print(f"    ✓ Checkpoint saved")
                    
                except TimeoutError as e:
                    print(f"    ✗ Timeout: {e}")
                    checkpoint_mgr.save_checkpoint(
                        pipeline_id=pipeline_id,
                        step_order=i,
                        step_name=step_name,
                        status="failed"
                    )
                    raise
                    
                except Exception as e:
                    print(f"    ✗ Error: {e}")
                    checkpoint_mgr.save_checkpoint(
                        pipeline_id=pipeline_id,
                        step_order=i,
                        step_name=step_name,
                        status="failed"
                    )
                    raise
        
        # Get pipeline-level metrics
        pipeline_summary = pipeline_monitor.get_summary()
    
    return {
        "context": context,
        "completed_steps": completed_steps,
        "total_steps": len(steps),
        "pipeline_monitor": pipeline_monitor,
        "registry": registry,
    }

# ============================================================================
# STEP 5: Generate reports using Phase 1 export
# ============================================================================

def generate_reports(infrastructure: dict, pipeline_id: str):
    """Generate reports from pipeline execution data."""
    
    exporter = infrastructure["exporter"]
    
    print("\n" + "="*60)
    print("PHASE 1 REPORTS")
    print("="*60)
    
    # Export statistics
    print("\n[STATISTICS]")
    try:
        stats = exporter.export_statistics(format="json")
        if isinstance(stats, str):
            stats = json.loads(stats)
        
        for key, value in stats.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"  (No statistics available: {e})")
    
    # Show checkpoint statistics
    checkpoint_mgr = infrastructure["checkpoint_mgr"]
    cp_stats = checkpoint_mgr.get_checkpoint_stats(pipeline_id)
    print(f"\n[CHECKPOINTS]")
    print(f"  Total checkpoints: {cp_stats['total_checkpoints']}")
    print(f"  Successful: {cp_stats['successful']}")
    print(f"  Failed: {cp_stats['failed']}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    import sys
    
    print("\n" + "="*60)
    print("WPipe Phase 1 - Honey Pot Complete Example")
    print("="*60)
    print("\nDemonstrating all Phase 1 features:")
    print("  1. ✓ Checkpointing & Resume")
    print("  2. ✓ Task Timeouts")
    print("  3. ✓ Type Hinting & Validation")
    print("  4. ✓ Resource Monitoring")
    print("  5. ✓ Export & Analytics")
    
    try:
        # Setup infrastructure
        infrastructure = setup_phase1_infrastructure()
        print("\n✓ Phase 1 infrastructure initialized")
        
        # Run pipeline
        result = run_phase1_pipeline(infrastructure)
        
        print("\n" + "="*60)
        print("PIPELINE EXECUTION SUMMARY")
        print("="*60)
        print(f"\n✓ Pipeline completed successfully!")
        print(f"  Completed steps: {result['completed_steps']}/{result['total_steps']}")
        print(f"  Total execution time: {result['pipeline_monitor'].get_summary()['elapsed_seconds']:.2f}s")
        print(f"  Peak RAM: {result['pipeline_monitor'].get_summary()['peak_ram_mb']:.2f} MB")
        
        # Generate reports
        generate_reports(infrastructure, "honey_pot_phase1")
        
        print("\n✓ Reports generated")
        print("\n" + "="*60)
        print("Files generated:")
        print("  - honey_pot_phase1.db (database)")
        print("  - honey_pot_phase1_output/results.json (results)")
        print("="*60 + "\n")
        
        sys.exit(0)
        
    except TimeoutError as e:
        print(f"\n✗ Pipeline timeout: {e}")
        print("  Run again to resume from last checkpoint")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Pipeline failed: {e}")
        print(f"  Error: {type(e).__name__}")
        print("  Run again to resume from last checkpoint")
        import traceback
        traceback.print_exc()
        sys.exit(1)
