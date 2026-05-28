# WPipe VS Code Extension 🚀

Esta extensión proporciona herramientas inteligentes para trabajar con la librería **WPipe** directamente en Visual Studio Code.

## Características actuales

- **Snippets para Python:**
  - `wpstep`: Crea rápidamente un paso de pipeline con decorador (basado en función).
  - `wpstate`: Crea un estado basado en clase con `@to_obj` y `PipelineContext` (recomendado para validación de tipos).
  - `wppipe`: Estructura básica de un pipeline con **base de datos y métricas activas**.
  - `wpparallel`, `wpcondition`, `wpfor`, `wpbackground`: Estructuras lógicas con **importaciones automáticas**.

- **Step Registry Explorer:**
  - Nueva vista en la barra lateral que muestra todos los pasos (`@step`) definidos en tu workspace.
  - Haz clic en cualquier paso para saltar directamente a su código.

- **Visualización de DAG en Tiempo Real:**
  - Renderiza el flujo del pipeline mientras lo construyes.
  - Soporte para archivos `.py` (basado en `set_steps`) y archivos `.yaml`.
  - Se actualiza automáticamente al guardar o editar el archivo.
- **Snippets para YAML:**
  - `wpyaml`: Estructura base para configuraciones de pipeline en YAML.
- **Comandos:**
  - `WPipe: Hello World`: Comando de prueba para verificar la activación.

## Próximos pasos (Roadmap)

1. **Visualización de DAG:** Renderizar el flujo del pipeline en un panel lateral.
2. **Validación de YAML:** Autocompletado y validación de esquemas para archivos `.yaml` de WPipe.
3. **Monitoreo en tiempo real:** Integración con el dashboard de WPipe.

## Cómo crear e instalar la extensión (Local)

Si deseas generar el instalador manualmente para usarlo en tu VS Code local o compartirlo, sigue estos pasos:

### 1. Requisitos previos
- Tener instalado **Node.js** y **npm**.
- Tener instalado el empaquetador oficial de VS Code:
  ```bash
  npm install -g @vscode/vsce
  ```

### 2. Generar el paquete (.vsix)
Desde la carpeta raíz del proyecto o desde `editors/vscode`, ejecuta el script de empaquetado automático:
```bash
cd editors/vscode
./package_local.sh
```
Este script se encargará de instalar las dependencias necesarias, compilar el código TypeScript y generar un archivo llamado `wpipe-vscode-0.1.0.vsix`.

### 3. Instalar en VS Code
Una vez generado el archivo `.vsix`, instálalo siguiendo estos pasos:
1. Abre **Visual Studio Code**.
2. Ve a la vista de **Extensiones** (`Ctrl+Shift+X`).
3. Haz clic en el menú de "tres puntos" (`...`) en la esquina superior derecha del panel de extensiones.
4. Selecciona la opción **"Install from VSIX..."**.
5. Busca y selecciona el archivo `wpipe-vscode-0.1.0.vsix` que acabas de generar.

## Cómo publicar en el Marketplace
Para subir la extensión de forma oficial:
1. Asegúrate de tener un **Personal Access Token (PAT)** de Azure DevOps con permisos de "Marketplace Manage".
2. Ejecuta el script de publicación:
   ```bash
   ./publish_marketplace.sh TU_TOKEN_DE_AZURE
   ```

---
Desarrollado para potenciar la orquestación de datos con WPipe.
