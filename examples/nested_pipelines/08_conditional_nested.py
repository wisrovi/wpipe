"""
08 Nested Pipelines - Conditional Nested

Shows nested pipeline with condition.
"""

from wpipe import Pipeline

def get_type(data):
    return {"type": "A"}

def process_a(data):
    return {"processed": "A"}

def process_b(data):
    return {"processed": "B"}

def main():
    inner_a = Pipeline(verbose=False)
    inner_a.set_steps([(process_a, "Process A", "v1.0")])
    
    inner_b = Pipeline(verbose=False)
    inner_b.set_steps([(process_b, "Process B", "v1.0")])
    
    print("Type A:")
    result = inner_a.run({"type": "A"})
    print(f"Result: {result}")
    
    print("\nType B:")
    result = inner_b.run({"type": "B"})
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
