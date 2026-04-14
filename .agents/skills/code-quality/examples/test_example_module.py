"""
Unit tests for example_module.py demonstrating best practices.
Includes fixtures, type hints, and comprehensive coverage.
"""

from unittest.mock import MagicMock, patch
import pytest

from example_module import (
    DataProcessor,
    UserConfig,
    ValidationError,
    ProcessingError,
)


@pytest.fixture
def mock_config() -> UserConfig:
    """Create a mock configuration for testing."""
    return UserConfig(
        username="testuser",
        password="hashed_password",
        email="test@example.com",
        is_active=True,
    )


@pytest.fixture
def processor(mock_config: UserConfig) -> DataProcessor:
    """Create a DataProcessor instance for testing."""
    return DataProcessor(config=mock_config, max_retries=3)


class TestUserConfig:
    """Test suite for UserConfig dataclass."""

    def test_create_config_with_defaults(self) -> None:
        """Test creating config with default values."""
        config = UserConfig(
            username="user",
            password="pass",
            email="user@example.com",
        )
        assert config.username == "user"
        assert config.is_active is True

    def test_create_config_with_custom_values(self) -> None:
        """Test creating config with custom values."""
        config = UserConfig(
            username="admin",
            password="secret",
            email="admin@example.com",
            is_active=False,
        )
        assert config.is_active is False


class TestDataProcessorInit:
    """Test suite for DataProcessor initialization."""

    def test_init_with_valid_config(self, mock_config: UserConfig) -> None:
        """Test initialization with valid configuration."""
        processor = DataProcessor(mock_config)
        assert processor.config == mock_config
        assert processor.max_retries == 3

    def test_init_with_custom_retries(self, mock_config: UserConfig) -> None:
        """Test initialization with custom retry count."""
        processor = DataProcessor(mock_config, max_retries=5)
        assert processor.max_retries == 5

    def test_init_with_invalid_retries(self, mock_config: UserConfig) -> None:
        """Test initialization fails with invalid retry count."""
        with pytest.raises(ValueError, match="max_retries must be at least 1"):
            DataProcessor(mock_config, max_retries=0)


class TestDataProcessorProcess:
    """Test suite for DataProcessor.process method."""

    def test_process_valid_data(self, processor: DataProcessor) -> None:
        """Test processing valid data."""
        input_data = {"key": "value", "number": 42}
        result = processor.process(input_data)

        assert result["processed"] is True
        assert result["original"] == input_data
        assert result["processor"] == "testuser"

    def test_process_increments_count(self, processor: DataProcessor) -> None:
        """Test that processing increments the counter."""
        processor.process({"data": "first"})
        processor.process({"data": "second"})
        assert processor._processed_count == 2

    def test_process_empty_dict_fails(self, processor: DataProcessor) -> None:
        """Test that processing empty dict raises ValidationError."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            processor.process({})

    def test_process_non_dict_fails(self, processor: DataProcessor) -> None:
        """Test that processing non-dict raises ValidationError."""
        with pytest.raises(ValidationError, match="must be a dictionary"):
            processor.process("not a dict")  # type: ignore


class TestDataProcessorValidation:
    """Test suite for DataProcessor input validation."""

    def test_validate_none_raises_error(self, processor: DataProcessor) -> None:
        """Test that None input raises ValidationError."""
        with pytest.raises(ValidationError):
            processor._validate_input(None)  # type: ignore

    def test_validate_list_raises_error(self, processor: DataProcessor) -> None:
        """Test that list input raises ValidationError."""
        with pytest.raises(ValidationError):
            processor._validate_input([1, 2, 3])  # type: ignore


class TestDataProcessorTransform:
    """Test suite for DataProcessor data transformation."""

    def test_transform_preserves_original(self, processor: DataProcessor) -> None:
        """Test that transformation preserves original data."""
        original = {"test": "data"}
        result = processor._transform_data(original)
        assert result["original"] == original

    def test_transform_adds_metadata(self, processor: DataProcessor) -> None:
        """Test that transformation adds processing metadata."""
        result = processor._transform_data({})
        assert "processed" in result
        assert "processor" in result
        assert "count" in result


class TestDataProcessorReset:
    """Test suite for DataProcessor.reset_count method."""

    def test_reset_count_zeros_counter(self, processor: DataProcessor) -> None:
        """Test that reset_count sets counter to zero."""
        processor.process({"data": "item"})
        processor.reset_count()
        assert processor._processed_count == 0
