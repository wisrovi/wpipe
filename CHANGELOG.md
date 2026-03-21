# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-22 - LTS Release

### Added

#### Core Library
- **Pipeline Core**: Task orchestration and execution tracking
- **API Integration**: Worker registration and process tracking via REST API
- **SQLite Storage**: Persistent data storage with `Wsqlite` and `Sqlite` classes
- **Condition Branching**: Conditional execution with `Condition` class
- **Retry Mechanism**: Automatic retry with configurable attempts
- **Error Handling**: Custom exceptions (`TaskError`, `ProcessError`, `ApiError`)
- **RAM Monitoring**: Memory usage tracking
- **YAML Configuration**: Load/save pipeline configuration

#### Examples (100+ examples organized by functionality)
- [01_basic_pipeline](examples/01_basic_pipeline/): 15 foundational examples
- [02_api_pipeline](examples/02_api_pipeline/): 21 API integration examples
- [03_error_handling](examples/03_error_handling/): 10 error handling patterns
- [04_condition](examples/04_condition/): 9 conditional branching examples
- [05_retry](examples/05_retry/): 9 retry mechanism examples
- [06_sqlite_integration](examples/06_sqlite_integration/): 9 SQLite examples
- [07_nested_pipelines](examples/07_nested_pipelines/): 9 nested pipeline examples
- [08_yaml_config](examples/08_yaml_config/): 9 YAML configuration examples
- [09_microservice](examples/09_microservice/): 9 microservice examples

#### Code Quality
- **Type Hints**: Complete type annotations for all functions
- **Google-style Docstrings**: Args, Returns, Example sections
- **Mermaid Diagrams**: 5 diagrams per example README (graph LR, sequenceDiagram, stateDiagram-v2, flowchart LR, graph TB)
- **Unit Tests**: 206 tests (106 core + 100 example tests)
- **Ruff Linting**: Full PEP 8 compliance
- **Mypy Type Checking**: Type validation

#### Documentation
- **Sphinx Documentation**: Full API reference
- **README Files**: Comprehensive documentation per module
- **Getting Started Guide**: Quick start tutorial
- **Architecture Documentation**: System design
- **FAQ Section**: Common questions
- **Glossary**: Terminology definitions

### Changed
- Examples reorganized by complexity (01_basic_pipeline to 09_microservice)
- Mermaid diagrams simplified for better rendering
- API client methods properly typed

### Fixed
- Ruff linting errors (unused imports, deprecated APIs)
- Test assertions (assert False → raise AssertionError)
- Exception handling in test files

### Dependencies
- `requests>=2.31.0`
- `pandas>=2.0.0`
- `pyyaml>=6.0.1`
- `tabulate>=0.9.0`

---

## [0.1.7] - 2024-01-01

### Added
- RAM monitoring functionality
- Index.html generation for microservice examples

## [0.1.4] - 2023-12-01

### Added
- Nested pipeline support
- Error recovery patterns

## [0.1.3] - 2023-11-01

### Added
- SQLite integration
- YAML configuration

## [0.1.1] - 2023-10-01

### Added
- Initial pipeline implementation
- API client for worker tracking

## [0.1.0] - 2023-09-01

### Added
- Initial release
- Basic pipeline functionality

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

- **Documentation**: [docs/](docs/)
- **Examples**: [examples/](examples/)
- **Issues**: [GitHub Issues](https://github.com/wisrovi/wpipe/issues)
- **Discussions**: [GitHub Discussions](https://github.com/wisrovi/wpipe/discussions)
