"""
09 Nested Pipelines - State Preservation

Shows state preservation between nested pipelines.
"""

from wpipe import Pipeline

def init_state(data):
    return {"state": {"count": 0}}

def increment(data):
    state = data.get("state", {})
    state["count"] += 1
    return {"state": state}

def get_state(data):
    return {"final_count": data.get("state", {}).get("count", 0)}

def main():
    inner = Pipeline(verbose=False)
    inner.set_steps([
        (init_state, "Init", "v1.0"),
        (increment, "Increment", "v1.0"),
    ])
    
    outer = Pipeline(verbose=True)
    outer.set_steps([
        (inner.run, "Inner", "v1.0"),
        (get_state, "Get State", "v1.0"),
    ])
    
    result = outer.run({})
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
