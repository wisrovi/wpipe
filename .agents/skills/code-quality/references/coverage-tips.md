# Coverage Improvement Tips

## Target: ≥85%

## Understanding Coverage Gaps

### Lines Not Covered

Run with detailed output:
```bash
pytest --cov=. --cov-report=term-missing tests/
```

This shows which specific lines are missing:
```
Name          Stmts   Miss  Cover   Missing
---------------------------------------------
app/main.py      50      5   90%   23,45,67,89
```

## Common Uncovered Patterns

### 1. Error Handling

```python
# Often uncovered
def load_config():
    try:
        return json.load(open('config.json'))
    except FileNotFoundError:  # ← This branch may not be tested
        return DEFAULT_CONFIG
    except json.JSONDecodeError:  # ← This too
        return DEFAULT_CONFIG
```

**Fix:** Add tests for each exception:
```python
def test_load_config_file_not_found():
    """Test behavior when config file is missing."""
    # Mock open() to raise FileNotFoundError
    with patch('builtins.open', side_effect=FileNotFoundError):
        result = load_config()
        assert result == DEFAULT_CONFIG

def test_load_config_invalid_json():
    """Test behavior when config has invalid JSON."""
    # Mock open() to return invalid JSON
    ...
```

### 2. Conditional Branches

```python
# if/else branches
if user.is_active:
    return send_email(user.email)  # One branch
else:
    return None  # Other branch - need test for inactive user
```

**Fix:** Test both paths:
```python
def test_send_notification_active_user():
    user = User(is_active=True)
    result = send_notification(user)
    assert result == "sent"

def test_send_notification_inactive_user():
    user = User(is_active=False)
    result = send_notification(user)
    assert result is None
```

### 3. Type Guards

```python
def process(data):
    if not isinstance(data, dict):  # ← Need test with non-dict
        raise TypeError("data must be dict")
    return data.get("value")
```

**Fix:** Test type validation:
```python
def test_process_non_dict_raises():
    with pytest.raises(TypeError):
        process("string")

def test_process_dict_returns_value():
    assert process({"value": 42}) == 42
```

### 4. Edge Cases

```python
def divide(a, b):
    return a / b  # ← b=0 needs test
```

**Fix:** Test edge cases:
```python
def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
```

## Strategies to Increase Coverage

### 1. Mock External Dependencies

```python
# Don't test external APIs, mock them
@patch('requests.get')
def test_fetch_user(mock_get):
    mock_get.return_value = Mock(json=lambda: {"name": "Test"})
    result = fetch_user(1)
    assert result["name"] == "Test"
```

### 2. Parametrize Tests

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert double(input) == expected
```

### 3. Use fixtures for complex setup

```python
@pytest.fixture
def sample_user():
    return User(name="Test", email="test@test.com", is_active=True)

def test_user_greet(sample_user):
    assert sample_user.greet() == "Hello, Test"
```

### 4. Test exceptions explicitly

```python
with pytest.raises(ValueError, match="invalid.*"):
    validate_input(bad_data)
```

## Coverage Thresholds

| Project Type | Recommended Target |
|--------------|-------------------|
| Library/Package | 90-100% |
| Application | 80-90% |
| Scripts | 70-80% |
| POC/MVP | 60-70% |

## Coverage Reports

### HTML Report (Interactive)

```bash
pytest --cov=. --cov-report=html
# Open htmlcov/index.html
```

### XML (CI Integration)

```bash
pytest --cov=. --cov-report=xml
# Generates coverage.xml for CI tools
```

### JSON

```bash
pytest --cov=. --cov-report=json --cov-report=term
# Generates coverage.json
```

## Excluding Code from Coverage

### .coveragerc

```ini
[run]
source = .
omit =
    */tests/*
    */venv/*
    */__pycache__/*
    */migrations/*
    setup.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
```

### In-code exclusions

```python
if False:  # pragma: no cover
    # Dead code, never executed in tests

def unimplemented():  # pragma: no cover
    """Not yet implemented."""
    raise NotImplementedError
```

## Measuring Improvement

```bash
# Before
pytest --cov=. --cov-report=term | grep TOTAL

# After refactoring
pytest --cov=. --cov-report=term | grep TOTAL

# Compare
echo "Coverage improvement: $AFTER% - $BEFORE%"
```
