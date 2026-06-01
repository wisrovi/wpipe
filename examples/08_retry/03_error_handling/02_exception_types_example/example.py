"""
Example: Error Handling - Different Exception Types

Shows handling different exception types.
"""

from typing import Any

from wpipe import Pipeline


def process_string(data: dict[str, Any]) -> dict[str, Any]:
    """Process string input."""
    value = data.get("value", "")
    return {"result": len(value), "type": "string"}


def process_number(data: dict[str, Any]) -> dict[str, Any]:
    """Process number input."""
    value = data.get("value", 0)
    return {"result": value * 2, "type": "number"}


def main() -> None:
    """Run exception types example."""
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps([
        (process_string, "Process String", "v1.0"),
        (process_number, "Process Number", "v1.0"),
    ])

    result = pipeline.run({"value": "hello"})
    print(f"String result: {result['result']}")
    print(f"Number result: {result['result']}")


if __name__ == "__main__":
    main()