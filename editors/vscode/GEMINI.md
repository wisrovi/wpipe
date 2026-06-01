# VS Code Extension Workflow

- Siempre que se realicen cambios en el código de la extensión (`editors/vscode/src/**`), se debe:
    1. Incrementar la versión en `package.json`.
    2. Actualizar el `CHANGELOG.md`.
    3. Ejecutar el script de construcción e instalación local: `bash package_local.sh` desde el directorio `editors/vscode`.
