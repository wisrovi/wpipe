"""
Example: YAML Configuration Loading

This example demonstrates how to load configuration from YAML files
and use them with the Pipeline.
"""

from wpipe.pipe import Pipeline
from wpipe.util import escribir_yaml, leer_yaml


def load_config(data: dict) -> dict:
    """Load configuration from file."""
    config = leer_yaml(data["config_path"])
    return {"config": config, "loaded": True}


def apply_config(data: dict) -> dict:
    """Apply the loaded configuration."""
    config = data.get("config", {})
    return {
        "service_name": config.get("name", "unknown"),
        "version": config.get("version", "unknown"),
        "applied": True,
    }


def validate_setup(data: dict) -> dict:
    """Validate the setup."""
    return {
        "valid": True,
        "service": data.get("service_name"),
        "version": data.get("version"),
    }


def main():
    """Demonstrate YAML configuration loading."""
    import os
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = os.path.join(tmpdir, "config.yaml")

        config_data = {
            "name": "example_service",
            "version": "v1.0.0",
            "settings": {"timeout": 30, "retries": 3},
        }

        escribir_yaml(config_path, config_data)
        print(f"Created config at: {config_path}")

        pipeline = Pipeline(verbose=True)
        pipeline.set_steps(
            [
                (load_config, "Load Config", "v1.0"),
                (apply_config, "Apply Config", "v1.0"),
                (validate_setup, "Validate Setup", "v1.0"),
            ]
        )

        result = pipeline.run({"config_path": config_path})
        print(f"Result: {result}")

        assert result["loaded"] is True
        assert result["applied"] is True
        assert result["service_name"] == "example_service"

        print("Configuration loaded and applied successfully!")


if __name__ == "__main__":
    main()
