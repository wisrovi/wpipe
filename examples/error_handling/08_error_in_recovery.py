"""
08 Error Handling - Recovery After Error

Shows recovery mechanism after step failure.
"""

from wpipe import Pipeline

def failing_step(data):
    raise RuntimeError("Step failed")

def recovery_step(data):
    return {"recovered": True, "error": data.get("error")}

def main():
    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (failing_step, "Failing", "v1.0"),
    ])
    result = pipeline.run({})
    print(f"Result has error: {'error' in result}")

if __name__ == "__main__":
    main()
