"""
Unit tests for transform utilities.
"""

import unittest
from dataclasses import dataclass
from types import SimpleNamespace
from pydantic import BaseModel
from wpipe.util.transform import dict_to_sns, object_to_dict, to_obj, auto_dict_input, state


class TestTransform(unittest.TestCase):
    """Test transform functionality."""

    def test_dict_to_sns(self):
        """Test recursive conversion from dict to SimpleNamespace."""
        data = {"a": 1, "b": {"c": 2}, "d": [1, {"e": 3}]}
        sns = dict_to_sns(data)
        
        self.assertIsInstance(sns, SimpleNamespace)
        self.assertEqual(sns.a, 1)
        self.assertIsInstance(sns.b, SimpleNamespace)
        self.assertEqual(sns.b.c, 2)
        self.assertIsInstance(sns.d, list)
        self.assertEqual(sns.d[0], 1)
        self.assertIsInstance(sns.d[1], SimpleNamespace)
        self.assertEqual(sns.d[1].e, 3)

    def test_object_to_dict(self):
        """Test recursive conversion from object to dict."""
        
        @dataclass
        class MyDataclass:
            x: int
            y: str

        class MyPydantic(BaseModel):
            a: int
            b: str

        class MyClass:
            def __init__(self, val):
                self.val = val

        # Test dataclass
        dc = MyDataclass(1, "test")
        self.assertEqual(object_to_dict(dc), {"x": 1, "y": "test"})

        # Test Pydantic
        pd = MyPydantic(a=10, b="pydantic")
        self.assertEqual(object_to_dict(pd), {"a": 10, "b": "pydantic"})

        # Test Custom class
        obj = MyClass(42)
        self.assertEqual(object_to_dict(obj), {"val": 42})

        # Test dict and list
        self.assertEqual(object_to_dict({"a": 1}), {"a": 1})
        self.assertEqual(object_to_dict([1, 2]), [1, 2])
        self.assertEqual(object_to_dict(10), 10)

    def test_to_obj_decorator(self):
        """Test to_obj decorator."""
        
        @to_obj
        def my_func(data):
            return data.name, data.value

        result = my_func({"name": "test", "value": 123})
        self.assertEqual(result, ("test", 123))

    def test_auto_dict_input_decorator(self):
        """Test auto_dict_input decorator."""
        
        @dataclass
        class MyDC:
            name: str

        @auto_dict_input
        def my_func(data):
            return data["name"]

        result = my_func(MyDC(name="hello"))
        self.assertEqual(result, "hello")

    def test_state_decorator(self):
        """Test state decorator."""
        
        @state(name="MyStep", version="v2.0")
        def my_step(data):
            return data * 2

        self.assertEqual(my_step.NAME, "MyStep")
        self.assertEqual(my_step.VERSION, "v2.0")
        self.assertEqual(my_step(10), 20)
        self.assertIn("<State: MyStep v2.0>", repr(my_step))


if __name__ == "__main__":
    unittest.main()
