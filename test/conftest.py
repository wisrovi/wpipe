"""
Pytest configuration and shared fixtures for wpipe tests.
"""

import os
import tempfile
import pytest
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_config():
    """Sample API configuration for testing."""
    return {"base_url": "http://localhost:8418", "token": "test_token"}


@pytest.fixture
def sample_pipeline_data():
    """Sample data for pipeline execution."""
    return {"x": 5, "y": "test"}


@pytest.fixture
def sample_steps():
    """Sample pipeline steps definition."""

    def step1(data):
        return {"result1": "step1_completed"}

    def step2(data):
        return {"result2": "step2_completed"}

    class Step3:
        def __call__(self, data):
            return {"result3": "step3_completed"}

    return [
        (step1, "Step1", "v1.0"),
        (step2, "Step2", "v1.0"),
        (Step3(), "Step3", "v1.0"),
    ]


@pytest.fixture
def sample_worker_data():
    """Sample worker registration data."""
    return {"name": "test_worker", "version": "v1.0.0"}


@pytest.fixture
def yaml_config_file(temp_dir):
    """Create a temporary YAML config file."""
    config_path = Path(temp_dir) / "test_config.yaml"
    config_content = """
name: test_microservice
version: v1.0
kafka_server: localhost:9092
pipeline_use: false
sqlite_db_name: test_register.db
"""
    config_path.write_text(config_content)
    return str(config_path)


@pytest.fixture
def db_file(temp_dir):
    """Create a temporary database file path."""
    return str(Path(temp_dir) / "test_register.db")
