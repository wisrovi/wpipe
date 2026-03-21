"""
10 YAML Config - Nested Configuration

Shows deeply nested configuration loading.
"""

from wpipe.util import leer_yaml
import tempfile
import os

def main():
    config = {
        "app": {
            "config": {
                "database": {"host": "localhost"},
                "cache": {"enabled": True}
            }
        }
    }
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        import yaml
        yaml.dump(config, f)
        temp_path = f.name
    
    loaded = leer_yaml(temp_path)
    print(f"DB Host: {loaded['app']['config']['database']['host']}")
    
    os.unlink(temp_path)

if __name__ == "__main__":
    main()
