import os
import sys
import pytest
import shutil
import tempfile
from importlib.util import spec_from_file_location, module_from_spec
from unittest.mock import patch

def run_python_file(file_path):
    """Executes a python file as if it was run as __main__."""
    file_path = os.path.abspath(file_path)
    directory = os.path.dirname(file_path)
    
    # Save original state
    orig_cwd = os.getcwd()
    orig_sys_path = list(sys.path)
    
    # Create a temporary directory for logs and databases
    tmp_dir = tempfile.mkdtemp()
    os.chdir(tmp_dir)
    
    # Add example directory to sys.path
    if directory not in sys.path:
        sys.path.insert(0, directory)
    
    try:
        # Read the file content
        with open(file_path, 'r') as f:
            code = f.read()
        
        # Execute the code in a new namespace
        namespace = {"__name__": "__main__", "__file__": file_path}
        exec(code, namespace)
        
        # If there's a main() function, call it if it wasn't called by exec
        if "main" in namespace and callable(namespace["main"]):
            # Check if it was already called by the __name__ == "__main__" block
            # In many cases exec will have already run it.
            pass
            
    finally:
        # Restore state
        os.chdir(orig_cwd)
        sys.path = orig_sys_path
        shutil.rmtree(tmp_dir)

@pytest.mark.parametrize("example_rel_path", [
    "examples/00_honey_pot/01 basic/example.py",
    "examples/01_basic_pipeline/01_simple_function/example.py",
    "examples/17_parallel/01_basic/parallel_basic.py",
    "examples/18_composition/01_nested/nested_pipeline.py",
])
def test_example_execution(example_rel_path):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    file_path = os.path.join(project_root, example_rel_path)
    if os.path.exists(file_path):
        run_python_file(file_path)
    else:
        pytest.skip(f"Example not found: {example_rel_path}")

def test_example_checkpoint_execution():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    file_path = os.path.join(project_root, "examples/00_honey_pot/01 basic/example_checkpoint.py")
    
    if not os.path.exists(file_path):
        pytest.skip("example_checkpoint.py not found")
        
    directory = os.path.dirname(file_path)
    orig_cwd = os.getcwd()
    orig_sys_path = list(sys.path)
    tmp_dir = tempfile.mkdtemp()
    os.chdir(tmp_dir)
    
    if directory not in sys.path:
        sys.path.insert(0, directory)
        
    try:
        # Run it twice as the example intended
        with open(file_path, 'r') as f:
            code = f.read()
            
        # First run might fail by design in the example (simulating crash)
        namespace1 = {"__name__": "__main__", "__file__": file_path}
        try:
            exec(code, namespace1)
        except Exception:
            pass
            
        # Second run should resume
        namespace2 = {"__name__": "__main__", "__file__": file_path}
        exec(code, namespace2)
            
    finally:
        os.chdir(orig_cwd)
        sys.path = orig_sys_path
        shutil.rmtree(tmp_dir)
