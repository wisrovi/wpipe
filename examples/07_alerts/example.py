"""
Example 07: Alert System

Demonstrates the alert system with configurable thresholds.
Alerts are triggered when metrics exceed defined limits.
"""

import time
from wpipe import Pipeline, PipelineTracker


def main():
    db_path = "alerts_example.db"
    config_dir = "./configs"

    print("=" * 60)
    print("Example 07: Alert System")
    print("=" * 60)

    # Configure alert thresholds
    tracker = PipelineTracker(db_path, config_dir)

    # Alert for slow pipelines (> 2 seconds)
    tracker.add_alert_threshold(
        name="slow_pipeline",
        metric="pipeline_duration_ms",
        condition=">",
        value=2000,
        severity="warning",
        message="Pipeline execution exceeded 2 seconds",
    )

    # Alert for very slow steps (> 500ms)
    tracker.add_alert_threshold(
        name="slow_step",
        metric="step_duration_ms",
        condition=">",
        value=500,
        severity="warning",
        message="Step execution exceeded 500ms",
    )

    # Alert for critical errors
    tracker.add_alert_threshold(
        name="pipeline_error",
        metric="error_rate",
        condition=">",
        value=0,
        severity="critical",
        message="Pipeline execution failed",
    )

    print("\nAlert Thresholds Configured:")
    alerts = tracker.get_alert_thresholds()
    for alert in alerts:
        print(
            f"  - {alert['name']}: {alert['metric']} {alert['condition']} {alert['value']} ({alert['severity']})"
        )

    # Run pipelines that will trigger alerts
    print("\n[Running Pipelines...]\n")

    # Pipeline 1: Fast (no alerts)
    print("Pipeline 1: Fast execution")
    p1 = Pipeline(
        tracking_db=db_path, config_dir=config_dir, pipeline_name="fast_pipeline"
    )
    p1.set_steps([(quick_step, "quick", "v1.0")])
    p1.run({"data": 1})
    print("  -> Completed quickly\n")

    # Pipeline 2: Slow (triggers duration alert)
    print("Pipeline 2: Slow execution (triggers alert)")
    p2 = Pipeline(
        tracking_db=db_path, config_dir=config_dir, pipeline_name="slow_pipeline"
    )
    p2.set_steps([(slow_step, "slow", "v1.0")])
    p2.run({"data": 2})
    print("  -> Completed slowly\n")

    # Pipeline 3: Error (triggers error alert)
    print("Pipeline 3: Error (triggers error alert)")
    p3 = Pipeline(
        tracking_db=db_path, config_dir=config_dir, pipeline_name="error_pipeline"
    )
    p3.set_steps([(failing_step, "fail", "v1.0")])
    try:
        p3.run({"data": 3})
    except:
        pass
    print("  -> Failed as expected\n")

    # Show fired alerts
    print("\nFired Alerts:")
    fired = tracker.get_fired_alerts(limit=10)
    for alert in fired:
        print(
            f"  - [{alert['severity'].upper()}] {alert.get('alert_name', 'Unknown')}: {alert['message']}"
        )

    print(
        f"\n[Dashboard] Run: python -m wpipe.dashboard --db {db_path} --config-dir {config_dir} --open"
    )


def quick_step(d):
    """Quick step."""
    return {"result": "quick"}


def slow_step(d):
    """Slow step that triggers duration alert."""
    time.sleep(2.5)  # Sleep to trigger slow alert
    return {"result": "slow"}


def failing_step(d):
    """Failing step."""
    raise RuntimeError("Intentional failure for alert demo")


if __name__ == "__main__":
    main()
