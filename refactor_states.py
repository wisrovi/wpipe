import os
import re

states_dir = "/home/wisrovi/Documentos/w_libraries/wpipe/wpipe/examples/00_honey_pot/03_yield/states/"

translation_map = {
    "cambiar_aceite": "change_oil",
    "conducir": "drive",
    "desinflar_neumaticos": "deflate_tires",
    "hechar_gasolina": "refuel",
    "inflar_neumaticos": "inflate_tires",
    "A_abrir_coche": "open_car",
    "B_inflar_neumaticos": "inflate_tires_prep",
    "C_limpiar_parabrisas": "clean_windshield",
    "D_arrancar_motor": "start_motor",
    "fase_preparacion": "preparation_phase",
    "print_gasolina": "print_fuel_level",
    "Print_info": "CarInfoPrinter",
    "nested": "nested_step",
}

def refactor_states():
    for filename in os.listdir(states_dir):
        if not filename.endswith(".py"):
            continue
        
        file_path = os.path.join(states_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Remove Spanish aliases at the end of the file
        # Pattern: alias = original  # comment
        for alias, original in translation_map.items():
            content = re.sub(fr"{alias}\s*=\s*{original}.*$", "", content, flags=re.MULTILINE)
        
        # Clean up __init__.py specially
        if filename == "__init__.py":
            # Remove Spanish names from __all__
            all_match = re.search(r"__all__\s*=\s*\[(.*?)\]", content, re.DOTALL)
            if all_match:
                items = all_match.group(1).split(",")
                new_items = []
                for item in items:
                    item_stripped = item.strip().strip("'").strip('"')
                    if item_stripped and item_stripped not in translation_map:
                        new_items.append(item.strip())
                new_all = "__all__ = [\n    " + ",\n    ".join(new_items) + ",\n]"
                content = content[:all_match.start()] + new_all + content[all_match.end():]
            
            # Remove Spanish imports
            lines = content.splitlines()
            new_lines = []
            for line in lines:
                if any(f"from .{m}" in line for m in translation_map.values()) or "from ." in line:
                    # Simplify import lines to only include English names
                    parts = line.split("import")
                    if len(parts) == 2:
                        prefix = parts[0]
                        imported_names = parts[1].split(",")
                        new_names = [n.strip() for n in imported_names if n.strip() not in translation_map]
                        if new_names:
                            new_lines.append(f"{prefix}import {', '.join(new_names)}")
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            content = "\n".join(new_lines)

        # Fix __init__.py more carefully
        if filename == "__init__.py":
            content = """\"\"\"States package for the car pipeline.

This package contains all the steps (states) used in the car pipeline examples.
All steps are exported in English only.
\"\"\"

from .cambiar_aceite import change_oil
from .conducir import drive
from .desinflar_neumaticos import deflate_tires
from .hechar_gasolina import refuel
from .inflar_neumaticos import inflate_tires
from .preparacion import (
    open_car,
    inflate_tires_prep,
    clean_windshield,
    start_motor,
    preparation_phase,
)
from .print_gasolina import print_fuel_level
from .print_info import (
    CarInfoPrinter,
    nested_step,
)

__all__ = [
    "change_oil",
    "drive",
    "deflate_tires",
    "refuel",
    "inflate_tires",
    "open_car",
    "inflate_tires_prep",
    "clean_windshield",
    "start_motor",
    "preparation_phase",
    "print_fuel_level",
    "CarInfoPrinter",
    "nested_step",
]
"""
        
        # Ensure Pylint 10/10 by removing trailing whitespace and extra newlines
        content = content.strip() + "\n"
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    print("Refactored states directory.")

if __name__ == "__main__":
    refactor_states()
