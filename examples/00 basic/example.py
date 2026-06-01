"""
Example demonstrating a basic pipeline for a car journey.

This script defines a simple pipeline that simulates a car journey,
including steps like refueling and driving. Uses wpipe Pipeline.
"""

from typing import Any, Dict

from wpipe import Pipeline, step


class Refuel:
    NAME = "refuel"
    VERSION = "v1.0"
    def __call__(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data["gasoline_level"] = "high"
        print("Refueling car...")
        return data


class ChangeOil:
    NAME = "change_oil"
    VERSION = "v1.0"
    def __call__(self, data: Dict[str, Any]) -> Dict[str, Any]:
        data["oil_level"] = "high"
        print("Changing oil...")
        return data


class Drive:
    NAME = "drive"
    VERSION = "v1.0"
    def __call__(self, data: Dict[str, Any]) -> Dict[str, Any]:
        print(f"Driving car... (gasoline: {data.get('gasoline_level', 'unknown')})")
        data["distance"] = data.get("distance", 0) + 100
        return data


def main() -> None:
    """Sets up and runs a car journey pipeline."""
    journey_pipeline = Pipeline(
        pipeline_name="journey",
        verbose=False,
    )

    journey_pipeline.set_steps([
        (Refuel(), "refuel", "v1.0"),
        (ChangeOil(), "change_oil", "v1.0"),
        (Drive(), "drive", "v1.0"),
    ])

    result = journey_pipeline.run({"gasoline_level": "low", "distance": 0})
    print(f"Results: {result}")


if __name__ == "__main__":
    main()