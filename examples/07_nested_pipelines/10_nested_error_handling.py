"""
10 Nested Pipelines - Error Handling

Shows error handling in nested pipelines.
"""

from wpipe import Pipeline


def failing_step(data):
    raise ValueError("Nested pipeline error")

def handle_error(data):
    return {"error_handled": True}

def main():
    inner = Pipeline(verbose=False)
    inner.set_steps([(failing_step, "Failing", "v1.0")])

    outer = Pipeline(verbose=True)
    outer.set_steps([
        (inner.run, "Inner", "v1.0"),
    ])

    result = outer.run({})
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
