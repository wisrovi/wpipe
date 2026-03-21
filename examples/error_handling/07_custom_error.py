"""
07 Error Handling - Custom Error Handler

Shows implementing custom error handling logic.
"""

from wpipe import Pipeline

def step_with_error(data):
    if data.get("fail"):
        raise ValueError("Intentional failure")
    return {"success": True}

def error_handler(data):
    return {"handled": True, "error": data.get("error")}

def main():
    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (step_with_error, "Step", "v1.0"),
    ])
    
    result = pipeline.run({"fail": True})
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
