"""
08 YAML Config - Schema Validation

Shows validating YAML configuration against schema.
"""

import os
import tempfile

import yaml

from wpipe.util import leer_yaml


def main() -> None:
    """Execute the YAML schema validation example."""
    config = {"pipeline": {"name": "test", "version": "1.0", "steps": []}}

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(config, f)
        temp_path = f.name

    loaded = leer_yaml(temp_path)
    print(f"Pipeline name: {loaded['pipeline']['name']}")

    os.unlink(temp_path)


if __name__ == "__main__":
    main()
