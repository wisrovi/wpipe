"""
Example 08: Pipeline Relationships

Demonstrates how to establish relationships between pipelines.
Shows parent-child and sibling relationships in the dashboard.
"""

from wpipe import Pipeline


def main():
    db_path = "relations_example.db"
    config_dir = "./configs"

    print("=" * 60)
    print("Example 08: Pipeline Relationships")
    print("=" * 60)

    # Parent pipeline - orchestrates the workflow
    print("\n[Creating Pipeline Hierarchy]")

    # Child pipeline 1: Data Collection
    collector = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="data_collector",
        verbose=False,
    )
    collector.set_steps(
        [
            (collect_from_api, "collect_api", "v1.0"),
            (validate_collection, "validate_collection", "v1.0"),
        ]
    )

    # Child pipeline 2: Data Processing
    processor = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="data_processor",
        verbose=False,
    )
    processor.set_steps(
        [
            (transform_data, "transform", "v1.0"),
            (enrich_data, "enrich", "v1.0"),
            (aggregate_data, "aggregate", "v1.0"),
        ]
    )

    # Child pipeline 3: Data Export
    exporter = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="data_exporter",
        verbose=False,
    )
    exporter.set_steps(
        [
            (format_output, "format", "v1.0"),
            (write_to_file, "write", "v1.0"),
        ]
    )

    # Parent pipeline - orchestrates all
    parent = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="data_workflow",
        verbose=True,
    )

    parent.set_steps(
        [
            (collector.run, "collect_phase", "v1.0"),
            (processor.run, "process_phase", "v1.0"),
            (exporter.run, "export_phase", "v1.0"),
            (send_notification, "notification", "v1.0"),
        ]
    )

    print("\n[Running Parent Pipeline...]\n")
    result = parent.run({"source": "api", "destination": "file"})

    print(f"\n[Result] {result}")

    # Manually link additional relationships
    if parent.pipeline_id and collector.pipeline_id:
        parent.link_to_pipeline(collector.pipeline_id, "parent_of")

    print(
        f"\n[Dashboard] Run: python -m wpipe.dashboard --db {db_path} --config-dir {config_dir} --open"
    )


# Step functions
def collect_from_api(d):
    """Collect data from API."""
    print("  [collect_api] Collecting data from API...")
    return {"records": [{"id": i, "value": i * 10} for i in range(10)]}


def validate_collection(d):
    """Validate collected data."""
    print("  [validate_collection] Validating collection...")
    return {"valid": True, "count": len(d["records"])}


def transform_data(d):
    """Transform data."""
    print("  [transform] Transforming data...")
    return {
        "transformed": [{"id": r["id"], "value": r["value"] * 2} for r in d["records"]]
    }


def enrich_data(d):
    """Enrich data with additional info."""
    print("  [enrich] Enriching data...")
    return {
        "enriched": [
            {**r, "category": "A" if r["id"] < 5 else "B"} for r in d["transformed"]
        ]
    }


def aggregate_data(d):
    """Aggregate data by category."""
    print("  [aggregate] Aggregating data...")
    categories = {}
    for r in d["enriched"]:
        cat = r["category"]
        categories[cat] = categories.get(cat, 0) + r["value"]
    return {"aggregated": categories}


def format_output(d):
    """Format output data."""
    print("  [format] Formatting output...")
    return {"formatted": {"summary": d["aggregated"], "timestamp": "2024-01-01"}}


def write_to_file(d):
    """Write to file."""
    print("  [write] Writing to file...")
    return {"written": True, "path": "/tmp/output.json"}


def send_notification(d):
    """Send notification."""
    print("  [notification] Sending notification...")
    return {"notified": True}


if __name__ == "__main__":
    main()
