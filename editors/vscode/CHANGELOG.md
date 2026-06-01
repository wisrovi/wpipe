# Changelog

## [0.8.5] - 2026-06-01

### Fixed
- **Broadened Exclusion Logic**: Expanded the workspace search exclusion list to include more virtual environment patterns (`.env`, `env`, `.conda`, `conda`, `venv`). This prevents scanning internal package files which could lead to performance issues or missing user steps.

## [0.8.4] - 2026-06-01

### Fixed
- **Workspace Step Search**: Corrected the glob exclude pattern in `findFiles`. Previously, the malformed pattern caused the extension to scan thousands of files in `.venv` and `node_modules`, often hitting the 50-file limit before finding actual project steps.
- **Search Performance**: Increased the workspace search limit to 500 files and optimized the exclusion of library directories, significantly improving responsiveness and reliability when refreshing steps.

## [0.8.3] - 2026-06-01

### Added
- **Personal Branding (wisrovi)**: Updated extension metadata, README badges, and added a "Meet the Author" section to officially recognize the author's identity and link to professional profiles.
- **Improved UX**: Enhanced visual presence of the author's brand across all interactive tools (Cheat Sheet and DAG Analysis).

### Changed
- Incremented version for deployment and marketplace synchronization.

## [0.8.2] - 2026-06-01

### Added
- **Compatibilidad con Antigravity**: Refactorización completa para soportar entornos web (vscode.dev, GitHub Codespaces, etc.) eliminando dependencias de Node.js nativo.
- **Implementación de Dashboard**: El comando `WPipe: Open Web Dashboard` ahora es funcional, permitiendo seleccionar la DB de tracking y el puerto de forma interactiva.
- **Hoja de trucos (Cheat Sheet)**: Nuevo comando `WPipe: Show Cheat Sheet` con acceso rápido a snippets y comandos.
- **Ejecución de Pasos**: Comando `Run this Step` en el explorador lateral para probar estados individuales.

### Changed
- **Iconos Optimizados**: Rediseño y ajuste de dimensiones de los iconos (`icon.png` a 128x128 y `lateral_icon.png` a 24x24) para cumplir con los estándares de VS Code.
- **Refactorización de Código**: Migración de `fs` y `https` a `vscode.workspace.fs` y `fetch` para compatibilidad multiplataforma.

### Fixed
- Error en el registro de comandos que impedía el funcionamiento del Dashboard.
- Problemas de visualización de iconos en temas oscuros y claros.

---
 - WPipe Tools

## [0.8.1] - 2026-05-31
### Changed
- **README Polishing**: Streamlined the documentation to be strictly user-facing, removing technical build instructions for a cleaner marketing focus.
- **Onboarding Experience**: Simplified the "Getting Started" guide to prioritize immediate visual feedback for new users.

## [0.8.0] - 2026-05-31
### Added
- **International Documentation**: Complete re-write of the extension's README in professional English, optimized for global developers.
- **Enhanced Visual Communication**: Improved feature descriptions and command documentation for better clarity and onboarding.
- **Build Optimization**: Refined local packaging scripts for more reliable version deployments.
- **Marketplace Readiness**: Prepared all metadata and documentation for high-visibility publishing.

## [0.7.9] - 2026-05-30
### Added
- **Suite de Análisis High-Fidelity**: Transformación del DAG en un panel de análisis profesional con cabecera enterprise, barra lateral de estadísticas y pie de página con versión del motor.
- **Análisis de Complejidad (Big O)**: Cálculo automático del coste computacional teórico de la orquestación (O(n), O(n²), etc.) basado en la profundidad de los bucles y ramificaciones.
- **Interactividad Total (Zoom & Pan)**: Integración de `svg-pan-zoom` que permite navegar por grafos complejos usando la rueda del ratón y arrastre de lienzo.
- **Barra de Herramientas Flotante**: Controles rápidos de Zoom In, Zoom Out y Reset/Center en el visor de arquitectura.
- **Catálogo Cloud-Native**: Sincronización en tiempo real con GitHub para descargar los 130+ estados oficiales y de comunidad sin necesidad de actualizar la extensión.
- **Reconocimiento de Autor**: Tooltips enriquecidos en el panel lateral que muestran el nombre del autor y el repositorio de origen para cada plugin.
- **Auto-Importación Inteligente**: Al hacer clic en un estado de la librería, se inyecta automáticamente el `import` y la instancia (con paréntesis si es clase) en el editor activo.
- **Semántica de Flujo**: Etiquetas claras de "True" e "False" en las flechas de condiciones y nuevos iconos visuales (Cohete para pasos, Rayo para Paralelo).
- **Icono de Actividad**: Actualizado el icono de la barra lateral de VS Code al cohete oficial de WPipe para una identidad de marca coherente.

### Fixed
- **Estabilidad de Activación**: La carga del catálogo ahora es no-bloqueante (background task), resolviendo conflictos con IntelliCode y otros servicios de lenguaje.
- **Soporte `add_state`**: El DAG y el explorador lateral ahora reflejan fielmente los estados añadidos dinámicamente mediante llamadas a `.add_state()`.
- **Navegación Precisa**: Al hacer clic en un estado del workspace, el editor se posiciona exactamente en la línea de la implementación (`def` o `class`) en lugar del decorador.
- **Filtrado de Workspace**: Se ignoran automáticamente carpetas de sistema (`.venv`, `node_modules`, `wpipe` core) para evitar ruido en la lista de estados del usuario.

## [0.6.3] - 2026-05-28
### Fixed
- **Dirección del Grafo**: Se ha añadido explícitamente `direction TD` (Top-Down) a todos los subgrafos generados (`For`, `Parallel`, `Background` y múltiples Pipelines). Esto evita que Mermaid expanda horizontalmente el diagrama y fuerza una estructura vertical mucho más limpia y natural.
- **Pipelines Únicos**: Cuando un archivo solo contiene un pipeline, ya no se envuelve en un subgrafo general "Pipeline 1", evitando marcos visuales innecesarios.

## [0.6.2] - 2026-05-28
### Added
- **Soporte para Múltiples Pipelines**: La extensión ahora es capaz de renderizar múltiples pipelines definidos en un mismo archivo. Cada pipeline se visualiza dentro de su propio subgrafo independiente en el Mermaid generado.
### Fixed
- **Comillas Anidadas en Condiciones**: Corregida la expresión regular que extrae el contenido de `expression` y `validation_expression` en los bloques lógicos. Ahora soporta correctamente comillas simples y dobles anidadas (ej. `status != 'error'`), evitando que Mermaid se rompa y deje de renderizar.

## [0.6.1] - 2026-05-28
### Fixed
- **Comentarios en Python**: El generador del DAG ahora ignora correctamente los comentarios (`# ...`) dentro del array de `set_steps`, evitando que rompan los IDs de los nodos y el texto de las etiquetas en Mermaid.
- **Caracteres Especiales**: Se reemplazan automáticamente las comillas dobles internas en los nombres de los pasos para prevenir errores de sintaxis en Mermaid.

## [0.6.0] - 2026-05-28
### Added
- **Selector de Archivos**: Al usar el comando `Open Dashboard`, ahora se abrirá un diálogo nativo del sistema operativo (Explorador de Archivos) que permite buscar y seleccionar visualmente el archivo de base de datos `.db` o `.sqlite`, en lugar de tener que escribir la ruta a mano.

## [0.5.9] - 2026-05-28
### Added
- **Mejora del WPipe Cheat Sheet**: El panel de ayuda ahora muestra un HTML estructurado y estéticamente mejorado, documentando todos los nuevos snippets (Pipelines, Steps, Lógica y Monitoreo) y los comandos de la extensión.
### Fixed
- **Comando Open Dashboard**: Reescrito para solicitar interactivamente al usuario la ruta de la base de datos de tracking, el directorio de configuración y el puerto, lanzando correctamente `python -m wpipe.dashboard`.

## [0.5.8] - 2026-05-28
### Added
- **Advertencias Prominentes**: Modificados los snippets `wpevent` y `wpalert` para incluir un bloque de comentario mucho más llamativo advirtiendo sobre la necesidad obligatoria de configurar `tracking_db` en el pipeline, actualizando también la descripción del snippet.

## [0.5.7] - 2026-05-28
### Added
- **Avisos en Snippets**: Añadido un comentario recordatorio en los snippets `wpevent` y `wpalert` indicando que su uso requiere que el pipeline haya sido inicializado con una base de datos de tracking (`tracking_db`).

## [0.5.6] - 2026-05-28
### Fixed
- **Snippet Importaciones**: Corregida la importación del decorador `@step` en el snippet `wperrorcapture` para que importe directamente desde `wpipe` en lugar de `wpipe.decorators`.

## [0.5.5] - 2026-05-28
### Fixed
- **Snippets de Pipeline**: Actualizados los snippets `wppipe` y `wppipeadv` para incluir manejo de errores mediante bloque `try-except` con `ProcessError`, y su correspondiente importación automática.

## [0.5.4] - 2026-05-28
### Fixed
- **Snippet wpstepadv**: Corregida la posición de los decoradores `@timeout_sync` y `@to_obj`, moviéndolos directamente al método `__call__` de acuerdo con las mejores prácticas de WPipe.

## [0.5.3] - 2026-05-28
### Fixed
- **Snippet wpstepadv**: Actualizado el snippet avanzado para que incluya y utilice correctamente `PipelineContext` y el decorador `@to_obj`, ofreciendo una plantilla de clase robusta y completamente tipada.

## [0.5.2] - 2026-05-28
### Added
- **Actualización Manual**: Añadido un botón de "Refresh" en la barra de título del panel "Step Registry Explorer" para actualizar la lista de pasos manualmente.

## [0.5.1] - 2026-05-28
### Fixed
- **Snippet Pipeline**: Corregido el snippet `wppipe` que proponía `pipeline.tracker.enable_resource_monitoring()`, reemplazándolo por el parámetro correcto `collect_system_metrics=True` en la inicialización del Pipeline.

## [0.5.0] - 2026-05-28
### Added
- **Snippets Profesionales**: Nuevos atajos de autocompletado para Python:
    - `wpstepadv`: Estado basado en clase con todas las propiedades del decorador, reintentos y timeouts.
    - `wppipeadv`: Configuración avanzada de Pipeline con gestión de errores, métricas y retries globales.
    - `wperrorcapture`: Plantilla completa para capturador de errores personalizado.
    - `wpevent`: Acceso rápido para añadir eventos personalizados al flujo.
    - `wpalert`: Configuración de umbrales de alerta basados en métricas (LTS).

## [0.4.9] - 2026-05-28
### Fixed
- **Parser de Python Robusto**: Se ha mejorado drásticamente la detección del bloque `set_steps` principal, evitando falsos positivos con bloques anidados.
- **Correcion de Mermaid**: Mejoras en la estructura de los subgrafos y conexiones para reflejar fielmente la jerarquía del pipeline.
- **Estabilidad de Exportación**: Corregido el guardado de archivos `.mermaid` en la carpeta local.

## [0.4.8] - 2026-05-28
### Added
- **Exportación Automática**: El código Mermaid generado ahora se guarda automáticamente en un archivo `.mermaid` en la misma carpeta que el archivo del pipeline.

## [0.4.7] - 2026-05-28
### Added
- **Subgrafos Avanzados**: Visualización mejorada de bloques `For`, `Parallel` y `Background` con etiquetas dinámicas.
- **Relaciones Asíncronas**: Conexión visual explícita entre disparadores y ejecución de tareas en background.

## [0.4.6] - 2026-05-28
### Fixed
- **Mejora del DAG RT**: El flujo del pipeline ahora se reconecta correctamente después de bloques `Condition` y `Parallel`.
- **Soporte para Tuplas**: Ahora el DAG detecta correctamente los pasos definidos como tuplas `(func, "nombre", "v1.0")`.
- **Flujo de Background**: Los pasos `Background` ya no bloquean visualmente la línea principal del pipeline.
- **Estabilidad de IDs**: Sanitización mejorada de IDs de nodos para evitar re-renderizados bruscos al escribir.
- **Extracción de Argumentos**: Soporte mejorado para extraer contenidos de ramas condicionales y pasos paralelos.
- **YAML mejorado**: Mejor detección de nombres de pasos en archivos de configuración YAML.

## [0.4.2] - 2026-05-28
### Fixed
- Error de sintaxis en el DAG ("Syntax error in text") mediante sanitización de IDs de nodos.
- Soporte mejorado para nombres de funciones con puntos o caracteres especiales.
### Added
- Formas visuales para `Condition` (diamante), `Parallel` (cápsula) y `For` (estadio) en el DAG.

## [0.4.1] - 2026-05-28
### Added
- Nuevo icono lateral (`lateral_icon.png`) diseñado para la barra de actividad.
- Soporte para multi-workspace en el "Step Registry Explorer".
- Detección de tanto `@step` como `@state` en el explorador de pasos.

## [0.4.0] - 2026-05-28
### Added
- **WPipe Cheat Sheet**: Ayuda visual integrada con el comando `WPipe: Show Cheat Sheet / Help`.
- **One-Click Test**: Ejecución individual de pasos desde el menú contextual del Step Registry.
- Importaciones automáticas en todos los snippets de Python.
- Configuración de base de datos y métricas por defecto en el snippet de `Pipeline`.

## [0.3.0] - 2026-05-28
### Added
- **Step Registry Explorer**: Panel lateral para navegar por todos los pasos del proyecto.
- **DAG Dinámico**: Visualización en tiempo real basada en el análisis del código Python y YAML.

## [0.2.0] - 2026-05-28
### Added
- Snippet `wpstate` para creación de estados basados en clases con `@to_obj` y `PipelineContext`.
- Soporte mejorado para validación de tipos en snippets.

## [0.1.0] - 2026-05-28
### Added
- Estructura base de la extensión.
- Snippets iniciales para Python y YAML.
- Validación de esquemas JSON para archivos YAML de WPipe.
- Comando inicial Hello World.
