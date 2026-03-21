"""
09 Nested Pipelines - State Preservation

Shows state preservation between nested pipelines.
"""


from wpipe import Pipeline


def init_state(data: dict) -> dict:
    """Initializes the state with a count.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary with initialized state.

    Example:
        >>> result = init_state({})
        >>> assert result == {"state": {"count": 0}}
    """
    return {"state": {"count": 0}}


def increment(data: dict) -> dict:
    """Increments the state count by one.

    Args:
        data: Input data dictionary containing state.

    Returns:
        Dictionary with incremented state.

    Example:
        >>> result = increment({"state": {"count": 5}})
        >>> assert result == {"state": {"count": 6}}
    """
    state: dict = data.get("state", {})
    state["count"] += 1
    return {"state": state}


def get_state(data: dict) -> dict:
    """Retrieves the final count from state.

    Args:
        data: Input data dictionary containing state.

    Returns:
        Dictionary with final_count.

    Example:
        >>> result = get_state({"state": {"count": 6}})
        >>> assert result == {"final_count": 6}
    """
    return {"final_count": data.get("state", {}).get("count", 0)}


def main() -> None:
    """Run the state preservation example.

    Example:
        >>> main()  # doctest: +ELLIPSIS
        Outer: Inner...
        Outer: Get State...
        Result: {...}
    """
    inner: Pipeline = Pipeline(verbose=False)
    inner.set_steps(
        [
            (init_state, "Init", "v1.0"),
            (increment, "Increment", "v1.0"),
        ]
    )

    outer: Pipeline = Pipeline(verbose=True)
    outer.set_steps(
        [
            (inner.run, "Inner", "v1.0"),
            (get_state, "Get State", "v1.0"),
        ]
    )

    result: dict = outer.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
