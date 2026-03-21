"""
09 Condition - Chained Conditions

Shows chaining multiple conditions.
"""

from typing import Any

from wpipe import Pipeline
from wpipe.pipe import Condition


def get_data(data: dict[str, Any]) -> dict[str, Any]:
    """Fetch tier and amount for hierarchical condition testing.

    Args:
        data: Input data dictionary (unused in this function).

    Returns:
        Dictionary with tier and amount values.

    Example:
        >>> result = get_data({})
        >>> print(result)
        {'tier': 'premium', 'amount': 1000}
    """
    return {"tier": "premium", "amount": 1000}


def premium_high(data: dict[str, Any]) -> dict[str, Any]:
    """Process premium users with high amounts.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary indicating premium high category.

    Example:
        >>> result = premium_high({})
        >>> print(result)
        {'category': 'premium_high'}
    """
    return {"category": "premium_high"}


def premium_low(data: dict[str, Any]) -> dict[str, Any]:
    """Process premium users with low amounts.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary indicating premium low category.

    Example:
        >>> result = premium_low({})
        >>> print(result)
        {'category': 'premium_low'}
    """
    return {"category": "premium_low"}


def standard(data: dict[str, Any]) -> dict[str, Any]:
    """Process standard tier users.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary indicating standard category.

    Example:
        >>> result = standard({})
        >>> print(result)
        {'category': 'standard'}
    """
    return {"category": "standard"}


def main() -> None:
    """Run the chained conditions example demonstrating nested conditions.

    Creates a pipeline with conditions nested within branch_true of another
    condition. This allows for hierarchical decision making where the first
    condition determines a category, and subsequent conditions refine it.

    Example:
        >>> main()
        Result: {...}
    """
    condition1 = Condition(
        expression="tier == 'premium'",
        branch_true=[
            Condition(
                expression="amount > 500",
                branch_true=[(premium_high, "Premium High", "v1.0")],
                branch_false=[(premium_low, "Premium Low", "v1.0")],
            )
        ],
        branch_false=[(standard, "Standard", "v1.0")],
    )

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps(
        [
            (get_data, "Get Data", "v1.0"),
            condition1,
        ]
    )

    result = pipeline.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
