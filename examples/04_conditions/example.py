"""
Example 04: Conditional Branching

Demonstrates conditional branching in pipelines.
Different code paths are taken based on data values, all tracked.
"""

from wpipe import Pipeline, Condition


def main():
    db_path = "conditions.db"
    config_dir = "./configs"

    print("=" * 60)
    print("Example 04: Conditional Branching")
    print("=" * 60)

    # Run multiple pipelines with different inputs to show branches
    test_cases = [
        {"temperature": 25, "name": "Warm Day"},
        {"temperature": 5, "name": "Cold Day"},
        {"temperature": 35, "name": "Hot Day"},
    ]

    for i, test_data in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {test_data['name']} ---")

        pipeline = Pipeline(
            tracking_db=db_path,
            config_dir=config_dir,
            pipeline_name=f"weather_check_{i}",
            verbose=False,
        )

        # Define conditional branches
        hot_condition = Condition(
            expression="temperature > 30",
            branch_true=[(activate_cooling, "activate_cooling", "v1.0")],
            branch_false=[
                Condition(
                    expression="temperature < 10",
                    branch_true=[(activate_heating, "activate_heating", "v1.0")],
                    branch_false=[(normal_operation, "normal_operation", "v1.0")],
                )
            ],
        )

        pipeline.set_steps(
            [
                (read_temperature, "read_temperature", "v1.0"),
                hot_condition,
                (log_result, "log_result", "v1.0"),
            ]
        )

        result = pipeline.run(test_data)
        print(f"  Result: {result.get('action', 'unknown')}")

    print(
        f"\n[Dashboard] Run: python -m wpipe.dashboard --db {db_path} --config-dir {config_dir} --open"
    )


# Step functions
def read_temperature(d):
    """Read temperature from input."""
    temp = d.get("temperature", 20)
    print(f"  [read_temperature] Temperature: {temp}°C")
    return {"temperature": temp}


def activate_cooling(d):
    """Activate cooling system."""
    print(f"  [activate_cooling] Activating cooling for {d['temperature']}°C")
    return {"action": "cooling_activated", "system": "AC"}


def activate_heating(d):
    """Activate heating system."""
    print(f"  [activate_heating] Activating heating for {d['temperature']}°C")
    return {"action": "heating_activated", "system": "heater"}


def normal_operation(d):
    """Normal operation mode."""
    print(f"  [normal_operation] Normal operation at {d['temperature']}°C")
    return {"action": "normal", "system": "none"}


def log_result(d):
    """Log the result."""
    print(f"  [log_result] Final action: {d.get('action', 'unknown')}")
    return {"logged": True}


if __name__ == "__main__":
    main()
