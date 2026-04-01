"""
ETL pipeline using composition example.

Demonstrates building an Extract-Transform-Load (ETL) pipeline by
composing three focused sub-pipelines that each handle one phase.
"""

from wpipe import Pipeline
from wpipe.composition import NestedPipelineStep


def create_extract_pipeline():
    """Extract phase: Read from source."""
    pipeline = Pipeline()
    
    pipeline.add_state("read_source", lambda c: {
        "raw_data": [
            {"id": 1, "name": " Alice ", "age": "28"},
            {"id": 2, "name": " Bob ", "age": "35"},
            {"id": 3, "name": " Charlie ", "age": "invalid"},
        ]
    })
    
    return pipeline


def create_transform_pipeline():
    """Transform phase: Clean and enrich data."""
    pipeline = Pipeline()
    
    pipeline.add_state("clean_data", lambda c: {
        "cleaned_data": [
            {
                "id": item["id"],
                "name": item["name"].strip(),
                "age": int(item["age"]) if item["age"].isdigit() else None
            }
            for item in c.get("raw_data", [])
            if item["age"].isdigit()
        ]
    })
    
    pipeline.add_state("enrich_data", lambda c: {
        "enriched_data": [
            {**item, "processed": True, "segment": "premium" if item["age"] > 30 else "standard"}
            for item in c.get("cleaned_data", [])
        ]
    })
    
    return pipeline


def create_load_pipeline():
    """Load phase: Save to destination."""
    pipeline = Pipeline()
    
    pipeline.add_state("validate_schema", lambda c: {
        "validation_passed": all(
            all(k in item for k in ["id", "name", "age", "processed"])
            for item in c.get("enriched_data", [])
        )
    })
    
    pipeline.add_state("save_data", lambda c: {
        "records_saved": len(c.get("enriched_data", [])) if c.get("validation_passed") else 0,
        "status": "success" if c.get("validation_passed") else "failed"
    })
    
    return pipeline


def create_etl_pipeline():
    """Main ETL pipeline using composition."""
    main = Pipeline()
    
    # Extract phase
    extract_sub = create_extract_pipeline()
    extract_step = NestedPipelineStep("extract", extract_sub)
    main.add_state("extract", lambda c: extract_step.run(c))
    
    # Transform phase
    transform_sub = create_transform_pipeline()
    transform_step = NestedPipelineStep("transform", transform_sub)
    main.add_state("transform", lambda c: transform_step.run(c))
    
    # Load phase
    load_sub = create_load_pipeline()
    load_step = NestedPipelineStep("load", load_sub)
    main.add_state("load", lambda c: load_step.run(c))
    
    # Final report
    main.add_state("report", lambda c: {
        "etl_status": "complete",
        "records_saved": c.get("records_saved", 0),
        "pipeline_status": c.get("status", "unknown")
    })
    
    return main


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("ETL PIPELINE WITH COMPOSITION")
    print("=" * 60)
    
    etl_pipeline = create_etl_pipeline()
    result = etl_pipeline.run({})
    
    print("\n✓ ETL Results:")
    print(f"  Status: {result.get('etl_status')}")
    print(f"  Records processed: {result.get('records_saved')}")
    print(f"  Pipeline: {result.get('pipeline_status')}")
    print("=" * 60 + "\n")
