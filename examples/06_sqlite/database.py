"""
Example: SQLite Database Integration

This example demonstrates how to use SQLite with wpipe for
persistent storage of pipeline execution results.
"""

from wpipe.pipe import Pipeline
from wpipe.sqlite import Wsqlite


def step1(data: dict) -> dict:
    """First step of the pipeline."""
    return {"step1_result": "completed", "value": 100}


def step2(data: dict) -> dict:
    """Second step of the pipeline."""
    return {"step2_result": "completed", "processed_value": data["value"] * 2}


def step3(data: dict) -> dict:
    """Third step of the pipeline."""
    return {"step3_result": "completed", "final_value": data["processed_value"] + 50}


def main():
    """Demonstrate SQLite integration with Pipeline."""
    pipeline = Pipeline(verbose=True)
    pipeline.set_steps(
        [
            (step1, "Step 1", "v1.0"),
            (step2, "Step 2", "v1.0"),
            (step3, "Step 3", "v1.0"),
        ]
    )

    db_name = "example_pipeline.db"

    with Wsqlite(db_name=db_name) as db:
        input_data = {"x": 10, "y": "test"}
        db.input = input_data

        print("Running pipeline...")
        result = pipeline.run(input_data)

        db.output = result

        print(f"Pipeline result: {result}")
        print(f"Database record ID: {db.id}")

    print("\nVerifying database contents...")
    from wpipe.sqlite.Sqlite import SQLite

    with SQLite(db_name=db_name) as sqlite:
        df = sqlite.export_to_dataframe()
        print(f"Total records: {sqlite.count_records()}")
        print(df)


if __name__ == "__main__":
    main()
