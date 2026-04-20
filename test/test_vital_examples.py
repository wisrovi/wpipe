import pytest
import os
import subprocess

# Lista de ejemplos que dan máxima cobertura core
EXAMPLES = [
    "examples/01_basic_pipeline/01_basic_pipeline.py",
    "examples/01_basic_pipeline/02_error_handling.py",
    "examples/00_honey_pot/01 basic/example.py"
]

@pytest.mark.parametrize("path", EXAMPLES)
def test_example_execution(path):
    if not os.path.exists(path): pytest.skip()
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    res = subprocess.run(["python3", path], env=env, capture_output=True)
    assert res.returncode == 0
