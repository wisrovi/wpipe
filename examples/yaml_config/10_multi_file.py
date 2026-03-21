"""
10 YAML Config - Multi-File Configuration

Shows loading configuration from multiple YAML files.
"""

from wpipe.util import leer_yaml
import tempfile
import os


def main():
    config1 = {"part": 1, "value": 100}
    config2 = {"part": 2, "value": 200}

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f1:
        import yaml

        yaml.dump(config1, f1)
        temp_path1 = f1.name

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f2:
        yaml.dump(config2, f2)
        temp_path2 = f2.name

    loaded1 = leer_yaml(temp_path1)
    loaded2 = leer_yaml(temp_path2)

    print(f"Part 1: {loaded1['value']}, Part 2: {loaded2['value']}")

    os.unlink(temp_path1)
    os.unlink(temp_path2)


if __name__ == "__main__":
    main()
