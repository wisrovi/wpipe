"""
Tests for YAML configuration functionality.
"""

from wpipe.util import escribir_yaml, leer_yaml


class TestYamlUtilities:
    """Test YAML read/write utilities."""

    def test_leer_yaml_valid_file(self, tmp_path):
        """Test reading a valid YAML file."""
        yaml_file = tmp_path / "config.yaml"
        yaml_file.write_text("name: test\nversion: v1.0")

        result = leer_yaml(str(yaml_file))
        assert result["name"] == "test"
        assert result["version"] == "v1.0"

    def test_leer_yaml_nonexistent_file(self, tmp_path):
        """Test reading a non-existent YAML file returns empty dict."""
        result = leer_yaml(str(tmp_path / "nonexistent.yaml"))
        assert result == {}

    def test_leer_yaml_nonexistent_file_verbose(self, tmp_path):
        """Test reading non-existent file with verbose mode."""
        result = leer_yaml(str(tmp_path / "nonexistent.yaml"), verbose=True)
        assert result == {}

    def test_escribir_yaml(self, tmp_path):
        """Test writing a YAML file."""
        yaml_file = tmp_path / "output.yaml"
        data = {"key": "value", "number": 42}
        escribir_yaml(str(yaml_file), data)
        assert yaml_file.exists()

        result = leer_yaml(str(yaml_file))
        assert result["key"] == "value"
        assert result["number"] == 42

    def test_escribir_yaml_verbose(self, tmp_path):
        """Test writing YAML with verbose mode."""
        yaml_file = tmp_path / "output_verbose.yaml"
        data = {"test": True}
        escribir_yaml(str(yaml_file), data, verbose=True)
        assert yaml_file.exists()

    def test_yaml_with_nested_data(self, tmp_path):
        """Test reading YAML with nested data."""
        yaml_file = tmp_path / "nested.yaml"
        yaml_file.write_text(
            """
outer:
  inner:
    key: value
  list:
    - item1
    - item2
"""
        )

        result = leer_yaml(str(yaml_file))
        assert result["outer"]["inner"]["key"] == "value"
        assert result["outer"]["list"][0] == "item1"


class TestYamlErrorHandling:
    """Test YAML error handling."""

    def test_leer_yaml_invalid_yaml_silent(self, tmp_path):
        """Test reading invalid YAML returns empty dict silently."""
        yaml_file = tmp_path / "invalid.yaml"
        yaml_file.write_text("invalid: yaml: content:")

        result = leer_yaml(str(yaml_file))
        assert result == {}

    def test_leer_yaml_invalid_yaml_verbose(self, tmp_path):
        """Test reading invalid YAML with verbose mode."""
        yaml_file = tmp_path / "invalid.yaml"
        yaml_file.write_text("invalid: yaml: content:")

        result = leer_yaml(str(yaml_file), verbose=True)
        assert result == {}

    def test_escribir_yaml_ioerror_silent(self, tmp_path):
        """Test writing to invalid path returns None silently."""
        result = escribir_yaml("/invalid/path/to/file.yaml", {"test": True})
        assert result is None

    def test_escribir_yaml_ioerror_verbose(self, tmp_path):
        """Test writing to invalid path with verbose mode."""
        result = escribir_yaml(
            "/invalid/path/to/file.yaml", {"test": True}, verbose=True
        )
        assert result is None
