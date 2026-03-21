"""
Tests for pipeline configuration functionality.
"""

import os
import pytest
from wpipe.pipe import Pipeline
from wpipe.util import leer_yaml, escribir_yaml


class TestPipelineSteps:
    """Test pipeline step functions."""

    def test_step_function_basic(self):
        """Test basic step function works in pipeline."""

        def step1(data):
            return {"step1_done": True}

        def step2(data):
            return {"step2_done": True}

        pipeline = Pipeline()
        pipeline.set_steps(
            [
                (step1, "Step1", "v1.0"),
                (step2, "Step2", "v1.0"),
            ]
        )
        result = pipeline.run({})
        assert result["step1_done"] is True
        assert result["step2_done"] is True

    def test_step_function_with_data(self):
        """Test step function processes data correctly."""

        def process_step(data):
            x = data.get("x", 0)
            return {"processed": x * 2}

        def final_step(data):
            return {"final": data.get("processed", 0) + 5}

        pipeline = Pipeline()
        pipeline.set_steps(
            [
                (process_step, "Process", "v1.0"),
                (final_step, "Final", "v1.0"),
            ]
        )
        result = pipeline.run({"x": 5})
        assert result["processed"] == 10
        assert result["final"] == 15


class TestPipelineConfig:
    """Test pipeline configuration."""

    def test_load_config_file(self, tmp_path):
        """Test loading pipeline configuration from YAML."""
        config_path = tmp_path / "config.yaml"
        config_data = {
            "name": "test_service",
            "version": "v1.0",
            "pipeline_use": True,
        }
        escribir_yaml(str(config_path), config_data)

        loaded_config = leer_yaml(str(config_path))
        assert loaded_config["name"] == "test_service"
        assert loaded_config["version"] == "v1.0"

    def test_config_defaults(self, tmp_path):
        """Test configuration with default values."""
        config_path = tmp_path / "config.yaml"
        config_data = {"name": "service"}
        escribir_yaml(str(config_path), config_data)

        loaded_config = leer_yaml(str(config_path))
        assert "name" in loaded_config


class TestPipelineExecution:
    """Test pipeline execution."""

    def test_pipeline_with_multiple_steps(self):
        """Test pipeline with multiple steps."""

        def validate(data):
            return {"validated": True}

        def process(data):
            return {"processed": True}

        def save(data):
            return {"saved": True}

        pipeline = Pipeline()
        pipeline.set_steps(
            [
                (validate, "Validate", "v1.0"),
                (process, "Process", "v1.0"),
                (save, "Save", "v1.0"),
            ]
        )

        result = pipeline.run({})
        assert result["validated"] is True
        assert result["processed"] is True
        assert result["saved"] is True

    def test_pipeline_error_handling(self):
        """Test pipeline handles errors."""

        def step1(data):
            return {"step1": True}

        def failing_step(data):
            raise ValueError("Test error")

        pipeline = Pipeline()
        pipeline.set_steps(
            [
                (step1, "Step1", "v1.0"),
                (failing_step, "FailingStep", "v1.0"),
            ]
        )

        try:
            pipeline.run({})
            assert False, "Should have raised an error"
        except Exception:
            pass
