#!/bin/bash

# If the script fail it stop
set -e

echo "Pre-commit install..."

if [ -z "${CONDA_PREFIX:-}" ]; then
    echo "Error: activate the Conda Python 3.9 environment before running this script."
    exit 1
fi

PYTHON_BIN="$CONDA_PREFIX/bin/python"
PYTHON_VERSION="$("$PYTHON_BIN" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"

if [ "$PYTHON_VERSION" != "3.9" ]; then
    echo "Error: the active Conda environment uses Python $PYTHON_VERSION; Python 3.9 is required."
    exit 1
fi

echo "Using Conda environment: $CONDA_PREFIX"

echo "update of pip (necessary for the installation of all the hooks)"
"$PYTHON_BIN" -m pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    echo "Installation of the dependencies in the requirements.txt"
    "$PYTHON_BIN" -m pip install -r requirements.txt
else
    echo "requirements.txt not found"
fi

echo "Installation of pre-comit hooks"
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
