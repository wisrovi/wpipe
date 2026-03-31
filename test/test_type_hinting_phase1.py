"""
Tests for Phase 1 type hinting functionality.

Tests TypeValidator, PipelineContext, and GenericPipeline.
"""

import pytest
from typing import TypedDict, Dict, List, Optional
from wpipe import TypeValidator, PipelineContext, GenericPipeline


class TestTypeValidator:
    """Test TypeValidator utility class."""

    def test_validate_int(self):
        """Test validating integer."""
        result = TypeValidator.validate(42, int)
        assert result == 42

    def test_validate_int_fails(self):
        """Test integer validation failure."""
        with pytest.raises(TypeError):
            TypeValidator.validate("not_int", int)

    def test_validate_str(self):
        """Test validating string."""
        result = TypeValidator.validate("hello", str)
        assert result == "hello"

    def test_validate_list(self):
        """Test validating list."""
        result = TypeValidator.validate([1, 2, 3], list)
        assert result == [1, 2, 3]

    def test_validate_dict(self):
        """Test validating dictionary."""
        data = {"key": "value"}
        result = TypeValidator.validate(data, dict)
        assert result == data

    def test_validate_list_with_items(self):
        """Test validating list with item types."""
        result = TypeValidator.validate([1, 2, 3], List[int])
        assert result == [1, 2, 3]

    def test_validate_list_with_wrong_items(self):
        """Test list validation failure with wrong item types."""
        with pytest.raises(TypeError):
            TypeValidator.validate([1, "2", 3], List[int])

    def test_validate_dict_with_types(self):
        """Test validating dict with key/value types."""
        data = {"a": 1, "b": 2}
        result = TypeValidator.validate(data, Dict[str, int])
        assert result == data

    def test_validate_dict_schema(self):
        """Test validating dictionary against schema."""
        schema = {
            "user_id": int,
            "username": str,
            "age": int,
        }
        
        data = {
            "user_id": 123,
            "username": "john",
            "age": 30,
        }
        
        result = TypeValidator.validate_dict(data, schema)
        assert result == data

    def test_validate_dict_schema_wrong_type(self):
        """Test dict schema validation fails on wrong type."""
        schema = {
            "user_id": int,
            "username": str,
        }
        
        data = {
            "user_id": "not_int",  # Wrong type
            "username": "john",
        }
        
        with pytest.raises(TypeError):
            TypeValidator.validate_dict(data, schema)

    def test_validate_dict_schema_missing_key(self):
        """Test dict schema validation fails on missing key."""
        schema = {
            "user_id": int,
            "username": str,
        }
        
        data = {
            "user_id": 123,
            # Missing 'username'
        }
        
        with pytest.raises(KeyError):
            TypeValidator.validate_dict(data, schema)

    def test_validate_dict_extra_keys_ok(self):
        """Test that extra keys in dict are ok."""
        schema = {
            "user_id": int,
        }
        
        data = {
            "user_id": 123,
            "extra_key": "value",
        }
        
        result = TypeValidator.validate_dict(data, schema)
        # Result should only contain validated fields
        assert "user_id" in result


class TestPipelineContext:
    """Test PipelineContext TypedDict."""

    def test_pipeline_context_structure(self):
        """Test PipelineContext has correct fields."""
        context: PipelineContext = {
            "step_id": "step_1",
            "step_name": "my_step",
            "execution_id": "exec_1",
            "timestamp": "2024-03-31T10:00:00",
            "metadata": {"key": "value"},
        }
        
        assert context["step_id"] == "step_1"
        assert context["step_name"] == "my_step"

    def test_custom_context_extends_base(self):
        """Test custom context can extend PipelineContext."""
        class MyContext(PipelineContext):
            user_id: int
            result: str
        
        context: MyContext = {
            "step_id": "step_1",
            "user_id": 123,
            "result": "success",
        }
        
        assert context["step_id"] == "step_1"
        assert context["user_id"] == 123
        assert context["result"] == "success"


class TestGenericPipeline:
    """Test GenericPipeline generic class."""

    def test_generic_pipeline_initialization(self):
        """Test initializing generic pipeline."""
        pipeline = GenericPipeline[Dict](dict)
        assert pipeline is not None

    def test_generic_pipeline_with_type_dict(self):
        """Test generic pipeline with TypedDict."""
        class UserContext(PipelineContext):
            user_id: int
        
        pipeline = GenericPipeline[UserContext](UserContext)
        assert pipeline.context_type == UserContext

    def test_generic_pipeline_validate_context(self):
        """Test validating context in generic pipeline."""
        pipeline = GenericPipeline[Dict[str, int]](Dict[str, int])
        
        data = {"a": 1, "b": 2}
        result = pipeline.validate_context(data)
        assert result == data

    def test_generic_pipeline_validate_context_fails(self):
        """Test generic pipeline validation failure."""
        pipeline = GenericPipeline[Dict[str, int]](Dict[str, int])
        
        data = {"a": "not_int"}
        with pytest.raises(TypeError):
            pipeline.validate_context(data)


class TestTypeHintingIntegration:
    """Integration tests for type hinting."""

    def test_step_input_validation(self):
        """Test validating step input data."""
        schema = {
            "user_id": int,
            "username": str,
            "email": str,
        }
        
        input_data = {
            "user_id": 123,
            "username": "john",
            "email": "john@example.com",
            "extra": "ignored",
        }
        
        validated = TypeValidator.validate_dict(input_data, schema)
        
        assert "user_id" in validated
        assert "username" in validated
        assert "email" in validated

    def test_step_output_validation(self):
        """Test validating step output."""
        class OutputContext(PipelineContext):
            result: str
            status: str
        
        output = {
            "result": "processed",
            "status": "success",
            "step_id": "step_1",
        }
        
        schema = {
            "result": str,
            "status": str,
        }
        
        validated = TypeValidator.validate_dict(output, schema)
        
        assert validated["result"] == "processed"
        assert validated["status"] == "success"

    def test_complex_nested_types(self):
        """Test validating complex nested types."""
        schema = {
            "users": List[Dict[str, int]],
        }
        
        data = {
            "users": [{"id": 1}, {"id": 2}],
        }
        
        # This should work
        result = TypeValidator.validate(data["users"], List[Dict[str, int]])
        assert len(result) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
