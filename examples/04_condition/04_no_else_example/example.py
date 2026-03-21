"""
04 Condition - No Else Branch

Shows condition without else branch (branch_false).
IMPORTANT: Condition must come AFTER a step that provides the data.
"""

from typing import Any

from wpipe import Pipeline
from wpipe.pipe import Condition


def get_tier(data: dict[str, Any]) -> dict[str, Any]:
    """Fetch user tier information.

    Args:
        data: Input data dictionary (unused in this function).

    Returns:
        Dictionary with tier and name information.

    Example:
        >>> result = get_tier({})
        >>> print(result)
        {'tier': 'premium', 'name': 'test'}
    """
    return {"tier": "premium", "name": "test"}


def premium_process(data: dict[str, Any]) -> dict[str, Any]:
    """Process premium tier users.

    Args:
        data: Input data dictionary containing tier information.

    Returns:
        Dictionary with processing result and discount.

    Example:
        >>> result = premium_process({"tier": "premium"})
        >>> print(result)
        {'processed': 'premium', 'discount': 0.1}
    """
    return {"processed": "premium", "discount": 0.1}


def main() -> None:
    """Run the no else branch example demonstrating optional branches.

    Creates a pipeline with a condition that only has a true branch,
    leaving the false branch empty. When the condition evaluates to false,
    no additional steps are executed.

    Example:
        >>> main()
        Test 1: tier = premium
        Result: {...}
    """
    condition = Condition(
        expression="tier == 'premium'",
        branch_true=[(premium_process, "Premium Process", "v1.0")],
        branch_false=[],
    )

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps(
        [
            (get_tier, "Get Tier", "v1.0"),
            condition,
        ]
    )

    print("Test 1: tier = premium")
    result1 = pipeline.run({})
    print(f"Result: {result1}")


if __name__ == "__main__":
    main()
