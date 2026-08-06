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

## Minimum Viable Test (Validation)
After ANY change to the `wpipe/` core library, validate before finishing. Do NOT modify the existing examples (`examples/00_honey_pot/**`) — they are the regression suite. Adding NEW examples is allowed.

1. **Full example suite**: `pytest test/test_examples.py` — must be 100% success (legitimate skips for missing optional deps like `shapely`/`ultralytics`/`pandas` are OK).
2. **Honey Pot suite (minimum viable)**: all examples under `examples/00_honey_pot/` must run. Special attention to `03_yield/` (142 `demo_level*.py` covering sync/async pipelines, `tracking_db`, alerts, export, dashboard data). Quick targeted run:
   ```bash
   pytest test/test_examples.py -k "honey_pot or demo_level"
   ```
   Full run from the folder: `bash run_demos.sh` (needs optional deps like `cv2`).
3. **Tracking storage flag**: run the new example `examples/00_honey_pot/04_save_json_input_output/example.py` — it asserts that `save_json_input_output=False` stores NULL `input_data`/`output_data` in `steps`/`pipelines` and that the default `True` stores them.
4. **Dashboard**: must render with both flag values; step details show `N/A` for Input/Output when the payloads were not saved (no crash, no blank sections).

## Release Workflow
After every change (and once the Minimum Viable Test passes):
1. **Bump version** in BOTH `setup.py` and `pyproject.toml` (current: `2.5.0`; minor for features, patch for fixes).
2. **Update `CHANGELOG.md`** (Keep a Changelog format, in Spanish, current date).
3. **Update READMEs/docs** (root `README.md`, `docs/`, `extra_readmes/`) if the change affects usage.
4. **Publish to PyPI**:
   ```bash
   rm -rf dist/ build/ *.egg-info && python3 -m build
   TWINE_USERNAME=__token__ TWINE_PASSWORD=<token> python3 -m twine upload dist/*
   ```
   (`publish.sh` is available for this flow.) Then commit and push with a descriptive message.
