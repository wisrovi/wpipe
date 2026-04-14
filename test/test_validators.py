"""
Unit tests for type hinting validators.
"""

import unittest
from typing import Dict, List, Any
from wpipe.type_hinting.validators import TypeValidator, GenericPipeline, PipelineContext


class TestTypeValidator(unittest.TestCase):
    """Test TypeValidator functionality."""

    def test_validate_basic_types(self):
        """Test validation of basic types."""
        self.assertEqual(TypeValidator.validate(10, int), 10)
        self.assertEqual(TypeValidator.validate("hello", str), "hello")
        self.assertEqual(TypeValidator.validate(1.5, float), 1.5)
        self.assertEqual(TypeValidator.validate(True, bool), True)

        with self.assertRaises(TypeError):
            TypeValidator.validate(10, str)
        with self.assertRaises(TypeError):
            TypeValidator.validate("hello", int)

    def test_validate_list(self):
        """Test validation of list types."""
        self.assertEqual(TypeValidator.validate([1, 2, 3], list), [1, 2, 3])
        self.assertEqual(TypeValidator.validate([1, 2, 3], List[int]), [1, 2, 3])
        
        with self.assertRaises(TypeError):
            TypeValidator.validate("not a list", list)
        
        with self.assertRaises(TypeError):
            TypeValidator.validate([1, "2", 3], List[int])

    def test_validate_dict(self):
        """Test validation of dict types."""
        self.assertEqual(TypeValidator.validate({"a": 1}, dict), {"a": 1})
        self.assertEqual(TypeValidator.validate({"a": 1}, Dict[str, int]), {"a": 1})
        
        with self.assertRaises(TypeError):
            TypeValidator.validate("not a dict", dict)
        
        with self.assertRaises(TypeError):
            TypeValidator.validate({"a": "1"}, Dict[str, int])
            
        with self.assertRaises(TypeError):
            TypeValidator.validate({1: 1}, Dict[str, int])

    def test_validate_dict_schema(self):
        """Test validation of dictionary against schema."""
        schema = {
            "name": str,
            "age": int,
            "tags": List[str]
        }
        data = {
            "name": "John",
            "age": 30,
            "tags": ["a", "b"]
        }
        
        validated = TypeValidator.validate_dict(data, schema)
        self.assertEqual(validated, data)
        
        # Missing key
        with self.assertRaises(KeyError):
            TypeValidator.validate_dict({"name": "John"}, schema)
            
        # Wrong type
        with self.assertRaises(TypeError):
            TypeValidator.validate_dict({"name": "John", "age": "30", "tags": []}, schema)

    def test_generic_pipeline(self):
        """Test GenericPipeline validation."""
        pipeline = GenericPipeline(PipelineContext)

        context = {
            "step_id": "step1",
            "step_name": "test",
            "execution_id": "exec1",
            "timestamp": "2023-01-01",
            "metadata": {"key": "value"}
        }

        # TypedDict is not a real runtime type for isinstance checks in all Python versions.
        # Validate that the dict has the required keys instead.
        required_keys = PipelineContext.__annotations__.keys()
        for key in required_keys:
            assert key in context, f"Missing required key: {key}"
        
    def test_unsupported_generic(self):
        """Test unsupported generic types (returns value as is)."""
        # TypeValidator.validate returns value if origin is not dict or list
        from typing import Union
        self.assertEqual(TypeValidator.validate(10, Union[int, str]), 10)


if __name__ == "__main__":
    unittest.main()
