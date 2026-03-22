Changelog
=========

This project follows `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_ format.

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[1.0.0] - 2026-03-22
---------------------

Added
~~~~~

**LTS Release**

- Official LTS (Long Term Support) release
- Stable API with guaranteed backward compatibility
- Comprehensive professional documentation
- 206 tests passing (106 core + 100 example tests)

**Documentation**

- Professional Sphinx documentation with sphinx_rtd_theme
- Complete API reference with parameter tables
- Detailed user guide with 9 sections
- Step-by-step tutorials
- Architecture documentation
- Comprehensive FAQ
- Glossary of terms
- Getting started guide
- Installation instructions
- Usage examples gallery

**Pipeline Features**

- Pipeline orchestration with step functions and classes
- Conditional branching for data-driven workflows
- Automatic retry logic with configurable parameters
- Nested pipelines for complex workflows
- Rich terminal progress visualization
- Comprehensive error handling with custom exceptions

**Integration Features**

- External API client for worker registration and health checks
- SQLite persistence for execution results
- YAML configuration support
- Worker management system

**Code Quality**

- Ruff linting with zero errors
- Type hints throughout codebase
- Detailed docstrings
- Consistent error handling
- MIT License

[0.1.7] - 2024-12-15
--------------------

Added
~~~~~

- Enhanced retry mechanism with exponential backoff
- SQLite context manager improvements
- Worker health check enhancements
- Pipeline condition support

Fixed
~~~~~

- Memory leak in long-running pipelines
- Race condition in worker registration
- SQLite connection pooling issues

[0.1.6] - 2024-11-20
--------------------

Added
~~~~~

- YAML configuration utilities
- Pipeline condition evaluation
- Nested pipeline support
- Step timeout configuration

[0.1.5] - 2024-10-10
--------------------

Added
~~~~~

- Rich terminal output for progress tracking
- Step metadata versioning
- Pipeline execution callbacks
- Result filtering utilities

[0.1.0] - 2024-01-01
--------------------

Added
~~~~~

- Initial release
- Basic Pipeline class
- SQLite integration
- API client
- Logging utilities
- RAM memory utilities
- Custom exceptions
- Basic test suite
