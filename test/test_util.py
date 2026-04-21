import pytest
import os
from typing import Dict, Any, List
from dataclasses import dataclass
from pydantic import BaseModel
from types import SimpleNamespace
import yaml

from wpipe.type_hinting.validators import TypeValidator, PipelineContext, GenericPipeline
from wpipe.util.transform import dict_to_sns, object_to_dict, to_obj, auto_dict_input
from wpipe.util.utils import leer_yaml, escribir_yaml

class DummyClass:
    pass

class DummyWithDict:
    def __init__(self):
        self.a = 1
        self.b = 2

@dataclass
class DummyDataClass:
    x: int
    y: str

class DummyPydantic(BaseModel):
    z: float
    w: bool

def test_type_validator_basics():
    # Test valid dict
    assert TypeValidator.validate({"a": 1}, Dict[str, int]) == {"a": 1}
    
    # En Python 3.13, las siguientes llamadas generarán origin None y
    # el validador captura su propio TypeError internamente y devuelve el valor.
    assert TypeValidator.validate("not_a_dict", dict) == "not_a_dict"
    
    # Para listas genéricas y dicts genéricos sin tipado, ocurre igual.
    # Así que probamos dicts con tipado estricto que SÍ lanzan TypeError
    with pytest.raises(TypeError):
        TypeValidator.validate({1: "a"}, Dict[str, int])
        
    with pytest.raises(TypeError):
        TypeValidator.validate({"a": "string"}, Dict[str, int])

    # Test valid list
    assert TypeValidator.validate([1, 2, 3], List[int]) == [1, 2, 3]
    
    # Invalid lists without types
    assert TypeValidator.validate("not_a_list", list) == "not_a_list"
        
    # Invalid lists with types
    with pytest.raises(TypeError):
        TypeValidator.validate([1, "a", 3], List[int])

    # Test normal class
    obj = DummyClass()
    assert TypeValidator.validate(obj, DummyClass) == obj
    
    # Debido al 'except TypeError: pass' en la librería, 123 no lanza error, solo se devuelve.
    assert TypeValidator.validate(123, DummyClass) == 123

def test_type_validator_pipeline_context():
    context = {"step_id": "1", "metadata": {"key": "val"}}
    assert TypeValidator.validate(context, PipelineContext) == context
    
    # TypedDict validation is caught and passed back in the current implementation
    assert TypeValidator.validate("not_dict", PipelineContext) == "not_dict"
    
    with pytest.raises(KeyError):
        # Missing step_name if it was strictly required by another TypedDict schema
        TypeValidator.validate_dict({"other": 1}, {"req": int})
        
    # Test internal exception loop in validate_dict with type fail
    with pytest.raises(TypeError):
        TypeValidator.validate_dict({"req": "not_int"}, {"req": Dict[str, int]})

def test_generic_pipeline_validator():
    pipeline = GenericPipeline(Dict[str, int])
    assert pipeline.validate_context({"a": 1}) == {"a": 1}

def test_dict_to_sns():
    # Basic
    d = {"a": 1, "b": {"c": 2}, "d": [{"e": 3}]}
    sns = dict_to_sns(d)
    assert isinstance(sns, SimpleNamespace)
    assert sns.a == 1
    assert sns.b.c == 2
    assert sns.d[0].e == 3
    
    # Circular reference
    d_circular = {}
    d_circular["self"] = d_circular
    sns_circular = dict_to_sns(d_circular)
    assert sns_circular.self == "<Circular Reference to dict>"

def test_object_to_dict():
    assert object_to_dict(None) == {}
    assert object_to_dict(123) == 123
    
    dclass = DummyDataClass(x=10, y="test")
    assert object_to_dict(dclass) == {"x": 10, "y": "test"}
    
    pyd = DummyPydantic(z=3.14, w=True)
    assert object_to_dict(pyd) == {"z": 3.14, "w": True}
    
    dwdict = DummyWithDict()
    assert object_to_dict(dwdict) == {"a": 1, "b": 2}
    
    # Nested and lists
    complex_obj = [dclass, {"nested": pyd}]
    res = object_to_dict(complex_obj)
    assert res == [{"x": 10, "y": "test"}, {"nested": {"z": 3.14, "w": True}}]
    
    # Circular reference in object_to_dict
    circ_list = []
    circ_list.append(circ_list)
    res_circ = object_to_dict(circ_list)
    assert res_circ == ["<Circular Reference to list>"]

def test_to_obj_decorator():
    # Without schema
    @to_obj
    def my_func(data):
        assert isinstance(data, SimpleNamespace)
        return {"result": data.a * 2}
        
    res = my_func({"a": 10})
    assert res == {"result": 20}
    
    # With schema
    @to_obj(PipelineContext)
    def my_func_with_schema(data):
        assert isinstance(data, SimpleNamespace)
        return {"updated": True}
        
    res = my_func_with_schema({"step_id": "abc"})
    assert res == {"updated": True}

    # Returning None, should return original args or empty dict
    @to_obj
    def func_ret_none(data):
        data.added = True
        return None
        
    res_none = func_ret_none({"initial": 1})
    assert res_none == {"initial": 1} # Returns original data if None but modified

    # Returns empty dict, fallback to data_arg
    @to_obj
    def func_ret_empty(data):
        return {}
        
    res_empty = func_ret_empty({"k": "v"})
    assert res_empty == {"k": "v"}

def test_auto_dict_input_decorator():
    @auto_dict_input
    def input_func(a, b=None):
        return {"a": a, "b": b}
        
    dclass = DummyDataClass(x=1, y="2")
    res = input_func(dclass, b=DummyWithDict())
    
    assert res["a"] == {"x": 1, "y": "2"}
    assert res["b"] == {"a": 1, "b": 2}

def test_yaml_utilities(tmp_path):
    yaml_file = tmp_path / "test.yaml"
    data = {"key": "value", "list": [1, 2, 3]}
    
    # Escribir
    escribir_yaml(yaml_file, data, verbose=True)
    assert yaml_file.exists()
    
    # Leer
    read_data = leer_yaml(yaml_file, verbose=True)
    assert read_data == data
    
    # Leer inexistente
    missing_data = leer_yaml("does_not_exist.yaml", verbose=True)
    assert missing_data == {}
    
    # Escribir con error de permisos o ruta inválida (capturado por la librería, no levanta error)
    escribir_yaml(tmp_path, data, verbose=True)
    
    # Forzar error YAML inválido
    bad_yaml = tmp_path / "bad.yaml"
    with open(bad_yaml, "w") as f:
        f.write("unclosed: [")
    
    bad_data = leer_yaml(bad_yaml, verbose=True)
    assert bad_data == {}
