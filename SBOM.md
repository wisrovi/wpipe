# Software Bill of Materials (SBOM)

**Project**: wpipe
**Version**: 2.0.0
**License**: MIT
**Author**: William Steve Rodriguez Villamizar
**Generated**: April 13, 2026

---

## Overview

This document provides a complete inventory of all dependencies, components, and resources used by wpipe 2.0.0. It is intended for enterprise users who require supply chain transparency and security auditing.

**Format**: SPDX 2.3 compatible
**Package Manager**: PyPI (pip)

---

## Runtime Dependencies

These packages are required for wpipe to function at runtime:

| Package | Min Version | Purpose | License | Critical? |
|---------|-------------|---------|---------|-----------|
| requests | >=2.31.0 | HTTP client for API integration | Apache-2.0 | Yes |
| loguru | >=0.7.0 | Logging framework | MIT | Yes |
| pandas | >=2.0.0 | Data processing and manipulation | BSD-3-Clause | Yes |
| pyyaml | >=6.0.1 | YAML configuration parsing | MIT | Yes |
| tqdm | >=4.66.0 | Progress bar display | MIT, MPL-2.0 | Yes |
| rich | >=13.7.0 | Rich terminal output and formatting | MIT | Yes |
| pydantic | >=2.0.0 | Data validation and settings management | MIT | Yes |
| fastapi | >=0.100.0 | Dashboard web API | MIT | Yes |
| uvicorn | >=0.23.0 | ASGI server for dashboard | BSD-3-Clause | Yes |
| wsqlite | >=0.1.0 | SQLite database wrapper | MIT | Yes |

---

## Development Dependencies

These packages are only needed for development and testing:

| Package | Min Version | Purpose | License |
|---------|-------------|---------|---------|
| pytest | >=7.4.0 | Test framework | MIT |
| pytest-cov | >=4.1.0 | Test coverage reporting | MIT |
| black | >=23.0.0 | Code formatter | MIT |
| ruff | >=0.1.0 | Linter and code quality | MIT |
| mypy | >=1.7.0 | Static type checker | MIT |

---

## Documentation Dependencies

These packages are only needed for building documentation:

| Package | Min Version | Purpose | License |
|---------|-------------|---------|---------|
| sphinx | >=7.2.0 | Documentation generator | BSD-2-Clause |
| sphinx-rtd-theme | >=2.0.0 | ReadTheDocs theme | MIT |
| sphinx-copybutton | >=0.5.0 | Copy button for code blocks | MIT |
| myst-parser | >=2.0.0 | Markdown parser for Sphinx | MIT |
| sphinx-sitemap | >=2.5.0 | Sitemap generation | MIT |
| sphinx-design | >=0.5.0 | Design components for Sphinx | MIT |

---

## Standard Library Dependencies

These are part of the Python standard library (no external installation needed):

| Module | Python Version | Purpose |
|--------|---------------|---------|
| sqlite3 | 3.9+ | Database operations |
| threading | 3.9+ | Thread synchronization |
| json | 3.9+ | JSON serialization |
| csv | 3.9+ | CSV file operations |
| os | 3.9+ | Operating system interfaces |
| sys | 3.9+ | System-specific parameters |
| time | 3.9+ | Time-related functions |
| datetime | 3.9+ | Date and time handling |
| typing | 3.9+ | Type hints support |
| asyncio | 3.9+ | Asynchronous I/O |
| concurrent.futures | 3.9+ | Thread/process pool executors |
| contextlib | 3.9+ | Utilities for with-statement |
| functools | 3.9+ | Higher-order functions |
| collections | 3.9+ | Container datatypes |
| pathlib | 3.9+ | Object-oriented filesystem paths |
| logging | 3.9+ | Logging facility |
| warnings | 3.9+ | Warning control |
| traceback | 3.9+ | Print or retrieve stack traces |
| inspect | 3.9+ | Inspect live objects |
| hashlib | 3.9+ | Secure hash and message digests |
| uuid | 3.9+ | UUID objects |
| dataclasses | 3.9+ | Data classes |
| abc | 3.9+ | Abstract base classes |
| enum | 3.9+ | Support for enumerations |
| copy | 3.9+ | Shallow and deep copy operations |
| tempfile | 3.9+ | Temporary files and directories |
| shutil | 3.9+ | High-level file operations |
| io | 3.9+ | Core tools for working with streams |

---

## Internal Components

These are modules developed specifically for wpipe:

| Component | Lines | Purpose |
|-----------|-------|---------|
| wpipe/__init__.py | ~290 | Main exports and version |
| wpipe/pipe/pipe.py | ~500 | Core Pipeline, Condition, ProgressManager |
| wpipe/pipe/pipe_async.py | ~150 | Async pipeline support |
| wpipe/api_client/api_client.py | ~200 | HTTP API client |
| wpipe/sqlite/Sqlite.py | ~150 | Core SQLite operations |
| wpipe/sqlite/Wsqlite.py | ~100 | SQLite context manager wrapper |
| wpipe/log/log.py | ~50 | Logging utilities |
| wpipe/ram/ram.py | ~100 | Memory control |
| wpipe/util/utils.py | ~150 | YAML and utility functions |
| wpipe/exception/api_error.py | ~100 | Custom exceptions |
| wpipe/checkpoint/ | ~300 | Checkpoint management |
| wpipe/timeout/ | ~200 | Timeout decorators |
| wpipe/type_hinting/ | ~200 | Type validation |
| wpipe/resource_monitor/ | ~250 | Resource monitoring |
| wpipe/export/ | ~200 | Export to JSON/CSV |
| wpipe/parallel/ | ~260 | Parallel execution |
| wpipe/composition/ | ~250 | Pipeline composition |
| wpipe/decorators/ | ~200 | Step decorators |
| wpipe/tracking/ | ~200 | Execution tracking |
| wpipe/dashboard/ | ~300 | FastAPI dashboard |

**Total Internal Code**: ~3,750 lines

---

## Python Version Support

| Python Version | Status | Tested in CI |
|---------------|--------|-------------|
| 3.9 | ✅ Supported | Yes |
| 3.10 | ✅ Supported | Yes |
| 3.11 | ✅ Supported | Yes |
| 3.12 | ✅ Supported | Yes |
| 3.13 | ✅ Supported | Yes |

---

## License Compatibility

All dependencies use licenses compatible with MIT:

| License | Packages | Compatible with MIT? |
|---------|----------|---------------------|
| MIT | loguru, pyyaml, tqdm, rich, pydantic, pytest, black, ruff, mypy, wsqlite, sphinx-rtd-theme, sphinx-copybutton, myst-parser, sphinx-sitemap, sphinx-design | ✅ Yes |
| Apache-2.0 | requests | ✅ Yes |
| BSD-3-Clause | pandas, uvicorn, sphinx | ✅ Yes |
| BSD-2-Clause | sphinx | ✅ Yes |
| MPL-2.0 | tqdm (dual license) | ✅ Yes |

---

## Security Advisories

### Known Vulnerabilities (as of April 13, 2026)

- **None reported** for any runtime dependency at minimum specified versions

### How to Check

To check for new vulnerabilities:

```bash
# Install safety and pip-audit
pip install safety pip-audit

# Check dependencies
safety check
pip-audit
```

---

## Supply Chain Risk Assessment

### Risk Level: LOW

**Justification**:
- All dependencies are well-established packages with millions of downloads
- No obscure or rarely-maintained packages
- All packages use permissive open-source licenses
- No binary dependencies (pure Python)
- No network calls at install time
- No post-install scripts

### Mitigations in Place

1. **CI Security Scanning**: Every PR runs `pip-audit` and `safety check`
2. **Dependabot**: Automated dependency updates weekly
3. **Lock Files**: Dependencies use minimum version pins
4. **Code Review**: All dependency changes reviewed via PR

---

## Build Artifacts

| Artifact | Type | Description |
|----------|------|-------------|
| wpipe-2.0.0-py3-none-any.whl | Wheel | Universal Python wheel |
| wpipe-2.0.0.tar.gz | Source | Source distribution (sdist) |

**Build System**: hatchling
**Python Tag**: py3 (Python 3 universal)
**Platform Tag**: none-any (platform independent)

---

## Verification

To verify this SBOM matches your installation:

```bash
# Install wpipe
pip install wpipe==2.0.0

# List installed dependencies
pip show wpipe
pip list --format=freeze | grep -E "(requests|loguru|pandas|pyyaml|tqdm|rich|pydantic|fastapi|uvicorn|wsqlite)"

# Verify versions meet minimum requirements
pip check
```

---

## Updates

This SBOM will be updated with each release to reflect:
- Added dependencies
- Removed dependencies
- Version requirement changes
- License changes

---

**SBOM Version**: 1.0
**Last Updated**: April 13, 2026
**Next Update**: With next release (2.0.1 or later)
**Maintainer**: wisrovi (William Steve Rodriguez Villamizar)
