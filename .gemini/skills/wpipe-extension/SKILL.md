---
name: wpipe-extension
description: Workflow for maintaining and building the wpipe VS Code extension. Use when working in 'editors/vscode/' to compile, package, or update the extension.
---

# wpipe Extension Maintenance

This skill covers the development and release cycle of the VS Code extension for `wpipe`.

## Workflows

### 1. Build and Compile
Before packaging, ensure the extension is correctly compiled.

- **Directory**: `editors/vscode/`
- **Commands**:
  ```bash
  npm install
  npm run compile
  ```

### 2. Packaging (VSIX)
To generate a distributable `.vsix` file:

- **Command**: `vsce package` (Ensure `vsce` is installed or use `npx vsce package`).
- **Check**: Verify the version in `package.json` is correct before packaging.

### 3. Steps Catalog Generation
The extension often requires a `steps_catalog.json` to provide autocomplete for pipeline steps.

- **Command**: (Verify if there's a script in `editors/vscode/` or `generate_catalog.py` at project root).
- **Execution**: `python3 generate_catalog.py`

## Project Structure (Extension)

- `src/extension.ts`: Core logic for the extension.
- `package.json`: Extension metadata, commands, and contributions.
- `out/`: Compiled JavaScript.
