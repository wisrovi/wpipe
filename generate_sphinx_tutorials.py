"""
Module to generate Sphinx documentation for learning tutorials.

This script iterates through example files, executes them to capture their output,
and creates corresponding ReStructuredText (RST) files for the documentation.
"""

import os
import re
import subprocess
from typing import List, Optional

def sort_key(filename: str) -> int:
    """
    Extract the numeric level from a filename following the pattern 'demo_levelX.py'.

    Args:
        filename: The name of the file to extract the level from.

    Returns:
        The extracted level number, or 0 if no match is found.
    """
    match: Optional[re.Match] = re.search(r'demo_level(\d+)\.py', filename)
    if match:
        return int(match.group(1))
    return 0

def generate() -> None:
    """
    Generate RST documentation files from example scripts in the specified directory.
    """
    examples_dir: str = 'examples/00_honey_pot/03_yield'
    output_dir: str = 'docs/source/tutorials/tour'
    os.makedirs(output_dir, exist_ok=True)

    files: List[str] = [
        file for file in os.listdir(examples_dir)
        if file.startswith('demo_level') and file.endswith('.py')
    ]
    files.sort(key=sort_key)

    index_content: str = (
        "Learning Tour (130 Levels)\n"
        "===========================\n\n"
        "Welcome to the WPipe Learning Tour. This guided tour will take you from "
        "the most basic concepts to the most complex orchestrations through "
        "130 practical levels.\n\n"
        ".. toctree::\n"
        "   :maxdepth: 1\n"
        "   :numbered:\n\n"
    )

    for filename in files:
        level_num: int = sort_key(filename)
        rst_filename: str = f'level{level_num}.rst'

        print(f"Executing {filename} to capture output...")
        try:
            result: subprocess.CompletedProcess = subprocess.run(
                ['python3', filename],
                cwd=examples_dir,
                capture_output=True,
                text=True,
                timeout=30,
                check=False
            )
            output: str = result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            output = "Error: Timeout when executing the example."
        except subprocess.SubprocessError as err:
            output = f"Subprocess error: {str(err)}"
        except OSError as err:
            output = f"OS error: {str(err)}"

        # Create individual rst for each level
        with open(os.path.join(output_dir, rst_filename), 'w', encoding='utf-8') as file:
            title: str = f"Level {level_num}: {filename}"
            file.write(f"{title}\n" + "=" * len(title) + "\n\n")
            file.write(f"This is level {level_num} of the learning tour.\n\n")

            file.write("Source Code\n-----------\n\n")
            file.write(f".. literalinclude:: ../../../../{examples_dir}/{filename}\n")
            file.write("   :language: python\n")
            file.write("   :linenos:\n\n")

            file.write("Execution Result\n----------------\n\n")
            file.write(".. code-block:: text\n\n")
            for line in output.splitlines():
                file.write(f"   {line}\n")
            file.write("\n")

        index_content += f"   {rst_filename[:-4]}\n"

    with open(os.path.join(output_dir, 'index.rst'), 'w', encoding='utf-8') as file:
        file.write(index_content)

    print(f"Generated {len(files)} levels with results in {output_dir}")

if __name__ == "__main__":
    generate()
