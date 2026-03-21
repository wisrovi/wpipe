# Basic Pipeline

This directory contains foundational examples for understanding pipeline creation and execution.

## Overview

The `basic_pipeline` module is the core of wpipe, demonstrating how to create and run pipelines with various step types.

## Quick Start

```python
from wpipe import Pipeline

def step_function(data):
    return {"result": "success"}

pipeline = Pipeline(verbose=True)
pipeline.set_steps([
    (step_function, "Step Name", "v1.0"),
])
result = pipeline.run({"input": "value"})
```

## Examples

| Example | Description |
|---------|-------------|
| [01_simple_function](01_simple_function/) | Basic pipeline with function step |
| [02_class_steps](02_class_steps/) | Using class instances as steps |
| [03_mixed_steps](03_mixed_steps/) | Mix of functions and classes |
| [04_default_values](04_default_values/) | Using default parameter values |
| [05_args_kwargs](05_args_kwargs/) | Handling *args and **kwargs |
| [06_dict_processing](06_dict_processing/) | Dictionary manipulation in steps |
| [07_multiple_runs](07_multiple_runs/) | Running pipeline multiple times |
| [08_data_aggregation](08_data_aggregation/) | Aggregating data across steps |
| [09_empty_data](09_empty_data/) | Running with empty input data |
| [10_lambda_steps](10_lambda_steps/) | Using lambda functions |
| [11_decorator_steps](11_decorator_steps/) | Using decorators with pipelines |
| [12_context_manager](12_context_manager/) | Context manager pattern |
| [13_async_pipeline](13_async_pipeline/) | Asynchronous pipeline execution |
| [14_pipeline_chaining](14_pipeline_chaining/) | Chaining multiple pipelines |
| [15_pipeline_clone](15_pipeline_clone/) | Cloning and reusing pipelines |

## Architecture

```mermaid
graph TB
    subgraph Input
        D[Input Data]
    end
    
    subgraph Pipeline
        P[Pipeline]
        S[Steps List]
    end
    
    subgraph Steps
        S1[Step 1]
        S2[Step 2]
        S3[Step 3]
    end
    
    subgraph Output
        O[Result Data]
    end
    
    D --> P
    P --> S
    S --> S1
    S1 --> S2
    S2 --> S3
    S3 --> O
```

## Step Types

```mermaid
graph LR
    A[Step Types] --> B[Function]
    A --> C[Lambda]
    A --> D[Callable Class]
    A --> E[Pipeline]
```

### Function Steps

```python
def my_step(data):
    data["processed"] = True
    return data
```

### Lambda Steps

```python
step = (lambda d: {**d, "done": True}, "Lambda Step", "v1.0")
```

### Class Steps

```python
class MyStep:
    def __call__(self, data):
        return {"result": data.get("value", 0) * 2}

step = (MyStep(), "Class Step", "v1.0")
```

## Data Flow

```mermaid
sequenceDiagram
    participant Input
    participant Step1
    participant Step2
    participant Output
    
    Input->>Step1: {"x": 1}
    Step1->>Step1: Process
    Step1->>Step2: {"x": 1, "step1": True}
    Step2->>Step2: Process
    Step2->>Output: {"x": 1, "step1": True, "step2": True}
```

## Error Handling

```mermaid
stateDiagram-v2
    [*] --> Execute
    Execute --> Success
    Execute --> Error
    Error --> Recover
    Recover --> Success
    Error --> Fail
    Success --> [*]
    Fail --> [*]
```

## Best Practices

```mermaid
flowchart LR
    subgraph Good
        G1[Return data dict]
        G2[Handle missing keys]
        G3[Type hints]
    end
    
    subgraph Avoid
        B1[Mutate global state]
        B2[Side effects]
        B3[Complex lambdas]
    end
```

1. Always return a dictionary from steps
2. Handle missing keys with `.get()`
3. Use type hints for better IDE support
4. Keep steps focused and small
5. Use descriptive step names

## See Also

- [API Pipeline](../02_api_pipeline/) - Pipeline with API integration
- [Condition](../04_condition/) - Conditional branching
- [Error Handling](../03_error_handling/) - Error handling patterns
