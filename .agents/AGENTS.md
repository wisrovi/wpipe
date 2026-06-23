# Workspace Rules for WPipe Project

## VS Code Extension Development & Auto-Installation
Whenever you modify files in the `editors/vscode/` directory (such as `package.json`, `src/extension.ts`, or settings), you MUST immediately rebuild and install the extension locally to ensure both VS Code and your environment are synchronized.

To do this, execute the local packaging script from the extension's folder:
```bash
cd editors/vscode
./package_local.sh
```

## Step Search Shortcut
The keyboard shortcut for searching and importing steps (`wpipe-vscode.searchSteps`) is configured to:
- `Ctrl+Alt+W` / `Cmd+Alt+W`
- Fallback: `Ctrl+Shift+Alt+W` / `Cmd+Shift+Alt+W`
- Target Condition: `"when": "editorTextFocus"`
