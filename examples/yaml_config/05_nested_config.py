"""
05 YAML - Nested Configuration

Shows working with deeply nested YAML configurations.
"""

import os
import tempfile
from wpipe.util import leer_yaml, escribir_yaml


def main():
    config = {
        "app": {
            "name": "MyApp",
            "version": "1.0.0",
            "settings": {
                "database": {"host": "localhost", "port": 5432, "name": "mydb"},
                "cache": {"enabled": True, "ttl": 3600},
            },
        }
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        escribir_yaml(f.name, config)
        temp_path = f.name

    loaded = leer_yaml(temp_path)

    db_host = loaded["app"]["settings"]["database"]["host"]
    cache_enabled = loaded["app"]["settings"]["cache"]["enabled"]

    print(f"Database host: {db_host}")
    print(f"Cache enabled: {cache_enabled}")

    os.unlink(temp_path)


if __name__ == "__main__":
    main()
