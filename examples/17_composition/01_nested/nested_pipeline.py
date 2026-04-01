"""
Nested pipeline composition example.

Demonstrates using a pipeline as a step in another pipeline.
"""

from wpipe import Pipeline
from wpipe.composition import NestedPipelineStep


def extract_data(context):
    """ETL: Extract."""
    print("    [EXTRACT] Extracting data...")
    return {
        "raw_data": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "source": "database"
    }


def transform_data(context):
    """ETL: Transform."""
    print("    [TRANSFORM] Transforming data...")
    raw = context["raw_data"]
    transformed = [x * 2 for x in raw]
    return {"transformed_data": transformed}


def load_data(context):
    """ETL: Load."""
    print("    [LOAD] Loading data...")
    return {"loaded": True, "record_count": len(context["transformed_data"])}


def validate_results(context):
    """Validate ETL results."""
    print("  [VALIDATE] Validating ETL results...")
    return {"validation": "passed", "quality_score": 0.95}


def send_notification(context):
    """Send completion notification."""
    print("  [NOTIFY] Sending notification...")
    return {"notified": True, "recipients": 5}


if __name__ == "__main__":
    print("=== Pipeline Composition Example ===\n")
    
    # Create sub-pipeline (ETL)
    print("→ Creating ETL sub-pipeline...")
    etl_pipeline = Pipeline()
    etl_pipeline.add_state("extract", extract_data)
    etl_pipeline.add_state("transform", transform_data)
    etl_pipeline.add_state("load", load_data)
    
    # Create main pipeline
    print("→ Creating main pipeline...\n")
    main_pipeline = Pipeline()
    
    # Add sub-pipeline as a step
    etl_step = NestedPipelineStep(
        name="etl",
        pipeline=etl_pipeline,
    )
    
    # Add as step
    main_pipeline.add_state("etl", lambda ctx: etl_step.run(ctx))
    main_pipeline.add_state("validate", validate_results)
    main_pipeline.add_state("notify", send_notification)
    
    # Execute main pipeline
    print("→ Executing main pipeline...\n")
    result = main_pipeline.run({})
    
    print(f"\n✓ Pipeline completed!")
    print(f"  ETL execution time: {etl_step.get_execution_time():.3f}s")
    print(f"  Final result:")
    print(f"    - Validation: {result.get('validation')}")
    print(f"    - Quality: {result.get('quality_score')}")
    print(f"    - Notified: {result.get('notified')}")
    print(f"    - Records: {result.get('record_count')}")
