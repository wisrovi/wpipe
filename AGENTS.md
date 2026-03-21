# AGENTS.md

Commands for developing wpipe.

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest test/test_pipeline.py

# Run with coverage
pytest --cov=wpipe --cov-report=html

# Open coverage report
open htmlcov/index.html
```

## Linting

```bash
# Run ruff linter
ruff check wpipe/

# Auto-fix linting issues
ruff check wpipe/ --fix

# Run mypy type checker
mypy wpipe/
```

## Building

```bash
# Build package
pip install -e .

# Build wheel
pip wheel . -w dist/

# Install from wheel
pip install dist/wpipe-*.whl
```

## Documentation

```bash
# Build docs
cd docs && make html

# View docs
open build/html/index.html
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all quality checks
ruff check wpipe/ && mypy wpipe/ && pytest
```
