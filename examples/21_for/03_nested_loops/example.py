"""
Example 03: Nested For loops

This example demonstrates nested For loops.
Shows multiple @state decorated functions in a For loop.
"""

from wpipe import For, Pipeline
from wpipe.util import state


@state(name="track", version="v1.0")
def track_iterations(data):
    iteration = data.get("_loop_iteration", 0)
    data["history"] = data.get("history", [])
    data["history"].append(f"iter_{iteration}")
    return data


def main():
    pipe = Pipeline(pipeline_name="nested_example", verbose=False)
    pipe.set_steps(
        [
            (lambda d: {"history": []}, "init", "v1"),
            For(
                iterations=3,
                steps=[
                    track_iterations,
                ],
            ),
        ]
    )

    result = pipe.run({})
    print(f"History: {result.get('history')}")
    print(f"Iterations: {result.get('_loop_iteration')}")

    assert len(result["history"]) == 3
    print("\nTest passed!")


if __name__ == "__main__":
    main()
