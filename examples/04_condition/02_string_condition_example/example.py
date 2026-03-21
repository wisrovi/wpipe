"""
02 Condition - String Based Condition

Shows using string conditions like 'status == "active"'.
IMPORTANT: Condition must come AFTER a step that provides the data.
"""

from typing import Any

from wpipe import Pipeline
from wpipe.pipe import Condition


def get_status(data: dict[str, Any]) -> dict[str, Any]:
    """Fetch user status information.

    Args:
        data: Input data dictionary (unused in this function).

    Returns:
        Dictionary with status and user information.

    Example:
        >>> result = get_status({})
        >>> print(result)
        {'status': 'active', 'user': 'john'}
    """
    return {"status": "active", "user": "john"}


def activate_user(data: dict[str, Any]) -> dict[str, Any]:
    """Process user activation when status is active.

    Args:
        data: Input data dictionary containing status information.

    Returns:
        Dictionary with activation message.

    Example:
        >>> result = activate_user({"status": "active"})
        >>> print(result)
        {'message': 'User activated'}
    """
    return {"message": "User activated"}


def deactivate_user(data: dict[str, Any]) -> dict[str, Any]:
    """Process user deactivation when status is not active.

    Args:
        data: Input data dictionary containing status information.

    Returns:
        Dictionary with deactivation message.

    Example:
        >>> result = deactivate_user({"status": "inactive"})
        >>> print(result)
        {'message': 'User deactivated'}
    """
    return {"message": "User deactivated"}


def main() -> None:
    """Run the string condition example demonstrating string-based branching.

    Creates a pipeline with a condition that evaluates 'status == "active"'
    and routes execution to activate or deactivate branches.

    Example:
        >>> main()
        Test 1: status = active
        Result: {...}
    """
    condition = Condition(
        expression='status == "active"',
        branch_true=[(activate_user, "Activate", "v1.0")],
        branch_false=[(deactivate_user, "Deactivate", "v1.0")],
    )

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps(
        [
            (get_status, "Get Status", "v1.0"),
            condition,
        ]
    )

    print("Test 1: status = active")
    result1 = pipeline.run({})
    print(f"Result: {result1}")


if __name__ == "__main__":
    main()
