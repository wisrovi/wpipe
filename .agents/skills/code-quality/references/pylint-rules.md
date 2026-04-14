# Pylint Rules Reference

## Scoring System

Pylint scores from 0-10. Target: ≥9.0

| Score | Rating |
|-------|--------|
| 10 | Perfect |
| 9.0-9.9 | Excellent |
| 8.0-8.9 | Good |
| 7.0-7.9 | Acceptable |
| <7.0 | Needs work |

## Common Issues and Fixes

### Code Design (C0103)
```
❌ naming violation: name too short, doesn't conform to snake_case
✅ Use: snake_case for variables/functions, CamelCase for classes
```

### Convention (C0111, C0112)
```
❌ Missing function docstring (Missing function docstring)
✅ Add: """Brief description of what function does."""
```

### Refactor (R0913, R0914)
```
❌ Too many arguments (X/7)
✅ Split function into smaller functions

❌ Too many local variables (X/15)
✅ Extract logic into helper functions
```

### Warning (W0612, W0611)
```
❌ Unused variable 'xxx'
✅ Remove or prefix with _

❌ Unused import xxx
✅ Remove import or use it
```

### Error (E1101, E0401)
```
❌ Instance of 'X' has no 'Y' member
✅ Check if attribute exists or add type ignore

❌ Unable to import X
✅ Install package or fix PYTHONPATH
```

## Disabled by Default

```python
--disable=import-error,no-member,no-name-in-module
```

These are often caused by dynamic imports or type stubs.

## Per-module Configuration

Create `.pylintrc` in project root:

```ini
[MASTER]
jobs=4
persistent=yes

[MESSAGES CONTROL]
disable=
    missing-docstring,
    too-few-public-methods,
    too-many-arguments,
    too-many-locals

[FORMAT]
max-line-length=120
indent-string='    '

[DESIGN]
max-args=7
max-locals=20
max-returns=10
max-branches=15
```

## Checking Specific Files

```bash
# Single file
pylint app/module.py

# Directory
pylint app/

# With output file
pylint app/ > pylint_report.txt

# JSON output
pylint app/ --output-format=json > pylint_report.json
```

## CI Integration

```yaml
# GitHub Actions
- name: Run pylint
  run: |
    pylint --output-format=text --exit-zero app/ || true
    pylint_score=$(cat pylint_report.txt | grep "rated at" | awk '{print $5}')
    echo "Pylint Score: $pylint_score"
```

## Common Patterns

### Classes need public methods

```python
class User:
    def __init__(self, name: str):
        self.name = name
    
    def greet(self) -> str:  # ✅ Has public method
        return f"Hello, {self.name}"

class Data:  # ⚠️ No public methods
    pass
```

### Exception handling

```python
# ❌
try:
    x = json.loads(data)
except:  # Bare except
    pass

# ✅
try:
    x = json.loads(data)
except json.JSONDecodeError as e:
    logger.error(f"Invalid JSON: {e}")
    raise ValueError("Invalid data") from e
```

### Imports order

```python
# 1. Standard library
import os
import json
from typing import Optional

# 2. Third party
import loguru
import pydantic

# 3. Local
from app.models import User
from app.utils import helpers
```

## Run with Auto-fix

```bash
# Format first
isort app/
black app/

# Then lint
pylint app/ --disable=import-error,no-member,no-name-in-module
```
