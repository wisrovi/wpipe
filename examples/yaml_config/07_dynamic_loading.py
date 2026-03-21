"""
07 YAML Config - Dynamic Loading

Shows dynamically loading and executing from YAML.
"""

from wpipe.util import leer_yaml
import tempfile
import os

def main():
    config = {
        "steps": [
            {"name": "Step 1", "function": "step1"},
            {"name": "Step 2", "function": "step2"},
        ]
    }
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        import yaml
        yaml.dump(config, f)
        temp_path = f.name
    
    loaded = leer_yaml(temp_path)
    print(f"Loaded config: {loaded}")
    
    os.unlink(temp_path)

if __name__ == "__main__":
    main()
