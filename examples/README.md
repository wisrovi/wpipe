# Examples

This directory contains example scripts demonstrating wpipe library functionality, organized by complexity.

## Structure (by complexity)

```
examples/
├── 01_basic_pipeline/        - Basic pipeline with functions and classes
├── 02_api_pipeline/         - Pipeline with API tracking
├── 03_error_handling/       - Error handling in pipelines
├── 04_condition/           - Conditional branching
├── 05_retry/               - Automatic retry on failure
├── 06_sqlite_integration/   - SQLite database integration
├── 07_nested_pipelines/     - Nested pipeline execution
├── 08_yaml_config/          - YAML configuration loading
├── 09_microservice/         - Microservice architecture
└── test/                    - Test files
```

## Complexity Levels

| Level | Module | Description |
|-------|--------|-------------|
| 1 | 01_basic_pipeline | Core pipeline functionality |
| 2 | 02_api_pipeline | API integration and tracking |
| 3 | 03_error_handling | Error handling strategies |
| 4 | 04_condition | Conditional execution |
| 5 | 05_retry | Retry mechanisms |
| 6 | 06_sqlite_integration | Database persistence |
| 7 | 07_nested_pipelines | Nested/hierarchical pipelines |
| 8 | 08_yaml_config | Configuration management |
| 9 | 09_microservice | Microservice patterns |

## Running Examples

```bash
# Level 1: Basic pipeline
python examples/01_basic_pipeline/01_simple_function/example.py

# Level 2: API tracking
python examples/02_api_pipeline/01_basic_api/example.py

# Level 3: Error handling
python examples/03_error_handling/*/example.py

# Level 4: Conditional execution
python examples/04_condition/*/example.py

# Level 5: Retry mechanisms
python examples/05_retry/*/example.py
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=wpipe --cov-report=html

# Open coverage report
open htmlcov/index.html
```

## Code Quality

- **ruff**: All checks passing
- **Tests**: 106 passing
- **Python Support**: 3.9 - 3.13
