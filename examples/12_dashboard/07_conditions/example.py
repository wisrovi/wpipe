"""
Example 07: Conditional Branching

Demonstrates conditional branching in pipelines.
Different code paths are taken based on data values, all tracked.
Shows both branches in the dashboard graph.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from states import cooling_on, fan_high, heating_on, log_action, read_temp

from wpipe import Condition, Pipeline


def main():
    db_path = "../wpipe_dashboard.db"
    config_dir = "../configs"

    print("=" * 60)
    print("Example 07: Conditional Branching")
    print("=" * 60)

    # Test Case 1: Hot Day (>30) - activates cooling
    print("\n--- Test Case 1: Hot Day (temperature=35) ---")
    pipeline1 = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="weather_hot",
        verbose=False,
    )
    pipeline1.set_steps(
        [
            (read_temp, "read_temp", "v1.0"),
            Condition(
                expression="temp > 30",
                branch_true=[
                    (cooling_on, "cooling_on", "v1.0"),
                    (fan_high, "fan_high", "v1.0"),
                ],
                branch_false=[(heating_on, "heating_on", "v1.0")],
            ),
            (log_action, "log_action", "v1.0"),
        ]
    )
    r1 = pipeline1.run({"temp": 35})
    print(f"  Result: {r1.get('action', 'unknown')}")

    # Test Case 2: Cold Day (<10) - activates heating
    print("\n--- Test Case 2: Cold Day (temperature=5) ---")
    pipeline2 = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="weather_cold",
        verbose=False,
    )
    pipeline2.set_steps(
        [
            (read_temp, "read_temp", "v1.0"),
            Condition(
                expression="temp > 30",
                branch_true=[
                    (cooling_on, "cooling_on", "v1.0"),
                    (fan_high, "fan_high", "v1.0"),
                ],
                branch_false=[(heating_on, "heating_on", "v1.0")],
            ),
            (log_action, "log_action", "v1.0"),
        ]
    )
    r2 = pipeline2.run({"temp": 5})
    print(f"  Result: {r2.get('action', 'unknown')}")

    # Test Case 3: Normal Day (10-30) - neither
    print("\n--- Test Case 3: Normal Day (temperature=20) ---")
    pipeline3 = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="weather_normal",
        verbose=False,
    )
    pipeline3.set_steps(
        [
            (read_temp, "read_temp", "v1.0"),
            Condition(
                expression="temp > 30",
                branch_true=[
                    (cooling_on, "cooling_on", "v1.0"),
                    (fan_high, "fan_high", "v1.0"),
                ],
                branch_false=[(heating_on, "heating_on", "v1.0")],
            ),
            (log_action, "log_action", "v1.0"),
        ]
    )
    r3 = pipeline3.run({"temp": 20})
    print(f"  Result: {r3.get('action', 'unknown')}")

    print("\n" + "=" * 60)
    print("[Dashboard] Shows both TRUE and FALSE branches")
    print("  - Hot: cooling_on + fan_high executed (heating_on skipped)")
    print("  - Cold: heating_on executed (cooling_on + fan_high skipped)")
    print("  - Normal: heating_on executed (cooling_on + fan_high skipped)")
    print("=" * 60)
    print(
        f"\n[Dashboard] Run: cd .. && python -m wpipe.dashboard --db wpipe_dashboard.db --config-dir configs --open"
    )


if __name__ == "__main__":
    main()
