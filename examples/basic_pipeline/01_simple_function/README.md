# 01 Simple Function Pipeline

This is the simplest possible pipeline example. It demonstrates the basic pattern of creating a pipeline and running it with sequential steps.

## What It Does

1. Creates a Pipeline instance
2. Defines three functions as pipeline steps
3. Runs the pipeline with input data
4. Each step transforms the data and passes it to the next step

## Code Example

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

## Flow Diagram

```mermaid
flowchart TD
    A[Start: input=5] --> B[Step 1: multiply_by_two]
    B -->|value=10| C[Step 2: add_ten]
    C -->|value=20| D[Step 3: square]
    D --> E[Result: result=400]
    
    style A fill:#e1f5fe
    style B fill:#b3e5fc
    style C fill:#b3e5fc
    style D fill:#b3e5fc
    style E fill:#c8e6c9
```

## Pipeline Execution Flow

```mermaid
sequenceDiagram
    participant User
    participant Pipeline
    participant Step1 as multiply_by_two
    participant Step2 as add_ten
    participant Step3 as square
    
    User->>Pipeline: run({input: 5})
    Pipeline->>Step1: invoke(data={input: 5})
    Step1-->>Pipeline: returns {value: 10}
    Pipeline->>Step2: invoke(data={value: 10})
    Step2-->>Pipeline: returns {value: 20}
    Pipeline->>Step3: invoke(data={value: 20})
    Step3-->>Pipeline: returns {result: 400}
    Pipeline-->>User: returns {input: 5, value: 20, result: 400}
```

## Data Transformation

```mermaid
graph LR
    subgraph Input
    I1[input: 5]
    end
    
    subgraph Step1_multiply_by_two
    S1[value: 10]
    end
    
    subgraph Step2_add_ten
    S2[value: 20]
    end
    
    subgraph Step3_square
    S3[result: 400]
    end
    
    I1 --> S1 --> S2 --> S3
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| Pipeline | Main orchestrator class |
| Step | A function that receives data, processes it, returns updated data |
| set_steps() | Method to define the sequence of steps |
| run() | Executes the pipeline with input data |

## Expected Output

```
Input: 5 -> Output: {'input': 5, 'value': 20, 'result': 400}
```

## Test

Run this example:
```bash
python examples/basic_pipeline/01_simple_function/example.py
```