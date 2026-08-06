"""
Demo 04: save_json_input_output
-------------------------------
Shows how to enable/disable persisting the input/output JSON blobs of the
pipeline and its executed steps in the tracking database.

- save_json_input_output=False (default is True): the pipeline runs normally
  but steps/pipelines store NULL in input_data / output_data, keeping the
  database small when those payloads are heavy.
- The dashboard tolerates the missing payloads and renders "N/A" for
  Input/Output in the step details.

Run:
    python example.py

It inspects the tracking database after each run and asserts the expected
storage behavior for both configurations.
"""

import os
import sqlite3
import sys
import tempfile

from wpipe import Pipeline


def load_cargo(data: dict) -> dict:
    """Load the truck cargo.

    Args:
        data: Pipeline context.

    Returns:
        dict: Cargo status merged with a heavy payload to mimic real data.
    """
    heavy_payload = {"boxes": list(range(500)), "fragile": True}
    return {"cargo": "loaded", "payload": heavy_payload}


def drive(data: dict) -> dict:
    """Drive the truck.

    Args:
        data: Pipeline context.

    Returns:
        dict: Trip status.
    """
    return {"km": (data.get("km", 0) or 0) + 120, "status": "arrived"}


def park(data: dict) -> dict:
    """Park the truck.

    Args:
        data: Pipeline context.

    Returns:
        dict: Final parking status.
    """
    return {"parked": True, "km": data.get("km", 0)}


def run_pipeline(db_path: str, config_dir: str, name: str, save_json: bool) -> str:
    """Run the pipeline once with the given storage setting.

    Args:
        db_path: Path to the tracking database.
        config_dir: Directory for pipeline YAML configurations.
        name: Pipeline name.
        save_json: Whether input/output JSON should be persisted.

    Returns:
        str: The registered pipeline ID.
    """
    pipeline = Pipeline(
        pipeline_name=name,
        tracking_db=db_path,
        config_dir=config_dir,
        save_json_input_output=save_json,
        verbose=False,
    )
    pipeline.set_steps([load_cargo, drive, park])
    pipeline.run({"trip": "A", "driver": "Ada"})
    return pipeline.pipeline_id


def fetch_storage(pipeline_id: str, db_path: str) -> dict:
    """Read the stored input/output payloads for a pipeline execution.

    Args:
        pipeline_id: Pipeline ID to inspect.
        db_path: Path to the tracking database.

    Returns:
        dict: The input_data/output_data cells for the pipeline and its steps.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        pipeline = conn.execute(
            "SELECT input_data, output_data FROM pipelines WHERE id = ?",
            (pipeline_id,),
        ).fetchone()
        steps = conn.execute(
            "SELECT input_data, output_data FROM steps WHERE pipeline_id = ?",
            (pipeline_id,),
        ).fetchall()
    finally:
        conn.close()

    return {
        "pipeline_input": pipeline["input_data"] if pipeline else None,
        "pipeline_output": pipeline["output_data"] if pipeline else None,
        "step_inputs": [step["input_data"] for step in steps],
        "step_outputs": [step["output_data"] for step in steps],
    }


def assert_case(case_name: str, storage: dict, expected_saved: bool) -> None:
    """Assert that a storage result matches the expected behavior.

    Args:
        case_name: Human-readable name of the case being checked.
        storage: Result of fetch_storage.
        expected_saved: True if payloads must be present, False if they must be NULL.
    """
    cells = (
        [storage["pipeline_input"], storage["pipeline_output"]]
        + storage["step_inputs"]
        + storage["step_outputs"]
    )
    if expected_saved:
        assert all(c is not None for c in cells), (
            f"{case_name}: expected payloads to be saved, found NULL"
        )
    else:
        assert all(c is None for c in cells), (
            f"{case_name}: expected payloads to be omitted (NULL)"
        )
    print(f"    [OK] {case_name}: {'saved' if expected_saved else 'omitted (NULL)'} "
          f"-> pipeline_input={storage['pipeline_input'] is not None}, "
          f"pipeline_output={storage['pipeline_output'] is not None}, "
          f"step_inputs={[s is not None for s in storage['step_inputs']]}, "
          f"step_outputs={[s is not None for s in storage['step_outputs']]}")


def main() -> None:
    """Run both configurations and verify the storage behavior."""
    print("=" * 70)
    print("DEMO 04: save_json_input_output")
    print("=" * 70)

    with tempfile.TemporaryDirectory() as tmp:
        db_path = os.path.join(tmp, "tracking.db")
        config_dir = os.path.join(tmp, "configs")

        print("\n--- Case 1: save_json_input_output=False ---")
        off_id = run_pipeline(db_path, config_dir, "Trip_L1", save_json=False)
        assert_case("False -> steps/pipeline store NULL", fetch_storage(off_id, db_path), expected_saved=False)

        print("\n--- Case 2: save_json_input_output=True (default) ---")
        on_id = run_pipeline(db_path, config_dir, "Trip_L2", save_json=True)
        assert_case("True -> steps/pipeline store payloads", fetch_storage(on_id, db_path), expected_saved=True)

        print("\n--- Case 3: default behavior (flag omitted) ---")
        pipeline = Pipeline(
            pipeline_name="Trip_L3",
            tracking_db=db_path,
            config_dir=config_dir,
            verbose=False,
        )
        pipeline.set_steps([load_cargo, drive, park])
        pipeline.run({"trip": "C"})
        assert_case("Default -> payloads saved", fetch_storage(pipeline.pipeline_id, db_path), expected_saved=True)

    print("\n" + "=" * 70)
    print("[OK] save_json_input_output works for both configurations")
    print("=" * 70)


if __name__ == "__main__":
    sys.exit(main())
