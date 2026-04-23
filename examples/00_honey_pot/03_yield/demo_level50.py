"""
DEMO LEVEL 50: CAR PIPELINE FINAL INTEGRATION
---------------------------------------------
Adds: Comprehensive integration of multiple features.
Accumulates: All previous levels.
"""

import json
import os
import random
import tempfile
import threading
from pathlib import Path
from typing import Any, Dict

import cv2
from dto.car import Car
from states.car_info_printer import CarInfoPrinter
from states.change_oil import change_oil
from states.drive import drive
from states.deflate_tires import deflate_tires
from states.preparation import preparation_phase
from states.refuel import refuel
from states.inflate_tires import inflate_tires
from states.car_info_printer import nested_step
from states.print_fuel_level import print_fuel_level

from wpipe import (
    Condition,
    For,
    Metric,
    Parallel,
    Pipeline,
    PipelineExporter,
    ResourceMonitor,
    Severity,
    TaskTimer,
    auto_dict_input,
    step,
)
from wpipe.sqlite import Wsqlite


@step(name="check_lights", version="v1.0")
def check_lights(data: Any) -> Any:
    """Check vehicle lights.

    Args:
        data: Input data for the step.

    Returns:
        Any: Unchanged input data.
    """
    print("     * Checking front and rear lights... OK")
    return data


@step(name="random_flat_tire", version="v1.0", retry_count=10, retry_delay=0.01)
def random_flat_tire(data: Any) -> Any:
    """Simulate a random flat tire with retries.

    Args:
        data: Input data for the step.

    Returns:
        Any: Unchanged input data.

    Raises:
        RuntimeError: If a puncture is simulated.
    """
    if random.random() < 0.5:
        raise RuntimeError("Random puncture")
    return data


@step(name="notify_telegram_error", version="v1.0")
def notify_telegram_error(context, error: Dict[str, Any]) -> Any:
    """Notify error via simulated Telegram message.

    Args:
        context: The current pipeline context.
        error: Error details.

    Returns:
        Any: Unchanged context.
    """
    print("\n" + "!" * 60)
    print("🚨 SYSTEM ALERT: ERROR DETECTED")
    print("!" * 60)
    print(f"📍 FAILED STATE: {error['step_name']}")
    print(f"📄 FILE: {error['file_path']}")
    print(f"🔢 LINE: {error['line_number']}")
    print(f"⚠️ MESSAGE: {error['error_message']}")
    print("-" * 60)
    return context


def get_trip_pipeline(db_path: str) -> Pipeline:
    """Configures and returns the main trip pipeline.

    Args:
        db_path: Path to the tracking database.

    Returns:
        Pipeline: Configured pipeline.
    """
    trip = Pipeline(
        pipeline_name="trip",
        verbose=False,
        tracking_db=db_path,
        max_retries=3,
        retry_delay=0,
        retry_on_exceptions=(RuntimeError),
        collect_system_metrics=True,
        show_progress=True,
    )

    trip.add_error_capture([notify_telegram_error])

    trip.tracker.add_alert_threshold(
        metric=Metric.PIPELINE_DURATION,
        expression=">500",
        severity=Severity.CRITICAL,
        steps=[CarInfoPrinter(">>> [ALERT] Global performance protocol activated")],
    )

    trip.tracker.add_alert_threshold(
        metric=Metric.STEP_DURATION,
        expression=">1000",
        severity=Severity.WARNING,
        steps=[(lambda d: print(">>> [ALERT] Slow step detected"), "Audit" "v1.0")],
    )

    trip.add_event(
        event_type="notification",
        event_name="authorized_person",
        message="Results sent to external APIs",
        steps=[CarInfoPrinter(">>> [HOOK] Trip finished sending final summary...")],
    )

    trip.add_checkpoint(
        checkpoint_name="trip_start",
        expression="True",
        steps=[CarInfoPrinter(">>> [CHECKPOINT] Trip start")],
    )

    trip.add_checkpoint(
        checkpoint_name="low_fuel",
        expression="fuel_level == 'Low'",
        steps=[CarInfoPrinter(">>> [CHECKPOINT] Low fuel alert detected")],
    )

    trip.set_steps(
        [
            preparation_phase,
            For(
                iterations=3,
                steps=[
                    CarInfoPrinter("--- New trip ---" "_loop_iteration"),
                    Parallel(steps=[refuel, change_oil, check_lights], max_workers=3),
                    nested_step,
                    For(
                        validation_expression="fuel_level != 'Empty'",
                        steps=[
                            drive,
                            Condition(
                                expression="tire_level == 'Low'",
                                branch_true=[nested_step, inflate_tires],
                                branch_false=[deflate_tires],
                            ),
                            random_flat_tire,
                        ],
                    ),
                    (
                        lambda c: print(
                            f"[non_serializable_obj]: {c.get('non_serializable_obj')}",
                            "non_serializable_obj" "v1.0",
                        )
                    ),
                ],
            ),
        ]
    )
    return trip


def export_logs_to_json(exporter: PipelineExporter, output_path: str) -> None:
    """Export logs to JSON format.

    Args:
        exporter: PipelineExporter instance.
        output_path: Path to save the JSON file.
    """
    print("\n" + "=" * 70)
    print("JSON EXPORT")
    print("=" * 70)

    try:
        json_data = exporter.export_pipeline_logs(export_format="json")
        if json_data:
            Path(output_path).write_text(json_data, encoding="utf-8")
            print(f"✓ Exported to: {output_path}")
            data = json.loads(json_data)
            if isinstance(data, list) and data:
                print(f"  Records: {len(data)}")
        else:
            print("ℹ No execution data to export yet")
    except Exception as e:
        print(f"ℹ JSON export error: {e}")


def export_logs_to_csv(exporter: PipelineExporter, output_path: str) -> None:
    """Export logs to CSV format.

    Args:
        exporter: PipelineExporter instance.
        output_path: Path for CSV output.
    """
    print("\n" + "=" * 70)
    print("CSV EXPORT")
    print("=" * 70)

    try:
        csv_data = exporter.export_pipeline_logs(export_format="csv")
        if csv_data:
            csv_path = output_path.replace(".json", ".csv")
            Path(csv_path).write_text(csv_data, encoding="utf-8")
            print(f"✓ Exported to: {csv_path}")
        else:
            print("ℹ No execution data to export yet")
    except Exception as e:
        print(f"ℹ CSV export error: {e}")


def run_exporter_demo(db_path: str) -> None:
    """Run data export demonstration.

    Args:
        db_path: Path to the tracking database.
    """
    output_dir = "output/export_output"
    Path(output_dir).mkdir(exist_ok=True)
    exporter = PipelineExporter(db_path)

    print("=" * 70)
    print("EXPORTING DATA")
    print("=" * 70 + "\n")

    stats_path = os.path.join(output_dir, "pipeline_statistics.json")
    try:
        exporter.export_statistics(export_format="json", output_path=stats_path)
        print(f"   ✓ Stats saved to: {stats_path}\n")
    except Exception as e:
        print(f"   ⚠ Stats export note: {e}\n")

    logs_json_path = os.path.join(output_dir, "pipeline_logs.json")
    export_logs_to_json(exporter, logs_json_path)
    export_logs_to_csv(exporter, logs_json_path)


def create_complex_handler() -> Any:
    """Creates a complex handler object holding system resources.

    Returns:
        Any: InternalSystemHandler instance.
    """

    class InternalSystemHandler:
        """Manages threading lock and temporary file."""

        def __init__(self):
            """Check lights step.

            Args:

                data: Input data for the step.

            Returns:

                dict: Result of the step.

            """
            self.lock = threading.Lock()
            self.resource = tempfile.NamedTemporaryFile(mode="w+")
            self.data = "Sensitive Runtime State"

        def __repr__(self):
            return "<InternalSystemHandler active>"

    return InternalSystemHandler()


def main() -> None:
    """Main execution entry point."""
    db_path = "output/wpipe_dashboard.db"
    with ResourceMonitor("Full_Trip") as monitor:
        with TaskTimer("trip_pipeline", timeout_seconds=30) as timer:
            trip = get_trip_pipeline(db_path)

            @auto_dict_input
            def run_pipeline(car_dict: Dict[str, Any]) -> Dict[str, Any]:
                car_dict["non_serializable_obj"] = create_complex_handler()
                return trip.run(car_dict)

            car = Car(make="Toyota", model="Corolla")
            results = run_pipeline(car)

    print(f"\nResource Summary:")
    summary = monitor.get_summary()
    print(f"  - Peak RAM: {summary['peak_ram_mb']} MB")
    print(f"  - Avg CPU: {summary['avg_cpu_percent']}%")
    print(f"✓ Total time monitored: {timer.elapsed_seconds:.2f}s")

    print(f"\nTrips completed: {results.get('_loop_iteration')}")
    print(f"Final fuel: {results.get('fuel_level')}")

    fired = trip.tracker.get_fired_alerts(limit=10)
    for alert in fired:
        print(
            f"  - [{alert['severity'].upper()}] {alert.get('alert_name')}: {alert['message']}"
        )

    run_exporter_demo(db_path)

    print("\n" + "=" * 70)
    print("📊 PERFORMANCE ANALYSIS")
    print("=" * 70)
    analysis = trip.tracker.analysis
    stats = analysis.get_stats()
    print(f"\nGlobal Summary:\n  - Total Executions: {stats['total_pipelines']}")
    print(f"  - Success Rate: {stats['success_rate']}%")


def test_wsqlite() -> None:
    """Test Wsqlite functionality."""
    image = cv2.imread("images.jpeg")
    with Wsqlite(db_name="output/demo.db") as db:
        db.input = {"inference": {"source": image}, "conf": 0.5}
        db.details = {"info": "Starting the process..."}
        db.output = {"status": "success"}


if __name__ == "__main__":
    test_wsqlite()
    main()
