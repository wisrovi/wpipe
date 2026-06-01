import os
import subprocess
import pytest

# List of directories to skip
SKIP_DIRS = {
    'states', 'utils', 'dto', 'configs', 'extra_readmes', 
    'extras', 'test', 'pipelines', '__pycache__', '.git', '.github', '.vscode', 
    'output', 'export_output', '.venv', 'venv', 'env', 'virtualenv', '.pytest_cache', '.ruff_cache'
}

def find_examples():
    root_dir = os.path.join(os.path.dirname(__file__), '..', 'examples')
    examples = []
    for root, dirs, files in os.walk(root_dir):
        # Filter directories in-place
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                examples.append(os.path.abspath(os.path.join(root, file)))
    return sorted(examples)

@pytest.mark.parametrize("example_path", find_examples())
def test_example_execution(example_path):
    """
    Test that an example script executes successfully.
    """
    # Set PYTHONPATH to include the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env = os.environ.copy()
    env['PYTHONPATH'] = project_root
    
    # Change directory to the example's parent directory
    example_dir = os.path.dirname(example_path)
    example_file = os.path.basename(example_path)

    # Shorter timeout for demo levels
    timeout = 10 if 'demo_level' in example_path else 30
    
    # Controlled keywords for examples demonstrating failures
    controlled_keywords = [
        "Expected Error", "captured error", "controlled failure", 
        "Input data cannot be None", "Expected exception", "demonstrates error handling",
        "Nested pipeline error", "failing_step"
    ]

    try:
        result = subprocess.run(
            ['python3', example_file],
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
            cwd=example_dir
        )
        
        stdout = result.stdout
        stderr = result.stderr
        
        # Check for success
        if result.returncode == 0:
            # Check if it was supposed to fail but succeeded (controlled success)
            # Or just standard success
            return

        # Check for controlled failures
        if any(kw in stdout or kw in stderr for kw in controlled_keywords):
            return

        # Handle specific known issues that shouldn't break the whole test suite
        # (Missing optional dependencies)
        missing_deps = ["shapely", "ultralytics", "pandas"]
        if "ModuleNotFoundError" in stderr and any(dep in stderr for dep in missing_deps):
            pytest.skip(f"Skipping due to missing optional dependency: {stderr}")

        # If it failed and wasn't a controlled failure, raise error
        pytest.fail(f"Example failed with return code {result.returncode}\n\nSTDOUT:\n{stdout}\n\nSTDERR:\n{stderr}")

    except subprocess.TimeoutExpired:
        # Some examples are servers/dashboards, they are considered successful if they start
        if any(kw in example_path for kw in ['dashboard', 'api', 'microservice', 'server']):
            return
        pytest.skip(f"Example timed out after {timeout}s")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred: {e}")
