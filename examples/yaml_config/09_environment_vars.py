"""
09 YAML Config - Environment Variables

Shows using environment variables in YAML config.
"""

from wpipe.util import leer_yaml
import tempfile
import os

def main():
    os.environ["TEST_VAR"] = "test_value"
    
    config = {"env_var": os.environ.get("TEST_VAR")}
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        import yaml
        yaml.dump(config, f)
        temp_path = f.name
    
    loaded = leer_yaml(temp_path)
    print(f"Env var value: {loaded['env_var']}")
    
    os.unlink(temp_path)

if __name__ == "__main__":
    main()
