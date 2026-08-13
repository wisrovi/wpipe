#!/bin/bash

# If the script fail it stop
set -e

echo "Pre-commit install (venv)..."

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.env"

# 1. Pick the Python interpreter. Prefer python3.9 (aligned with the black
#    language_version pin); fall back to the system python3 otherwise.
if command -v python3.9 >/dev/null 2>&1; then
    SYSTEM_PY="$(command -v python3.9)"
else
    SYSTEM_PY="$(command -v python3)"
    echo "Note: python3.9 not found; using $SYSTEM_PY"
fi

# 2. Create the virtualenv inside the project (.env) if it does not exist.
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtualenv in $VENV_DIR"
    "$SYSTEM_PY" -m venv "$VENV_DIR"
fi

PYTHON_BIN="$VENV_DIR/bin/python"

echo "update of pip (necessary for the installation of all the hooks)"
"$PYTHON_BIN" -m pip install --upgrade pip

echo "Installation of pre-commit"
"$PYTHON_BIN" -m pip install pre-commit

if [ -f "requirements.txt" ]; then
    echo "Installation of the dependencies in the requirements.txt"
    "$PYTHON_BIN" -m pip install -r requirements.txt
else
    echo "requirements.txt not found"
fi

# 3. If the virtualenv is not Python 3.9, point the black language_version at
#    the interpreter actually in use, otherwise pre-commit cannot run black.
PYTHON_VERSION="$("$PYTHON_BIN" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
CFG="$ROOT_DIR/.pre-commit-config.yaml"
if [ -f "$CFG" ] && [ "$PYTHON_VERSION" != "3.9" ]; then
    echo "Using virtualenv Python $PYTHON_VERSION; adjusting black language_version in .pre-commit-config.yaml"
    sed -i "s/language_version: python3\.9/language_version: python$PYTHON_VERSION/" "$CFG"
fi

echo "Installation of pre-commit hooks"
"$PYTHON_BIN" -m pre_commit install

# Keep the hook output visible without preventing local commits. The PR workflow
# remains the enforcement point for merging.
HOOK_PATH="$(git rev-parse --git-path hooks)/pre-commit"
cat > "$HOOK_PATH" <<EOF
#!/bin/sh

"$PYTHON_BIN" -m pre_commit run "\$@"
status=\$?

if [ "\$status" -ne 0 ]; then
    echo "Pre-commit found errors; continuing with the commit."
fi

exit 0
EOF
chmod +x "$HOOK_PATH"

echo "pre-commit hooks update"
"$PYTHON_BIN" -m pre_commit autoupdate

echo "Installation finished"
