"""
07 Nested Pipelines - Parallel Execution

Shows multiple nested pipelines in parallel.
"""

from wpipe import Pipeline

def process_a(data):
    return {"a": data.get("value", 0)}

def process_b(data):
    return {"b": data.get("value", 0) * 2}

def combine(data):
    return {"combined": data.get("a", 0) + data.get("b", 0)}

def main():
    p1 = Pipeline(verbose=False)
    p1.set_steps([(process_a, "Process A", "v1.0")])
    
    p2 = Pipeline(verbose=False)
    p2.set_steps([(process_b, "Process B", "v1.0")])
    
    main_p = Pipeline(verbose=True)
    main_p.set_steps([
        (p1.run, "Pipeline A", "v1.0"),
        (p2.run, "Pipeline B", "v1.0"),
        (combine, "Combine", "v1.0"),
    ])
    
    result = main_p.run({"value": 10})
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
