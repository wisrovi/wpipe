"""
Example: API - Error Handling

Shows API error handling.
"""

from typing import Any

from wpipe import Pipeline


def api_call(data: dict[str, Any]) -> dict[str, Any]:
    """Simulate API call."""
    return {"result": "success", "status": 200}


def main() -> None:
    """Run API error example."""
    pipeline = Pipeline(pipeline_name="api_demo", verbose=True)

    pipeline.set_steps([
        (api_call, "API Call", "v1.0"),
    ])

    result = pipeline.run({})
    print(f"API Result: {result['result']}")


if __name__ == "__main__":
    main()