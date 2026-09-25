"""
Example: Error Capture with break_on_error

Demonstrates how to capture forensic error information using add_error_capture
and enforce fail-fast behavior with break_on_error=True.
"""

from typing import Any, Dict
from wpipe import Pipeline, step, to_obj


@step(name="error_capture", version="v1.0", tags=["error_capture"])
@to_obj
def error_capture(context: Any, error: Dict[str, Any]) -> Any:
    """Captures and logs errors occurring within the pipeline."""
    print("\n" + "!" * 60)
    print("🚨 SYSTEM ALERT: ERROR DETECTED")
    print("!" * 60)
    print(f"📍 FAILED STEP: {error['step_name']}")
    print(f"📄 FILE: {error['file_path']}")
    print(f"🔢 LINE: {error['line_number']}")
    print(f"⚠️ MESSAGE: {error['error_message']}")
    print("-" * 60)
    return context


@step(name="step_one", version="v1.0")
def step_one(data: Dict[str, Any]) -> Dict[str, Any]:
    print("Executing Step 1...")
    return {"step_1": "success"}


@step(name="failing_step", version="v1.0")
def failing_step(data: Dict[str, Any]) -> Dict[str, Any]:
    print("Executing Failing Step...")
    raise RuntimeError("Critical error in data processing!")


@step(name="step_three", version="v1.0")
def step_three(data: Dict[str, Any]) -> Dict[str, Any]:
    print("Executing Step 3 (Should NOT be reached)...")
    return {"step_3": "success"}


def main() -> None:
    # Initialize pipeline (break_on_error=True can be set here or in add_error_capture)
    pipeline = Pipeline(
        pipeline_name="break_on_error_demo",
        break_on_error=True,
        verbose=False,
    )

    # Register error capture state with explicit break_on_error=True
    pipeline.add_error_capture([error_capture], break_on_error=True)

    pipeline.set_steps([step_one, failing_step, step_three])

    print("\n[Running Pipeline...]")
    try:
        result = pipeline.run({})
        print(f"\n[Execution Result] {result}")
    except RuntimeError as e:
        print(f"\n[Caught Expected Fail-Fast Exception] {e}")
        print("✓ Pipeline halted cleanly after error capture!")


if __name__ == "__main__":
    main()
