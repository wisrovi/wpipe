"""
09 YAML Config - Environment Variables

Shows using environment variables in YAML config.
"""

import os
import tempfile

import yaml

from wpipe.util import leer_yaml


def main() -> None:
    """Execute the environment variables in YAML config example."""
    os.environ["TEST_VAR"] = "test_value"

    config = {"env_var": os.environ.get("TEST_VAR")}

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(config, f)
        temp_path = f.name

    loaded = leer_yaml(temp_path)
    print(f"Env var value: {loaded['env_var']}")

    os.unlink(temp_path)


if __name__ == "__main__":
    main()
