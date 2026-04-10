"""
Example 05: Nested Pipelines

Demonstrates how to compose pipelines from other pipelines.
Parent-child relationships are tracked automatically.
"""

from wpipe import Pipeline


def main():
    db_path = "../wpipe_dashboard.db"
    config_dir = "../configs"

    print("=" * 60)
    print("Example 08: Nested Pipelines")
    print("=" * 60)

    # Create child pipeline (data extraction)
    extract_pipeline = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="extract_data",
        verbose=False,
    )
    extract_pipeline.set_steps(
        [
            (connect_source, "connect_source", "v1.0"),
            (fetch_records, "fetch_records", "v1.0"),
            (parse_data, "parse_data", "v1.0"),
        ]
    )

    # Create child pipeline (data transformation)
    transform_pipeline = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="transform_data",
        verbose=False,
    )
    transform_pipeline.set_steps(
        [
            (clean_data, "clean_data", "v1.0"),
            (normalize_data, "normalize_data", "v1.0"),
            (validate_data, "validate_data", "v1.0"),
        ]
    )

    # Create child pipeline (data loading)
    load_pipeline = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="load_data",
        verbose=False,
    )
    load_pipeline.set_steps(
        [
            (prepare_target, "prepare_target", "v1.0"),
            (insert_records, "insert_records", "v1.0"),
            (verify_load, "verify_load", "v1.0"),
        ]
    )

    # Create parent pipeline (ETL orchestration)
    etl_pipeline = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="etl_orchestration",
        verbose=True,
    )

    etl_pipeline.set_steps(
        [
            (extract_pipeline.run, "extract_phase", "v1.0"),
            (transform_pipeline.run, "transform_phase", "v1.0"),
            (load_pipeline.run, "load_phase", "v1.0"),
            (generate_report, "generate_report", "v1.0"),
        ]
    )

    print("\n[Running ETL Pipeline...]\n")
    result = etl_pipeline.run({"source": "database", "target": "warehouse"})

    print(f"\n[Result] Records processed: {result.get('total_records', 0)}")
    print(
        f"\n[Dashboard] Run: cd .. && python -m wpipe.dashboard --db wpipe_dashboard.db --config-dir configs --open"
    )


# Step functions
def connect_source(d):
    """Connect to data source."""
    print("  [connect_source] Connecting to source...")
    return {"connected": True, "source": d.get("source")}


def fetch_records(d):
    """Fetch records from source."""
    print("  [fetch_records] Fetching 100 records...")
    return {"raw_records": [{"id": i, "value": f"record_{i}"} for i in range(100)]}


def parse_data(d):
    """Parse fetched data."""
    print(f"  [parse_data] Parsing {len(d['raw_records'])} records...")
    return {"parsed_records": d["raw_records"]}


def clean_data(d):
    """Clean data."""
    print("  [clean_data] Cleaning data...")
    return {"cleaned_records": d["parsed_records"]}


def normalize_data(d):
    """Normalize data."""
    print("  [normalize_data] Normalizing data...")
    return {"normalized_records": d["cleaned_records"]}


def validate_data(d):
    """Validate data."""
    print("  [validate_data] Validating data...")
    return {"validated_records": d["normalized_records"]}


def prepare_target(d):
    """Prepare target database."""
    print(f"  [prepare_target] Preparing {d.get('target')}...")
    return {"target_ready": True}


def insert_records(d):
    """Insert records into target."""
    print(f"  [insert_records] Inserting {len(d['validated_records'])} records...")
    return {"inserted": len(d["validated_records"])}


def verify_load(d):
    """Verify data load."""
    print("  [verify_load] Verifying data load...")
    return {"verified": True}


def generate_report(d):
    """Generate execution report."""
    print("  [generate_report] Generating report...")
    return {"total_records": d.get("inserted", 0), "report_generated": True}


if __name__ == "__main__":
    main()
