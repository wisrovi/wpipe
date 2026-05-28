# Changelog - WPipe Tools

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
