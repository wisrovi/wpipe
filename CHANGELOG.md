# WPipe Changelog

All notable changes to WPipe will be documented in this file.

---

## [2.0.0-LTS] - 2026-04-13

### Added
- **LTS Certification**: Long-Term Support release for mission-critical pipelines.
- **Improved Coverage**: Minimum 90% test coverage for core components.
- **Enhanced Reliability**: Stabilized Honey Pot and LogGestor examples.
- **Consistency**: PipelineExporter synchronized with unified PipelineModel schema.
- **API Maturity**: Full support for parallel execution and composition as stable features.

### Fixed
- Checkpoint persistence in demo scenarios.
- Database schema mismatch in export tools.

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