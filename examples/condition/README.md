# Condition Examples

This directory contains examples demonstrating conditional branching in pipelines.

## Important

**Condition must come AFTER a step that provides the data.** The condition evaluates data that was added by previous steps.

## Examples

| File | Description |
|------|-------------|
| `01_basic_condition.py` | Basic conditional branch based on numeric value |
| `02_string_condition.py` | String-based conditions (e.g., status == "active") |
| `03_multiple_steps.py` | Multiple steps in each branch |
| `04_no_else.py` | Condition without else branch |
| `05_invalid_expression.py` | Handling invalid condition expressions |

## Usage

```python
from wpipe import Pipeline
from wpipe.pipe import Condition

def fetch_data(data):
    return {"value": 50, "type": "A"}

def process_a(data):
    return {"processed": "A"}

condition = Condition(
    expression="value > 50",
    branch_true=[(process_a, "Process A", "v1.0")],
)

pipeline = Pipeline(verbose=True)
pipeline.set_steps([
    (fetch_data, "Fetch", "v1.0"),
    condition,
])
result = pipeline.run({})
```

## Expression Syntax

The condition expression is evaluated using Python's `eval()`. Available variables are the keys from the data (added by previous steps):

- Numeric: `value > 50`, `count >= 10`
- String: `status == "active"`, `name == "admin"`
- Boolean: `is_valid == True`, `enabled`

Safe globals: `True`, `False`, `None`