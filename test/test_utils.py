"""
Tests for utility functions.
"""

import os

import pytest

from wpipe.util import escribir_yaml, leer_yaml


class TestYamlUtilities:
    """Test YAML read/write utilities."""

    def test_leer_yaml_valid_file(self, yaml_config_file):
        """Test reading a valid YAML file."""
        result = leer_yaml(yaml_config_file)
        assert result is not None
        assert "name" in result
        assert result["name"] == "test_microservice"

    def test_leer_yaml_nonexistent_file(self, temp_dir):
        """Test reading a non-existent YAML file."""
        result = leer_yaml(os.path.join(temp_dir, "nonexistent.yaml"))
        assert result == {}

    def test_leer_yaml_nonexistent_file_verbose(self, temp_dir):
        """Test reading non-existent file with verbose mode."""
        result = leer_yaml(os.path.join(temp_dir, "nonexistent.yaml"), verbose=True)
        assert result == {}

    def test_escribir_yaml(self, temp_dir):
        """Test writing a YAML file."""
        yaml_path = os.path.join(temp_dir, "output.yaml")
        data = {"key": "value", "number": 42}
        escribir_yaml(yaml_path, data)
        assert os.path.exists(yaml_path)

        result = leer_yaml(yaml_path)
        assert result["key"] == "value"
        assert result["number"] == 42

    def test_escribir_yaml_verbose(self, temp_dir):
        """Test writing YAML with verbose mode."""
        yaml_path = os.path.join(temp_dir, "output_verbose.yaml")
        data = {"test": True}
        result = escribir_yaml(yaml_path, data, verbose=True)
        assert result is None
        assert os.path.exists(yaml_path)
