# 01 Simple Function Pipeline

Basic pipeline example demonstrating sequential function execution.

## What It Does

1. Creates a Pipeline instance
2. Adds three functions as sequential steps
3. Runs the pipeline with input data
4. Each step transforms and passes data to the next

## Flow Diagram

```mermaid
flowchart TD
    A[Start: input=5] --> B[Step 1: multiply_by_two]
    B -->|value=10| C[Step 2: add_ten]
    C -->|value=20| D[Step 3: square]
    D --> E[Result: result=400]
    
    style A fill:#e1f5fe
    style E fill:#c8e6c9
```

## Execution Sequence

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant S1 as multiply_by_two
    participant S2 as add_ten
    participant S3 as square
    
    P->>S1: run({input: 5})
    S1-->>P: {value: 10}
    P->>S2: run({value: 10})
    S2-->>P: {value: 20}
    P->>S3: run({value: 20})
    S3-->>P: {result: 400}
    P-->>User: {input: 5, value: 20, result: 400}
```

## Data Transformation

```mermaid
graph LR
    I[input: 5] --> S1[×2 → 10] --> S2[+10 → 20] --> S3[² → 400]
    style I fill:#e1f5fe
    style S3 fill:#c8e6c9
```

## Code

```python
from wpipe import Pipeline

def multiply_by_two(data):
    return {"value": data["input"] * 2}

def add_ten(data):
    return {"value": data["value"] + 10}

def square(data):
    return {"result": data["value"] ** 2}

pipeline = Pipeline(verbose=True)
pipeline.set_steps([
    (multiply_by_two, "Multiply by 2", "v1.0"),
    (add_ten, "Add 10", "v1.0"),
    (square, "Square", "v1.0"),
])
result = pipeline.run({"input": 5})
# Result: {"input": 5, "value": 20, "result": 400}
```

## Run

```bash
python examples/basic_pipeline/01_simple_function/example.py
```