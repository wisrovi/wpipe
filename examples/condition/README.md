# Condition Examples

This directory contains examples demonstrating conditional branching in pipelines.

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

condition = Condition(
    expression="value > 50",
    branch_true=[(step_a, "Step A", "v1.0")],
    branch_false=[(step_b, "Step B", "v1.0")],
)

pipeline = Pipeline(verbose=True)
pipeline.set_condition(condition)
result = pipeline.run({"value": 30})
```

## Expression Syntax

The condition expression is evaluated using Python's `eval()`. Available variables are the keys from the input data:

- Numeric: `value > 50`, `count >= 10`
- String: `status == "active"`, `name == "admin"`
- Boolean: `is_valid == True`, `enabled`

Safe globals: `True`, `False`, `None`