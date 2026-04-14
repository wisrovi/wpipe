# Python Coding Standards

## Nomenclatura

| Element | Convention | Example |
|---------|------------|---------|
| Variables | snake_case | `user_name` |
| Functions | snake_case | `get_user_by_id()` |
| Classes | CamelCase | `UserRepository` |
| Constants | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| Private variables | _prefix | `_internal_state` |
| Module private | __prefix | `__private_method` |

### ❌ Incorrecto
```python
userName = "john"           # camelCase
def GetUser(id):           # PascalCase function
    return USER_DATA[id]   # ALL_CAPS constant
```

### ✅ Correcto
```python
user_name = "john"         # snake_case
def get_user(id: int) -> dict:  # snake_case
    return users[id]       # lowercase
MAX_RETRY = 3              # UPPER_SNAKE for true constants
```

---

## Docstrings (Google Style)

### Functions

```python
def calculate_total(items: list[dict], tax_rate: float = 0.1) -> float:
    """Calculate total price including tax.
    
    Args:
        items: List of item dictionaries with 'price' key.
        tax_rate: Tax rate as decimal (default: 0.1).
    
    Returns:
        Total price including tax.
    
    Raises:
        ValueError: If items is empty or tax_rate is negative.
    
    Example:
        >>> items = [{"price": 10}, {"price": 20}]
        >>> calculate_total(items)
        33.0
    """
    if not items:
        raise ValueError("Items cannot be empty")
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative")
    
    subtotal = sum(item["price"] for item in items)
    return subtotal * (1 + tax_rate)
```

### Classes

```python
class UserService:
    """Service for managing user operations.
    
    Attributes:
        db: Database connection instance.
        cache: Cache client for user data.
    
    Example:
        >>> service = UserService(db, cache)
        >>> user = service.get_user(123)
    """
    
    def __init__(self, db: Database, cache: Cache) -> None:
        """Initialize UserService.
        
        Args:
            db: Database connection.
            cache: Cache client.
        """
        self._db = db
        self._cache = cache
    
    def get_user(self, user_id: int) -> User | None:
        """Get user by ID.
        
        Args:
            user_id: The user's unique identifier.
        
        Returns:
            User object if found, None otherwise.
        """
        # Implementation
        pass
```

---

## Type Hints

### Basic Usage

```python
def greet(name: str) -> str:
    return f"Hello, {name}"

def process_numbers(numbers: list[int]) -> int:
    return sum(numbers)

def get_user(user_id: int) -> dict[str, Any]:
    return {"id": user_id, "name": "Test"}
```

### Optional and Union

```python
from typing import Optional

def find_user(name: str) -> Optional[User]:
    """Return User if found, None otherwise."""
    ...

def parse_value(data: str) -> int | float:
    """Parse as int or float."""
    ...
```

### Complex Types

```python
from typing import TypedDict, Callable

class UserDict(TypedDict):
    name: str
    email: str
    age: int

def process_users(
    users: list[UserDict],
    validator: Callable[[UserDict], bool]
) -> list[UserDict]:
    return [u for u in users if validator(u)]
```

---

## Exception Handling

### ❌ Incorrecto
```python
try:
    data = json.loads(raw)
except:  # Bare except - catches everything
    pass

try:
    x = 1 / 0
except Exception:  # Too broad
    print("error")
```

### ✅ Correcto

```python
from loguru import logger

try:
    data = json.loads(raw)
except json.JSONDecodeError as e:
    logger.error(f"Invalid JSON at position {e.pos}: {e.msg}")
    raise ValueError("Configuration must be valid JSON") from e

try:
    result = divide(a, b)
except ZeroDivisionError:
    logger.warning(f"Division by zero: {a} / {b}")
    return None
```

### Exception Hierarchy

```python
class AppError(Exception):
    """Base exception for application errors."""
    pass

class ValidationError(AppError):
    """Raised when input validation fails."""
    pass

class ResourceNotFoundError(AppError):
    """Raised when a resource is not found."""
    pass

def get_user(user_id: int) -> User:
    user = _find_user(user_id)
    if not user:
        raise ResourceNotFoundError(f"User {user_id} not found")
    return user
```

---

## Logging con Loguru

### Setup

```python
from loguru import logger
import sys

# Configure logger
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)

# File logging
logger.add(
    "app.log",
    rotation="500 MB",
    retention="10 days",
    level="DEBUG"
)
```

### Usage

```python
from loguru import logger

def process_data(data: dict) -> None:
    logger.info("Processing data", extra={"data_id": data.get("id")})
    
    try:
        result = transform(data)
        logger.success(f"Processed successfully: {result}")
    except Exception as e:
        logger.exception(f"Failed to process data: {e}")
        raise

# With context
logger.bind(user_id=123).info("User action")
```

---

## Imports

### Order (isort)

```python
# 1. Standard library
import os
import json
from typing import Optional, Union

# 2. Third party
import loguru
import pydantic
import requests

# 3. Local application
from app.models import User
from app.utils import helpers
```

### Relative Imports

```python
# In app/services/user_service.py
from app.models import User           # Absolute (preferred)
from ..models import User            # Relative (OK)
from . import validators            # Same package
```

---

## Function Design

### Single Responsibility

```python
# ❌ Too many responsibilities
def handle_user(data: dict):
    validate(data)
    save_to_db(data)
    send_email(data)
    log_action(data)
    update_cache(data)

# ✅ Single responsibility
def create_user(data: dict) -> User:
    validate_user_data(data)
    return save_user(data)

def notify_user(user: User) -> None:
    send_welcome_email(user)

def sync_user_cache(user: User) -> None:
    cache.set(user.id, user)
```

### Early Returns

```python
# ❌ Nested ifs
def process(data):
    if data:
        if data.is_valid:
            if data.has_items:
                return do_something(data)
            else:
                return None
        else:
            raise ValueError("Invalid")
    else:
        raise ValueError("Empty")

# ✅ Early returns
def process(data):
    if not data:
        raise ValueError("Empty")
    
    if not data.is_valid:
        raise ValueError("Invalid")
    
    if not data.has_items:
        return None
    
    return do_something(data)
```

---

## Testing Standards

### Test Structure

```python
import pytest
from unittest.mock import Mock, patch

class TestUserService:
    """Test suite for UserService."""
    
    @pytest.fixture
    def service(self, mock_db, mock_cache):
        return UserService(mock_db, mock_cache)
    
    @pytest.fixture
    def sample_user(self):
        return User(id=1, name="Test", email="test@test.com")
    
    def test_get_user_found(self, service, sample_user, mock_db):
        mock_db.find.return_value = sample_user
        
        result = service.get_user(1)
        
        assert result == sample_user
        mock_db.find.assert_called_once_with(1)
    
    def test_get_user_not_found(self, service, mock_db):
        mock_db.find.return_value = None
        
        result = service.get_user(999)
        
        assert result is None
    
    def test_get_user_db_error(self, service, mock_db):
        mock_db.find.side_effect = DatabaseError("Connection failed")
        
        with pytest.raises(ServiceError, match="Database error"):
            service.get_user(1)
```

---

## Code Complexity

### Target: MCCABE < 10

```python
# ❌ High complexity
def process_order(order):
    if order.type == "standard":
        if order.items:
            if order.customer:
                if order.customer.verified:
                    if order.payment:
                        # Deep nesting
                        return fulfill_order(order)
                    else:
                        return "No payment"
                else:
                    return "Customer not verified"
            else:
                return "No customer"
        else:
            return "No items"
    elif order.type == "express":
        # Duplicate logic
        ...
```

### ✅ Low complexity

```python
def process_order(order: Order) -> str | OrderResult:
    validation = validate_order(order)
    if not validation.success:
        return validation.error
    
    if order.type == "standard":
        return fulfill_standard_order(order)
    elif order.type == "express":
        return fulfill_express_order(order)
```

---

## Git Commit Messages

```
feat(auth): implement JWT-based authentication

- Add JWT token generation
- Add token validation middleware
- Add refresh token support

Closes #123
```

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance
```
