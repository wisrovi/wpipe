# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-22 - LTS Release

### Added

#### LTS Release
- Official Long Term Support release
- Stable API with guaranteed backward compatibility
- Comprehensive professional documentation
- 106 tests passing (106 core + 100 example tests)

#### Documentation

- **Professional Sphinx Documentation** with sphinx_rtd_theme
- **Complete API Reference** with parameter tables
- **Detailed User Guide** with 10 sections
- **Step-by-step Tutorials** covering all features
- **Comprehensive FAQ** with 40+ questions
- **Glossary** of terms
- **Architecture Documentation** with design patterns
- **Getting Started Guide** with prerequisites
- **Installation Instructions** (pip, source, dev)
- **Usage Examples Gallery** with 100+ examples

#### Pipeline Features
- Pipeline orchestration with step functions and classes
- Conditional branching for data-driven workflows
- Automatic retry logic with configurable parameters
- Nested pipelines for complex workflows
- Rich terminal progress visualization
- Comprehensive error handling with custom exceptions

#### Integration Features
- External API client for worker registration and health checks
- SQLite persistence for execution results
- YAML configuration support
- Worker management system

#### Code Quality
- Ruff linting with zero errors
- Type hints throughout codebase
- Detailed docstrings
- Consistent error handling
- MIT License

### Examples (100+ organized by complexity)

| Folder | Count | Description |
|--------|-------|-------------|
| 01_basic_pipeline | 15 | Functions, classes, mixed steps, data flow |
| 02_api_pipeline | 21 | External APIs, workers, execution tracking |
| 03_error_handling | 10 | Exceptions, error codes, graceful recovery |
| 04_condition | 9 | Conditional branches, decision trees |
| 05_retry | 9 | Automatic retries, backoff strategies |
| 06_sqlite_integration | 9 | Persistence, database operations |
| 07_nested_pipelines | 9 | Complex workflows, reusable components |
| 08_yaml_config | 9 | Configuration, environment variables |
| 09_microservice | 9 | Production-ready microservice patterns |

### Dependencies
- `requests>=2.31.0` — HTTP client for API communication
- `pyyaml>=6.0.1` — YAML configuration parsing

---

## [0.1.7] - 2024-12-15

### Added
- Enhanced retry mechanism with exponential backoff
- SQLite context manager improvements
- Worker health check enhancements
- Pipeline condition support

### Fixed
- Memory leak in long-running pipelines
- Race condition in worker registration
- SQLite connection pooling issues

---

## [0.1.6] - 2024-11-20

### Added
- YAML configuration utilities
- Pipeline condition evaluation
- Nested pipeline support
- Step timeout configuration

---

## [0.1.5] - 2024-10-10

### Added
- Rich terminal output for progress tracking
- Step metadata versioning
- Pipeline execution callbacks
- Result filtering utilities

---

## [0.1.0] - 2024-01-01

### Added
- Initial release
- Basic Pipeline class
- SQLite integration
- API client
- Logging utilities
- RAM memory utilities
- Custom exceptions
- Basic test suite

---

## Upgrade Guide

### From 0.x to 1.0.0

```bash
# Update wpipe
pip install --upgrade wpipe

# Verify version
python -c "import wpipe; print(wpipe.__version__)"
```

### Breaking Changes

None. Version 1.0.0 is fully backward compatible with 0.x versions.

---

## Support

- **Documentation**: https://wpipe.readthedocs.io/
- **Examples**: https://github.com/wisrovi/wpipe/tree/main/examples
- **Issues**: https://github.com/wisrovi/wpipe/issues
- **Discussions**: https://github.com/wisrovi/wpipe/discussions
- **PyPI**: https://pypi.org/project/wpipe/
