# Code Review Examples

## Example 1: Before/After Refactoring

### ❌ BEFORE (Bad Code)

```python
# examples/bad_user_service.py
def process_user_data(user_id, data):
    try:
        if not user_id:
            print("Error: user_id required")
            return None
        if not data:
            print("Error: data required")
            return None
        if type(data) != dict:
            print("Error: data must be dict")
            return None
        result = {"id": user_id, "name": data.get("name"), "email": data.get("email")}
        print(f"Processing user {user_id}")
        return result
    except:
        pass
```

### ✅ AFTER (Good Code)

```python
# examples/good_user_service.py
from loguru import logger


class ValidationError(Exception):
    """Raised when input validation fails."""
    pass


def validate_user_input(user_id: str, data: dict) -> None:
    """Validate user input parameters."""
    if not user_id:
        raise ValidationError("user_id is required")
    if not data:
        raise ValidationError("data is required")
    if not isinstance(data, dict):
        raise ValidationError("data must be a dictionary")


def process_user_data(user_id: str, data: dict) -> dict:
    """Process and return user data.
    
    Args:
        user_id: Unique user identifier.
        data: User data dictionary.
    
    Returns:
        Processed user data dictionary.
    
    Raises:
        ValidationError: If inputs are invalid.
    """
    validate_user_input(user_id, data)
    
    logger.info(f"Processing user {user_id}")
    
    return {
        "id": user_id,
        "name": data.get("name"),
        "email": data.get("email")
    }
```

## Example 2: Security Report Output

```markdown
# 🔒 Security Assessment Report

**Project:** example-service  
**Date:** 2026-03-24  
**Status:** 🟢 SECURE

---

## 📊 Executive Summary

| Metric | Value | Status |
|--------|-------|--------|
| Bandit Score | 10/10 | 🟢 |
| Vulnerabilities Found | 0 | 🟢 |
| Critical Issues | 0 | 🟢 |
| High Issues | 0 | 🟢 |

---

## ✅ All Checks Passed

- No hardcoded credentials found
- No SQL injection vulnerabilities
- No command injection risks
- Secure random usage
- Proper exception handling
```

## Example 3: Checklist Output

```
=== CODE REVIEW CHECKLIST ===
✓ Functions <30 lines
✓ No duplicate logic
✓ No unused imports
✓ No print statements (using loguru)
✓ No bare except
✓ Type hints present
✓ Docstrings present
✓ Bandit: 0 issues
✓ Safety: 0 vulnerabilities
✓ Pylint: 9.5/10
```
