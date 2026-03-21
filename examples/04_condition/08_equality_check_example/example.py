"""
08 Condition - Equality Checks

Shows equality and inequality checks.
"""

from typing import Any

from wpipe import Pipeline
from wpipe.pipe import Condition


def get_status(data: dict[str, Any]) -> dict[str, Any]:
    """Fetch user status for equality checking.

    Args:
        data: Input data dictionary (unused in this function).

    Returns:
        Dictionary with status information.

    Example:
        >>> result = get_status({})
        >>> print(result)
        {'status': 'active'}
    """
    return {"status": "active"}


def process_active(data: dict[str, Any]) -> dict[str, Any]:
    """Process user when status is active.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary indicating active processing.

    Example:
        >>> result = process_active({})
        >>> print(result)
        {'processed': 'active'}
    """
    return {"processed": "active"}


def process_inactive(data: dict[str, Any]) -> dict[str, Any]:
    """Process user when status is inactive.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary indicating inactive processing.

    Example:
        >>> result = process_inactive({})
        >>> print(result)
        {'processed': 'inactive'}
    """
    return {"processed": "inactive"}


def main() -> None:
    """Run the equality check example demonstrating == operator.

    Creates a pipeline with a condition that checks if status equals
    'active' and routes to the appropriate processing step.

    Example:
        >>> main()
        Result: {...}
    """
    condition = Condition(
        expression='status == "active"',
        branch_true=[(process_active, "Process Active", "v1.0")],
        branch_false=[(process_inactive, "Process Inactive", "v1.0")],
    )

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps(
        [
            (get_status, "Get Status", "v1.0"),
            condition,
        ]
    )

    result = pipeline.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
