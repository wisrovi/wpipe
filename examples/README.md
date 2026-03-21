# Examples

This directory contains example scripts demonstrating wpipe library functionality.

## Structure

```
examples/
├── basic_pipeline/       - Basic pipeline with functions and classes
├── api_pipeline/        - Pipeline with API tracking
├── error_handling/      - Error handling in pipelines
├── nested_pipelines/    - Nested pipeline execution
├── sqlite_integration/   - SQLite database integration
├── yaml_config/         - YAML configuration loading
├── test/                - Test files for all examples
└── README.md
```

## Running Examples

```bash
# Basic pipeline
python examples/basic_pipeline/pipeline.py

# API tracking
python examples/api_pipeline/client.py

# Error handling
python examples/error_handling/errors.py

# Nested pipelines
python examples/nested_pipelines/nested.py

# SQLite integration
python examples/sqlite_integration/database.py

# YAML configuration
python examples/yaml_config/config_loader.py
```

## Running Tests

```bash
# Run all example tests
pytest examples/test/

# Run with coverage
pytest examples/test/ --cov --cov-report=html
```

## Code Quality

- **Pylint Score**: 9.47/10
- **Tests**: 84 passing
- **Python Support**: 3.9 - 3.13
