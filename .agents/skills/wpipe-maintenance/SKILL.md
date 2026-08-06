---
name: wpipe-maintenance
description: Handles core library maintenance for wpipe, including example validation (pytest), concurrency fixes, version bumping, PyPI publication, and repository synchronization. Use when making changes to the 'wpipe/' directory or preparing a new release.
---

# wpipe Maintenance

This skill provides a standardized workflow for maintaining the `wpipe` core library. It ensures that all changes are verified against the extensive example suite and correctly published.

## Workflows

### 1. Verification and Validation
ALWAYS run the automated example tests after any change to the core library (`wpipe/`).

- **Command**: `pytest test/test_examples.py`
- **Goal**: 100% Success (or legitimate skips).
- **Minimum Viable Test**: the Honey Pot suite under `examples/00_honey_pot/` MUST all run — special attention to `03_yield/` (142 demo levels covering sync/async pipelines, `tracking_db`, alerts, export, dashboard data). Targeted run: `pytest test/test_examples.py -k "honey_pot or demo_level"`. See the **Minimum Viable Test** section in `.agents/AGENTS.md` for details.
- **Handling Failures**:
  - If a test fails, analyze `STDOUT` and `STDERR`.
  - Prioritize library fixes (e.g., handling concurrency, fixing imports) over modifying examples.
  - Do NOT modify existing examples under `examples/00_honey_pot/` (regression suite); add NEW examples instead.
  - If an example is broken due to old API usage, add a compatibility alias in `wpipe/__init__.py`.

### 2. Cleanup
Before committing or publishing, remove all temporary execution artifacts.

- **Artifacts to remove**:
  - `*.db`, `*.db-shm`, `*.db-wal`
  - `logs/`, `output/`, `pipeline_configs/`
  - `reporte_ejemplos.csv`, `validate_examples.py`

### 3. PyPI Publication
When the library is stable and all tests pass:

1. **Bump Version**: Update `version` in both `setup.py` and `pyproject.toml`.
2. **Build**: `rm -rf dist/ build/ *.egg-info && python3 -m build`
3. **Upload**: Use `twine` with the provided token from Global Personal Memory.
   ```bash
   TWINE_USERNAME=__token__ TWINE_PASSWORD=<token> python3 -m twine upload dist/*
   ```

### 4. Repository Sync
- **Stage**: Add library fixes, the `test_examples.py` file, and version bumps.
- **Commit**: Use a descriptive message summarizing the fixes and improvements.
- **Push**: `git push origin main`

## Technical Guardrails

- **Concurrency**: SQLite writes MUST include retry logic (see `wpipe/__init__.py`'s `patched_insert`).
- **Compatibility**: Maintain aliases for `TimeoutError`, `set_states`, etc.
- **Pickle Safety**: Standalone functions should be used for `ProcessPoolExecutor` steps to avoid pickling locks.
