# Changelog

## [1.0.1 LTS] - 2026-06-22

### Added
- **Buscador de Estados Unificado**: El buscador de estados ahora integra dinámicamente los estados definidos localmente en el workspace y los estados remotos en una sola lista de búsqueda.
- **Búsqueda por Categoría**: La descripción de los ítems en el QuickPick incluye la jerarquía de categorías, lo que permite buscar por subcategoría (ej. escribir "redis" filtrará todos los estados de esa tecnología).
- **Atajo de Teclado**: Se ha agregado el atajo de teclado global `Ctrl+Alt+S` (o `Cmd+Alt+S` en macOS) para abrir el buscador de estados de manera instantánea.
- **Filtro de Plantillas**: Se excluyen los archivos `__init__.py` al listar plantillas de ejemplos para descargar.

## [1.0.0 LTS] - 2026-06-22

### Added
- **Categorización Jerárquica**: Los estados oficiales y comunitarios en el panel lateral (Step Registry) ahora se organizan jerárquicamente en subcarpetas basadas en `category`, `subcategory1`, `subcategory2` y `subcategory3`.
- **Organización Limpia**: Los estados sin categoría definida se agrupan automáticamente bajo una carpeta virtual "General", manteniendo la raíz del menú lateral limpia y organizada.
- **Native Webview Dashboard**: WPipe monitoring dashboard now opens directly inside a VS Code tab.
- **Bi-directional DAG Interaction**: Click on any node in the DAG to jump to the corresponding line of code.
- **Log Replay & Error Highlighting**: New command `WPipe: Replay Log Errors` to visualize failures from log files directly in the editor and DAG.
- **Impact Analysis**: Right-click on workspace steps in the sidebar to find all their usages and analyze the impact of changes.
- **AI Pipeline Assistant**: Generate complex pipeline structures from natural language descriptions.
- **Optimization Suggestions**: The DAG panel now provides automatic tips for performance (e.g., parallelism suggestions).
- **Quick Fixes**: Added a "Convert to WPipe Step" lightbulb action for standard Python functions.
- **YAML & Catalog Validation**: Real-time warnings if steps in a pipeline are missing from the workspace or catalog.
- **Enhanced Exports**: Added support for exporting the DAG as **PNG** in addition to SVG.

### Changed
- **Unified Branding**: Updated all icons and visual elements for a consistent v1.0 experience.
- **AST Parser Improvements**: Faster and more precise detection of pipelines and steps.

## [0.9.10] - 2026-06-07

### Added
- **Configuración Personalizada**: Soporte para el archivo `wpipe.config.json` en la raíz del workspace para configurar el comportamiento de la extensión de forma persistente y compartible.
- **Control de Respaldos**: Nueva opción `wpipe.enableBackupFile` para activar/desactivar la generación automática de archivos de respaldo.

### Fixed
- **Optimización de Archivos**: Se ha corregido el error que creaba archivos de respaldo para todos los archivos Python abiertos. Ahora, los archivos `.wpipe.mermaid` solo se generan de forma manual (al abrir el DAG) o al guardar archivos específicos, evitando el desorden en el proyecto.
- **Nueva Extensión de Respaldo**: Los respaldos ahora utilizan la extensión `.wpipe.mermaid` para una mejor identificación y soporte nativo de sintaxis Mermaid.

## [0.9.9] - 2026-06-01

### Changed
- **Convención de Nomenclatura**: Se ha actualizado el sufijo de exportación automática del DAG a `_dag.wpipe.md` para identificar claramente los archivos de documentación generados por la extensión.

## [0.9.8] - 2026-06-01

### Added
- **Motor DAG de Precisión**: Rediseño completo del motor de generación de Mermaid. Ahora las etiquetas de decisión ("True", "False", "exit") aparecen correctamente en las flechas de salida de los bloques lógicos, eliminando la confusión visual en ramas anidadas.
- **Visualización de Background**: Las tareas `Background` ahora se representan con líneas punteadas (`-. async .->`), permitiendo ver claramente qué pasos se ejecutan en paralelo sin detener el flujo principal.
- **Eliminación de Duplicados**: Corregido un error que causaba que pipelines complejos aparecieran varias veces en el mismo diagrama.

## [0.9.7] - 2026-06-01

### Fixed
- **Estabilidad del DAG**: Refactorización total de la inicialización de Mermaid. Ahora utiliza el API `render` explícito, eliminando parpadeos, paneles negros y fallos de carga.
- **Zoom Ultra-Preciso**: Re-implementado el sistema de Zoom con un rango de 0.001x a 100x, permitiendo navegar por pipelines de cualquier tamaño sin perder el control.
- **Exportación SVG Corregida**: El botón de descarga ahora utiliza un puente de mensajería seguro entre el editor y el sistema operativo, garantizando que la ventana de guardado aparezca siempre.

## [0.9.6] - 2026-06-01

### Added
- **Mapeo de add_state**: El motor AST ahora detecta y mapea correctamente los estados añadidos mediante `pipeline.add_state()`, integrándolos perfectamente en el flujo visual del DAG.
- **Exportación Automática a Markdown**: Cada vez que previsualizas el DAG, se genera automáticamente un archivo `<nombre>_dag.md` en la misma carpeta con el código Mermaid. Ideal para documentación y control de versiones.
- **Interactividad del DAG**: Añadido botón de **💾 Download SVG** para guardar el diagrama y botones mejorados de **Zoom In/Out** para navegar por pipelines complejos.

## [0.9.5] - 2026-06-01

### Added
- **Acceso Directo al Dashboard**: Ahora aparece un botón `📊 Open Dashboard` directamente sobre tu código si el Pipeline tiene configurada una `tracking_db`. La extensión detecta automáticamente la ruta de la base de datos y la pre-carga, permitiéndote abrir el dashboard con un solo clic sin tener que buscar el archivo manualmente.

## [0.9.3] - 2026-06-01

### Fixed
- **CodeLens Refinement**: Se ha eliminado el botón `Preview DAG` de los decoradores de estados individuales (`@step`), ya que el análisis de arquitectura solo es relevante a nivel de Pipeline. Ahora, el botón de previsualización del DAG aparece exclusivamente sobre las definiciones y ejecuciones de `Pipeline`.

## [0.9.2] - 2026-06-01

### Changed
- **Plantilla de Estado Profesional**: El asistente de creación de estados ahora genera archivos que siguen exactamente el estándar `wpstepadv`. Esto incluye el uso de Pydantic `BaseModel` para el contexto tipado, decoradores de `@timeout_sync` y `@to_obj`, y todos los parámetros avanzados de `@step` (retries, timeouts, tags).

## [0.9.1] - 2026-06-01

### Added
- **Hover Documentation**: Al pasar el ratón sobre un paso dentro de `set_steps`, ahora verás un popup con el nombre, versión y descripción del estado (tanto de tu workspace como de la librería oficial).
- **Inserción Contextual**: El botón `Add Logic Block` ahora es inteligente: detecta automáticamente los corchetes `[]` de `set_steps` e inserta el bloque directamente en su interior, sin importar dónde esté tu cursor.

## [0.9.0] - 2026-06-01

### Added
- **Snippets de Lógica Enriquecidos**: El asistente de `Add Logic Block` ahora inserta bloques completos con placeholders idénticos a los atajos de teclado (`wpfor`, `wpcondition`, etc.), facilitando el rellenado rápido de parámetros.
- **PascalCase Automático**: El mago de creación de estados ahora convierte automáticamente nombres como `mi_paso` a `MiPaso` para la definición de la clase, siguiendo las PEP8.
- **Scoping de CodeLens**: Se ha afinado la visibilidad de los CodeLens de ayuda; ahora el botón `Add Logic Block` solo aparece cuando detecta específicamente el método `.set_steps()` de un Pipeline.

## [0.8.9] - 2026-06-01

### Added
- **Asistente de Estados Inteligente**: El mago de creación de estados ahora capitaliza automáticamente el nombre de la clase y actualiza el archivo `states/__init__.py` con el export correspondiente, permitiendo importaciones limpias.
- **CodeLens para Pipeline**: Nuevo botón `▶ Run Pipeline` que aparece automáticamente sobre las definiciones de tu pipeline para ejecutar el script completo con un clic.
- **Asistente de set_steps**: Nuevo botón `➕ Add Logic Block` sobre los bloques de pasos que permite insertar rápidamente estructuras de `Condition`, `For`, `Parallel` o `Background` con placeholders inteligentes.

## [0.8.8] - 2026-06-01

### Added
- **CodeLenses en el Editor**: Ahora aparecen enlaces interactivos (`Run Step` y `Preview DAG`) directamente encima de cada decorador `@step` en el código. Ejecuta tus estados sin quitar las manos del teclado.
- **Asistente de Creación de Estados**: Nuevo comando `WPipe: Create New Advanced Step` que genera automáticamente una clase de estado profesional en una carpeta `states/` con su `__init__.py`, usando la plantilla de clase avanzada (LTS) de WPipe.

## [0.8.7] - 2026-06-01

### Added
- **Parser AST de Nivel Enterprise**: Integrado `@lezer/python` (el motor que usa CodeMirror) para el análisis de los archivos de Python. La búsqueda de pasos ahora comprende la estructura real del código (Abstract Syntax Tree), haciéndola 100% resistente a formateos de código complejos, comentarios multi-línea o cadenas de texto extrañas. ¡Adiós a las expresiones regulares frágiles!
- **Arquitectura Modular**: Refactorización completa del código base de la extensión (`src/extension.ts`), separando la lógica en un diseño escalable con módulos para Webviews, Proveedores y Servicios, preparando el terreno para futuras herramientas de UI visuales.
- **Esbuild Bundler**: Migrada la compilación de `tsc` a `esbuild`, resultando en tiempos de build de ~14ms y permitiendo incrustar librerías avanzadas sin romper la compatibilidad web ni aumentar el peso drásticamente.

## [0.8.6] - 2026-06-01

### Added
- **Configuración de Usuario**: Ahora puedes personalizar las rutas excluidas y el límite de búsqueda desde los ajustes de VS Code (`wpipe.excludePaths` y `wpipe.maxSearchFiles`).
- **Exclusión de Caché y Builds**: Se ignoran automáticamente directorios de caché (`__pycache__`, `.pytest_cache`, etc.) y carpetas de construcción (`build`, `dist`), mejorando drásticamente la velocidad de escaneo.

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
