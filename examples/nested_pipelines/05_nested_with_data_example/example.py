"""
05 Nested Pipelines - Passing Custom Data

Shows passing custom data to nested pipelines.
"""

from wpipe import Pipeline

def inner_step(data):
    return {"inner_result": data.get("value", 0) * 2}

def outer_step(data):
    return {"outer_result": data.get("inner_result", 0) + 10}

def main():
    inner = Pipeline(verbose=False)
    inner.set_steps([(inner_step, "Inner", "v1.0")])
    
    outer = Pipeline(verbose=True)
    outer.set_steps([
        (inner.run, "Inner Pipeline", "v1.0"),
        (outer_step, "Outer", "v1.0"),
    ])
    
    result = outer.run({"value": 5})
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
