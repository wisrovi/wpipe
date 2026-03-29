"""
Example 10: COMPLETE DASHBOARD - Full Feature Demo

This is the MASTER example demonstrating ALL features:
✓ Pipeline tracking with unique IDs (matrícula)
✓ YAML configuration generation
✓ Dashboard visualization
✓ Retry logic with configurable attempts
✓ Conditional branching
✓ Error handling and tracking
✓ Events and annotations
✓ Alert system with thresholds
✓ Pipeline relationships (parent/child)
✓ System metrics collection
✓ Performance comparison

Run this example to see the full power of wpipe tracking!
"""

import time
import random
from wpipe import Pipeline, PipelineTracker


def main():
    db_path = "complete_dashboard.db"
    config_dir = "./configs"

    print("=" * 70)
    print("  COMPLETE DASHBOARD - Full Feature Demo")
    print("=" * 70)
    print("""
    This example demonstrates:
    ✓ Pipeline tracking with unique IDs (matrícula)
    ✓ YAML configuration generation
    ✓ Retry logic with configurable attempts
    ✓ Conditional branching
    ✓ Error handling and tracking
    ✓ Events and annotations
    ✓ Alert system with thresholds
    ✓ Pipeline relationships (parent/child)
    ✓ System metrics collection
    ✓ Performance comparison
    """)

    # ============================================================
    # 1. SETUP ALERTS
    # ============================================================
    print("\n" + "=" * 70)
    print("  STEP 1: Configure Alert Thresholds")
    print("=" * 70)

    tracker = PipelineTracker(db_path, config_dir)

    tracker.add_alert_threshold(
        name="slow_pipeline",
        metric="pipeline_duration_ms",
        condition=">",
        value=3000,
        severity="warning",
        message="Pipeline took longer than 3 seconds",
    )

    tracker.add_alert_threshold(
        name="slow_step",
        metric="step_duration_ms",
        condition=">",
        value=1000,
        severity="warning",
        message="Step took longer than 1 second",
    )

    tracker.add_alert_threshold(
        name="critical_error",
        metric="error_rate",
        condition=">",
        value=0,
        severity="critical",
        message="Pipeline execution failed",
    )

    print("\n  ✓ Alerts configured:")
    for alert in tracker.get_alert_thresholds():
        print(
            f"    - {alert['name']}: {alert['metric']} {alert['condition']} {alert['value']}"
        )

    # ============================================================
    # 2. CREATE CHILD PIPELINES
    # ============================================================
    print("\n" + "=" * 70)
    print("  STEP 2: Create Child Pipelines")
    print("=" * 70)

    # Child Pipeline: Data Validation
    print("\n  [Creating] validation_pipeline...")
    validation_pipeline = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="data_validation",
        verbose=False,
    )
    validation_pipeline.set_steps(
        [
            (check_schema, "check_schema", "v1.0"),
            (validate_fields, "validate_fields", "v1.0"),
            (clean_invalid, "clean_invalid", "v1.0"),
        ]
    )

    # Child Pipeline: Data Transformation
    print("  [Creating] transformation_pipeline...")
    transformation_pipeline = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="data_transformation",
        verbose=False,
    )
    transformation_pipeline.set_steps(
        [
            (normalize_data, "normalize", "v1.0"),
            (enrich_data, "enrich", "v1.0"),
            (aggregate_data, "aggregate", "v1.0"),
        ]
    )

    # Child Pipeline: Data Export
    print("  [Creating] export_pipeline...")
    export_pipeline = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="data_export",
        verbose=False,
    )
    export_pipeline.set_steps(
        [
            (format_output, "format", "v1.0"),
            (compress_data, "compress", "v1.0"),
            (upload_to_storage, "upload", "v1.0"),
        ]
    )

    # ============================================================
    # 3. CREATE PARENT PIPELINE WITH CONDITIONAL + RETRY
    # ============================================================
    print("\n" + "=" * 70)
    print("  STEP 3: Create Parent Pipeline (Full Features)")
    print("=" * 70)

    # Define conditional logic
    data_quality_condition = Condition(
        expression="data_quality_score > 80",
        branch_true=[
            (validation_pipeline.run, "validation", "v1.0"),
            (transformation_pipeline.run, "transformation", "v1.0"),
        ],
        branch_false=[
            (quarantine_data, "quarantine", "v1.0"),
            (send_alert_notification, "alert_notification", "v1.0"),
        ],
    )

    parent_pipeline = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="etl_master_workflow",
        verbose=True,
        max_retries=2,
        retry_delay=1.0,
        retry_on_exceptions=(RuntimeError,),
        collect_system_metrics=True,  # Enable system metrics collection
    )

    parent_pipeline.set_steps(
        [
            (ingest_data, "ingest", "v1.0"),
            (calculate_quality_score, "quality_check", "v1.0"),
            data_quality_condition,
            (export_pipeline.run, "export", "v1.0"),
            (send_success_notification, "notification", "v1.0"),
        ]
    )

    # ============================================================
    # 4. RUN THE PIPELINE
    # ============================================================
    print("\n" + "=" * 70)
    print("  STEP 4: Execute Master Pipeline")
    print("=" * 70)
    print("\n  ⚙️  Running with:")
    print("      - Retry: 2 attempts")
    print("      - Conditional branching based on data quality")
    print("      - System metrics collection enabled")
    print("      - Alert monitoring active")
    print()

    try:
        result = parent_pipeline.run(
            {
                "source": "database",
                "records": [
                    {"id": 1, "name": "Alice", "score": 95},
                    {"id": 2, "name": "Bob", "score": 82},
                    {"id": 3, "name": "Charlie", "score": 71},
                    {"id": 4, "name": "Diana", "score": 88},
                    {"id": 5, "name": "Eve", "score": 91},
                ],
            }
        )

        print(f"\n  ✓ Pipeline completed successfully")
        print(f"  ✓ Pipeline ID: {parent_pipeline.pipeline_id}")
        print(f"  ✓ Result: {result}")

    except Exception as e:
        print(f"\n  ✗ Pipeline failed: {e}")
        print(f"  ✓ Pipeline ID: {parent_pipeline.pipeline_id}")
        print(f"  ✓ Error tracked in dashboard")

    # ============================================================
    # 5. ADD EVENTS
    # ============================================================
    print("\n" + "=" * 70)
    print("  STEP 5: Add Events/Annotations")
    print("=" * 70)

    if parent_pipeline.pipeline_id:
        parent_pipeline.add_event(
            event_type="milestone",
            event_name="processing_complete",
            message="Master ETL workflow completed all phases",
            data={"total_phases": 4},
            tags=["milestone", "etl"],
        )
        print("\n  ✓ Event added: processing_complete")

        parent_pipeline.add_event(
            event_type="annotation",
            event_name="quality_review",
            message="Data quality threshold was met - normal flow executed",
            tags=["quality", "annotation"],
        )
        print("  ✓ Event added: quality_review")

    # ============================================================
    # 6. RUN SECOND PIPELINE FOR COMPARISON
    # ============================================================
    print("\n" + "=" * 70)
    print("  STEP 6: Run Second Pipeline for Comparison")
    print("=" * 70)

    # Simulate a different run with lower quality data
    print("\n  [Running] Comparison pipeline (low quality data)...")

    comparison_pipeline = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="etl_master_workflow",
        verbose=False,
        collect_system_metrics=True,
    )
    comparison_pipeline.set_steps(
        [
            (ingest_data, "ingest", "v1.0"),
            (calculate_quality_score, "quality_check", "v1.0"),
            data_quality_condition,
            (export_pipeline.run, "export", "v1.0"),
            (send_success_notification, "notification", "v1.0"),
        ]
    )

    comparison_pipeline.run(
        {
            "source": "api",
            "records": [
                {"id": 1, "name": "Unknown", "score": 45},
                {"id": 2, "name": "Unknown", "score": 32},
            ],
        }
    )

    print(f"  ✓ Comparison pipeline ID: {comparison_pipeline.pipeline_id}")

    # ============================================================
    # 7. COMPARE EXECUTIONS
    # ============================================================
    print("\n" + "=" * 70)
    print("  STEP 7: Compare Pipeline Executions")
    print("=" * 70)

    comparison = tracker.compare_pipelines(
        parent_pipeline.pipeline_id, comparison_pipeline.pipeline_id
    )

    print(f"\n  Pipeline A ({comparison['pipeline_a']['name']}):")
    print(f"    ID: {comparison['pipeline_a']['id']}")
    print(f"    Status: {comparison['pipeline_a']['status']}")
    print(f"    Duration: {comparison['pipeline_a']['duration_ms']:.2f}ms")

    print(f"\n  Pipeline B ({comparison['pipeline_b']['name']}):")
    print(f"    ID: {comparison['pipeline_b']['id']}")
    print(f"    Status: {comparison['pipeline_b']['status']}")
    print(f"    Duration: {comparison['pipeline_b']['duration_ms']:.2f}ms")

    print(f"\n  Comparison:")
    print(
        f"    Duration diff: {comparison['duration_diff_ms']:.2f}ms ({comparison['duration_diff_percent']:+.1f}%)"
    )
    print(f"    Status changed: {comparison['status_changed']}")

    # ============================================================
    # 8. SHOW STATISTICS
    # ============================================================
    print("\n" + "=" * 70)
    print("  STEP 8: Statistics")
    print("=" * 70)

    stats = tracker.get_stats()
    print(f"\n  Total Pipelines: {stats['total_pipelines']}")
    print(f"  Completed: {stats['completed']}")
    print(f"  Errors: {stats['errors']}")
    print(f"  Success Rate: {stats['success_rate']}%")
    print(f"  Total Steps: {stats['total_steps']}")
    print(f"  Unacknowledged Alerts: {stats['unacknowledged_alerts']}")

    # Show alerts
    alerts = tracker.get_fired_alerts()
    if alerts:
        print(f"\n  Fired Alerts ({len(alerts)}):")
        for alert in alerts[:5]:
            print(
                f"    - [{alert['severity'].upper()}] {alert.get('alert_name', 'Unknown')}"
            )

    # ============================================================
    # FINISH
    # ============================================================
    print("\n" + "=" * 70)
    print("  DASHBOARD")
    print("=" * 70)
    print(f"""
    Database: {db_path}
    Configs: {config_dir}
    
    Run the dashboard with:
    
        python -m wpipe.dashboard \\
            --db {db_path} \\
            --config-dir {config_dir} \\
            --port 8035 \\
            --open
    
    The dashboard will show:
    ✓ Pipeline graph with execution flow
    ✓ Step-by-step input/output data
    ✓ Execution timeline
    ✓ Alert history
    ✓ Performance comparison
    ✓ System metrics charts
    ✓ YAML configurations
    ✓ Events timeline
    ✓ Pipeline relationships
    """)
    print("=" * 70)


# ============================================================
# STEP FUNCTIONS
# ============================================================


def ingest_data(d):
    """Ingest data from source."""
    print("    [ingest] Loading data from source...")
    time.sleep(0.3)
    return {
        "ingested_records": d.get("records", []),
        "source": d.get("source", "unknown"),
    }


def calculate_quality_score(d):
    """Calculate data quality score."""
    print("    [quality_check] Calculating quality score...")
    records = d.get("ingested_records", [])
    if not records:
        return {"data_quality_score": 0}

    # Calculate average score
    scores = [r.get("score", 0) for r in records]
    avg_score = sum(scores) / len(scores) if scores else 0

    time.sleep(0.2)
    return {"data_quality_score": avg_score}


def check_schema(d):
    """Check data schema."""
    print("      [check_schema] Validating schema...")
    time.sleep(0.1)
    return {"schema_valid": True}


def validate_fields(d):
    """Validate required fields."""
    print("      [validate_fields] Validating fields...")
    time.sleep(0.2)
    return {"fields_valid": True}


def clean_invalid(d):
    """Clean invalid records."""
    print("      [clean_invalid] Cleaning invalid records...")
    time.sleep(0.1)
    return {"cleaned": True}


def quarantine_data(d):
    """Quarantine low quality data."""
    print("      [quarantine] Quarantining low quality data...")
    time.sleep(0.2)
    return {"quarantined": True}


def send_alert_notification(d):
    """Send alert notification."""
    print("      [alert_notification] Sending alert notification...")
    time.sleep(0.1)
    return {"alert_sent": True}


def normalize_data(d):
    """Normalize data."""
    print("      [normalize] Normalizing data...")
    time.sleep(0.2)
    return {"normalized": True}


def enrich_data(d):
    """Enrich data with external info."""
    print("      [enrich] Enriching data...")
    time.sleep(0.3)
    return {"enriched": True}


def aggregate_data(d):
    """Aggregate data."""
    print("      [aggregate] Aggregating data...")
    time.sleep(0.2)
    return {"aggregated": True}


def format_output(d):
    """Format output."""
    print("      [format] Formatting output...")
    time.sleep(0.1)
    return {"formatted": True}


def compress_data(d):
    """Compress data."""
    print("      [compress] Compressing data...")
    time.sleep(0.2)
    return {"compressed": True}


def upload_to_storage(d):
    """Upload to storage."""
    print("      [upload] Uploading to storage...")
    time.sleep(0.3)
    return {"uploaded": True, "location": "s3://bucket/data.parquet"}


def send_success_notification(d):
    """Send success notification."""
    print("    [notification] Sending success notification...")
    time.sleep(0.1)
    return {"notified": True}


if __name__ == "__main__":
    main()
