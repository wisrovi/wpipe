"""
06 Nested Pipelines - Deep Nesting

Shows deeply nested pipeline structure.
"""

from wpipe import Pipeline

def step_a(data):
    return {"a": 1}

def step_b(data):
    return {"b": 2}

def step_c(data):
    return {"c": 3}

def main():
    p1 = Pipeline(verbose=False)
    p1.set_steps([(step_a, "A", "v1.0")])
    
    p2 = Pipeline(verbose=False)
    p2.set_steps([(step_b, "B", "v1.0")])
    
    p3 = Pipeline(verbose=True)
    p3.set_steps([
        (p1.run, "P1", "v1.0"),
        (p2.run, "P2", "v1.0"),
        (step_c, "C", "v1.0"),
    ])
    
    result = p3.run({})
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
