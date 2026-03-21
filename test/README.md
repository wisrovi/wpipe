# Test Suite

This directory contains the test suite for wpipe library.

## Structure

- `conftest.py` - Shared pytest fixtures and configuration
- `test_pipeline.py` - Tests for Pipeline class
- `test_api_client.py` - Tests for APIClient class
- `test_sqlite.py` - Tests for SQLite database functionality
- `test_exceptions.py` - Tests for custom exceptions
- `test_utils.py` - Tests for utility functions
- `test_ram.py` - Tests for RAM memory utilities
- `test_log.py` - Tests for logging functionality

## Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=wpipe --cov-report=html
```

Run specific test file:
```bash
pytest test_pipeline.py -v
```

## Fixtures

Available fixtures in `conftest.py`:

- `temp_dir` - Temporary directory for test files
- `sample_config` - Sample API configuration
- `sample_pipeline_data` - Sample pipeline input data
- `sample_steps` - Sample pipeline steps definition
- `sample_worker_data` - Sample worker registration data
- `yaml_config_file` - Temporary YAML config file path
- `db_file` - Temporary database file path
