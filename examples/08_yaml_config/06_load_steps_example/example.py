"""
06 YAML - Loading Pipeline Steps from YAML

Shows loading pipeline step definitions from a YAML file.
"""

import os
import tempfile
from wpipe.util import leer_yaml, escribir_yaml
from wpipe import Pipeline


def main():
    steps_config = {
        "steps": [
            {"name": "Step 1", "function": "step1", "version": "v1.0"},
            {"name": "Step 2", "function": "step2", "version": "v1.0"},
        ]
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        escribir_yaml(f.name, steps_config)
        temp_path = f.name

    config = leer_yaml(temp_path)

    def step1(data):
        return {"step1": "done"}

    def step2(data):
        return {"step2": "done"}

    functions = {"step1": step1, "step2": step2}

    pipeline = Pipeline(verbose=True)
    steps = []

    for step_config in config["steps"]:
        func = functions[step_config["function"]]
        steps.append((func, step_config["name"], step_config["version"]))

    pipeline.set_steps(steps)
    result = pipeline.run({})

    print(f"Result: {result}")

    os.unlink(temp_path)


if __name__ == "__main__":
    main()
