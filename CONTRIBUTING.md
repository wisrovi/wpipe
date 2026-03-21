# Contributing to wpipe

Thank you for your interest in contributing to wpipe!

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/wpipe.git
   cd wpipe
   ```
3. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=wpipe --cov-report=html

# Run specific test file
pytest test/test_pipeline.py
```

### Code Quality

```bash
# Lint with ruff
ruff check wpipe/

# Type checking with mypy
mypy wpipe/

# Format code with black
black wpipe/
```

### Running All Quality Checks

```bash
ruff check wpipe/ && mypy wpipe/ && pytest
```

## Project Structure

```
wpipe/
├── wpipe/
│   ├── __init__.py
│   ├── api_client/       # API client for pipeline tracking
│   ├── exception/        # Custom exceptions
│   ├── log/              # Logging utilities
│   ├── pipe/             # Core pipeline implementation
│   ├── ram/              # Memory limit utilities
│   ├── sqlite/           # SQLite database utilities
│   └── util/             # YAML utilities
├── test/                 # Core library tests
└── examples/             # Example scripts
    └── test/             # Example tests
```

## Writing Tests

- All new features should include tests
- Tests are in `test/` for core functionality
- Example tests are in `examples/test/`
- Use descriptive test names: `test_<feature>_<behavior>`

## Pull Request Guidelines

1. Ensure all tests pass
2. Run linting: `ruff check wpipe/`
3. Run type checking: `mypy wpipe/`
4. Update documentation if needed
5. Keep changes focused and atomic

## Code Style

- Follow PEP 8
- Use type hints where possible
- Add docstrings to public functions
- Keep functions small and focused

## Reporting Issues

- Use the GitHub issue tracker
- Include a minimal reproducible example
- Specify your Python version and OS
