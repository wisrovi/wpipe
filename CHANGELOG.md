# WPipe Changelog

All notable changes to WPipe will be documented in this file.

---

## [2.0.0] - 2026-04-13

### LTS Certification
- **Long-Term Support release** with 5-year support until April 2031
- Minimum 90% test coverage for core components
- Consistent version declarations across all files
- Formal LTS policy document (LTS_POLICY.md)
- Public API contract document (PUBLIC_API.md)
- Software Bill of Materials (SBOM.md)

### Added
- **ParallelExecutor**: Execute pipeline steps in parallel (I/O or CPU bound)
- **ExecutionMode**: IO_BOUND, CPU_BOUND, SEQUENTIAL options
- **DAGScheduler**: Dependency graph management with topological sorting
- **PipelineAsStep**: Use pipelines as steps in other pipelines
- **@step()** decorator: Inline step definition with metadata
- **StepRegistry**: Central registry for decorated steps
- **AutoRegister**: Bulk step registration
- **ResourceMonitor**: Track RAM/CPU during execution
- **ResourceMonitorRegistry**: Monitor management
- **PipelineExporter**: Export logs, metrics, statistics to JSON/CSV
- **TypeValidator**: Runtime type validation for pipeline context
- **PipelineContext**: Typed pipeline context
- **GenericPipeline**: Generic typed pipeline support
- **CheckpointManager**: Save and resume from checkpoints
- **TimeoutError**: Timeout exception class
- **TaskTimer**: Task timing utility
- **timeout_sync**: Sync function timeout decorator
- **timeout_async**: Async function timeout decorator
- **PipelineTracker**: Execution tracker
- **Metric**: Metric definition
- **Severity**: Severity levels enum
- **PipelineAsync**: Async pipeline support
- **For**: Loop construct for pipelines
- **CompositionHelper**: Composition utilities
- **NestedPipelineStep**: Nested pipeline step
- **Transform decorators**: to_obj, auto_dict_input, state, object_to_dict
- **Dashboard**: FastAPI dashboard with WebSocket support
- **Pre-commit hooks**: .pre-commit-config.yaml with ruff, black, mypy
- **Dependabot**: Automated dependency updates
- **LTS regression tests**: Comprehensive backward compatibility tests

### Fixed
- Version inconsistencies across pyproject.toml, setup.py, __init__.py, docs/conf.py
- setup.py python_requires mismatch (was >=3.6, now >=3.9)
- Test coverage threshold raised from 72% to 90%
- Checkpoint persistence in demo scenarios
- Database schema mismatch in export tools
- PROJECT_STATUS.md reconciliation with PHASE_2_COMPLETION_SUMMARY.md

### Infrastructure
- Added .pre-commit-config.yaml
- Added .github/dependabot.yml
- Added LTS_POLICY.md
- Added PUBLIC_API.md
- Added SBOM.md
- Added test/test_lts_regression.py

### Changed
- Version unified to 2.0.0 across all files
- Coverage fail_under raised to 90
- PROJECT_STATUS.md updated to reflect all phases complete

### Security
- GitHub Actions security workflow with pip-audit and safety
- Dependency review on PRs
- Weekly automated dependency updates via Dependabot


---

## [1.5.3] - 2026-04-10

### Added
- Official 2.0.0-LTS preparation.
- Minor fixes in examples.

---

## [1.5.1] - 2026-04-10

### Fixed
- Alert system API compatibility with new `expression` parameter
- Performance comparison example using `get_stats()` instead of deprecated method
- Reduced package size (42MB → 140KB) by excluding heavy examples

---

## [1.5.0] - 2026-04-10

### Added
- **ParallelExecutor**: Execute pipeline steps in parallel (ThreadPoolExecutor/ProcessPoolExecutor)
- **ExecutionMode**: IO_BOUND, CPU_BOUND, SEQUENTIAL
- **DAGScheduler**: Dependency graph management with topological sorting
- **PipelineAsStep**: Use pipelines as steps in other pipelines
- **@step()** decorator: Inline step definition
- **StepRegistry**: Central registry for decorated steps
- **ResourceMonitor**: Track RAM/CPU during execution
- **Exporter**: JSON/CSV export capabilities
- **Type validators**: Input/output validation

---

## [1.0.0] - 2024-04-01

### Added
- **Pipeline**: Core pipeline orchestration
- **Condition**: Conditional branching based on data
- **Retry**: Automatic retry with backoff
- **APIClient**: External API integration
- **SQLite/Wsqlite**: Data persistence
- **Error handling**: Custom exceptions with codes
- **YAML config**: Load configurations from YAML
- **Nested pipelines**: Compose complex workflows
- **Progress tracking**: Rich terminal output
- **Type hints**: Complete type annotations