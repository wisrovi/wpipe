# wpipe Changelog

All notable changes to wpipe will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.4] - 2026-04-23

### Fixed
- **Resiliencia en Parallel**: Añadido fallback automático de Procesos a Hilos si los datos del contexto no son serializables (ej: generadores, locks), evitando el error `Can't pickle` que rompía la ejecución.

## [2.1.3] - 2026-04-23

### Fixed
- **Precisión de Traceback**: El reporte de errores ahora identifica correctamente el frame del código del usuario, ignorando frames de librerías externas (como numpy) para facilitar la depuración.
- **Nombres de Pasos**: Se ha mejorado la identificación del nombre del paso fallido, evitando el nombre genérico "task" y priorizando metadatos del decorador.

## [2.1.2] - 2026-04-23

### Fixed
- **Contención de SQLite**: Solucionado el error `database is locked` mediante la implementación de un commit único al finalizar el pipeline y gestión robusta de conexiones compartidas.
- **Colisión de Argumentos**: Corregido el fallo `multiple values for argument parent_step_id` que ocurría en ejecuciones paralelas anidadas dentro de bucles.
- **Barra de Progreso**: Corregido el `NameError: LiveError` en entornos donde Rich no está disponible o se carga de forma perezosa.

### Changed
- **Rendimiento de Carga**: Implementación de **Lazy Loading** en `wpipe/__init__.py` y decoradores, reduciendo el tiempo de importación inicial drásticamente.
- **Optimización de Ejecución**: Reducción del tiempo de ejecución del pipeline de ~300ms a < 15ms mediante el uso de `PRAGMA synchronous=OFF` y transacciones optimizadas en SQLite.
- **Arquitectura**: Los componentes pesados de UI (Rich, Tqdm) y Métricas (Psutil) ahora se cargan bajo demanda, evitando penalizaciones de tiempo si no se utilizan.

## [2.1.1] - 2026-04-23

### Changed
- **Branding & Identity**: Updated contact email to `wisrovi.rodriguez@gmail.com` and LinkedIn profile to `https://es.linkedin.com/in/wisrovi-rodriguez`.
- **Documentation**: Refreshed `index.html` with a modern, enterprise-grade design and updated all version references to v2.1.1 LTS across the project.
- **Consistency**: Synchronized versioning in `pyproject.toml`, `setup.py`, and Sphinx configuration.

## [2.1.0] - 2026-04-23

### Added
- **Tour de Aprendizaje (130 Niveles)**: Nuevo conjunto de 130 ejemplos guiados que cubren desde conceptos básicos hasta orquestación compleja, accesibles en la documentación y mediante `run_demos.sh`.
- **Tutorial Guiado en Sphinx**: Documentación renovada con un modo tutorial "Paso a Paso" que integra los 130 ejemplos con código fuente y resultados de ejecución.
- **Modernización de Sphinx**: Actualización total del motor de documentación con soporte para las últimas funcionalidades de la Fase 2 (Paralelismo, Composición, Decoradores).

### Changed
- **README e index.html**: Actualizados para reflejar el estado actual de la librería v2.1.0 LTS.
- **run_demos.sh**: Optimizado para ejecutar y validar los 130 niveles del tour de aprendizaje.

## [1.7.0] - 2026-04-22

### Added
- Mejoras generales de estabilidad y preparación para el lanzamiento mayor de la v2.1.0.

## [1.6.17] - 2026-04-21

### Fixed
- **Graph rendering**: Fixed step IDs to use step_order when id is null, enabling dashboard graph visualization.

## [1.6.16] - 2026-04-21

### Added
- ** serialización de objetos no serializables**: Los objetos como numpy arrays, objetos complejos, etc., ahora se convierten automáticamente a strings representativos antes de guardar en SQLite, evitando errores de serialización.

### Fixed
- **Barra de progreso**: Ahora muestra el formato `pipeline_name - task_name` en lugar de solo el nombre del paso.
- **Import duplicate**: Corregido error de importación duplicada de `nested` en example.py.

## [1.6.15] - 2026-04-20

### Added
- **Robustez en Tracking**: Soporte para objetos complejos y resiliencia ante referencias circulares en el contexto del pipeline.
- **Sincronización Thread-safe**: Implementación de bloqueos y manejo de conexiones seguras para SQLite en ejecuciones paralelas de alta intensidad.

### Fixed
- Resiliencia ante objetos no serializables en el contexto, permitiendo guardar checkpoints incluso con datos técnicos complejos.

## [1.6.3] - 2026-04-20
### Fixed
- Fixed critical bug in `CheckpointManager` where progress could not be saved if the context contained non-serializable objects (like `rich.progress.Progress`).
- Improved `Pipeline.run` to clean technical data before saving checkpoints.
- Fixed `step_name` retrieval in `save_checkpoint` for decorated steps.

## [1.6.2] - 2026-04-19

### Documentation and Example Refinement

Fixed critical missing decorator in README examples and synced version across all platforms.

### Fixed
- **README Example**: Added missing `@to_obj(Context)` decorator in the "Example of Power" to correctly show how data validation and object conversion is triggered.
- **Parity**: Ensured `to_obj` and `step` decorators are shown working together for best practices.

## [1.6.1] - 2026-04-19

### Stability and Persistence Refinement

This patch release resolves critical persistence issues in the LogGestor and unifies the internal database engine.

### Added
- **Native ID Tracking**: Implemented direct `rowid` capture for all SQLite operations, ensuring reliable record updates.

### Fixed
- **LogGestor Data Loss**: Fixed a bug where `output` and `details` were not persisted correctly due to ID synchronization issues.
- **Circular Imports**: Resolved module dependency conflicts between core components and SQLite wrappers.
- **Database Connector Robustness**: Improved connection pooling and thread safety for the internal WSQLite driver.

## [1.6.0] - 2026-04-19

### Persistence and Reliability Overhaul (Major Update)

This release focuses on architectural purity and reliability, unifying all persistence under `wsqlite` and enhancing the pipeline orchestration engine.

### Added
- **Intelligent Checkpoints**: New `add_checkpoint` method with expression evaluation for real-time milestone tracking.
- **Forensic Error Capture**: New `add_error_capture` system that provides file path and line number for easier debugging.
- **Unified WSQLite Persistence**: Removed all direct `sqlite3` dependencies in favor of `wsqlite` and Pydantic models.
- **High Resolution Resource Monitoring**: Enhanced CPU measurement for short-lived tasks.
- **PipelineAsync Parity**: Full feature parity between synchronous and asynchronous pipelines.
- **Progress Visibility Control**: New `show_progress` flag to toggle Rich progress bars.

### Changed
- **Turbo Mode Persistence**: Enabled WAL (Write-Ahead Logging) and connection pooling by default for massive performance gains.
- **Retry Hierarchy**: Step-level retry settings now correctly override global pipeline settings.

### Fixed
- **Database Locks**: Resolved 'database is locked' errors during high-concurrency executions.
