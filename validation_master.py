import os
import subprocess
import sys
import time
from pathlib import Path

def run_python_file(file_path, cwd):
    try:
        # We use a timeout to prevent infinite loops in examples
        result = subprocess.run(
            [sys.executable, file_path.name],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return True, ""
        else:
            return False, result.stderr
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT (30s)"
    except Exception as e:
        return False, str(e)

def validate_tour():
    tour_dir = Path("examples/00_honey_pot/03_yield")
    demos = sorted([f for f in tour_dir.glob("demo_level*.py")], key=lambda x: str(x))
    # Custom sort for demo_level1.py, demo_level2.py ... demo_level10.py
    import re
    def natural_sort_key(s):
        return [int(text) if text.isdigit() else text.lower()
                for text in re.split('([0-9]+)', str(s))]
    
    demos.sort(key=natural_sort_key)
    
    results = []
    print(f"Validating Tour ({len(demos)} levels)...")
    for demo in demos:
        # print(f"Running {demo.name}...", end=" ", flush=True)
        success, error = run_python_file(demo, tour_dir)
        results.append((demo.name, success, error))
        # if success:
        #    print("OK")
        # else:
        #    print("FAIL")
    return results

def validate_examples():
    examples_dir = Path("examples")
    # Skip the tour dir as it's handled separately
    ignore_dirs = ["00_honey_pot/03_yield", "__pycache__", ".venv", "env", "configs", "test", "dto", "states", "utils", "app", "pipeline_configs"]
    
    all_examples = []
    for root, dirs, files in os.walk(examples_dir):
        rel_root = os.path.relpath(root, examples_dir)
        if any(rel_root.startswith(ignore) for ignore in ignore_dirs if rel_root != "."):
            continue
        
        # Also ignore internal states/utils folders in sub-examples
        if any(part in ["states", "utils", "dto", "pipeline_configs", "app"] for part in Path(rel_root).parts):
            continue

        for file in files:
            if file.endswith(".py") and (file == "example.py" or file.startswith("demo") or "example" in file):
                all_examples.append(Path(root) / file)
    
    all_examples.sort()
    
    results = []
    print(f"Validating other examples ({len(all_examples)} files)...")
    for example in all_examples:
        # print(f"Running {example}...", end=" ", flush=True)
        success, error = run_python_file(example, example.parent)
        results.append((str(example), success, error))
    return results

if __name__ == "__main__":
    # Ensure wpipe is in PYTHONPATH
    os.environ["PYTHONPATH"] = os.getcwd() + os.pathsep + os.environ.get("PYTHONPATH", "")
    
    tour_results = validate_tour()
    example_results = validate_examples()
    
    all_results = tour_results + example_results
    failed = [r for r in all_results if not r[1]]
    
    print("\n" + "="*50)
    print("VALIDATION REPORT")
    print(f"Total tested: {len(all_results)}")
    print(f"Passed:       {len(all_results) - len(failed)}")
    print(f"Failed:       {len(failed)}")
    print("="*50)
    
    if failed:
        print("\nFAILED FILES:")
        for name, _, err in failed:
            print(f"\n--- {name} ---")
            print(err.strip())
    else:
        print("\nALL EXAMPLES PASSED!")
