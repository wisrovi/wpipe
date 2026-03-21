# Examples

This directory contains example scripts demonstrating wpipe library functionality.

## Available Examples

### Basic Examples

- `example_01_basic_pipeline.py` - Basic pipeline execution without API
- `example_02_api_pipeline.py` - Pipeline with API connection
- `example_03_error_handling.py` - Error handling in pipelines
- `example_04_nested_pipelines.py` - Nested pipeline execution
- `example_05_sqlite_integration.py` - SQLite database integration
- `example_06_yaml_config.py` - YAML configuration loading

## Running Examples

Run any example with:
```bash
python examples/example_01_basic_pipeline.py
```

## Legacy Examples

The `example/` directory contains legacy examples that may require additional dependencies (e.g., wkafka).

## Creating Custom Pipelines

Basic pipeline structure:
```python
from wpipe.pipe import Pipeline

def my_step(data):
    return {"result": data["input"] * 2}

pipeline = Pipeline(verbose=True)
pipeline.set_steps([(my_step, "My Step", "v1.0")])
result = pipeline.run({"input": 10})
```
