import os
import re
from pathlib import Path

BASE_DIR = Path("examples/00_honey_pot/03_yield/")
LEVEL_RANGE = range(11, 131)

MAPPING = {
    r"\bconducir\b": "drive",
    r"\bhechar_gasolina\b": "refuel",
    r"\bcambiar_aceite\b": "change_oil",
    r"\binflar_neumaticos\b": "inflate_tires",
    r"\bdesinflar_neumaticos\b": "deflate_tires",
    r"\bA_abrir_coche\b": "open_car",
    r"\bfase_preparacion\b": "preparation_phase",
    r"\bprint_gasolina\b": "print_fuel_level",
    r"\bPrint_info\b": "CarInfoPrinter",
    r"\bpreparacion\b": "preparation",
    r"\bviaje\b": "trip",
    r"\bcoche\b": "car",
    r"\biniciar\b": "start",
    r"\bprocesar\b": "process",
    r"\bfinalizar\b": "finish",
    r"\bexito\b": "success",
    r"\bfalla\b": "failure",
    r"\balerta\b": "alert",
    r"\bhistorial\b": "history",
    r"\bmedir\b": "measure",
}

IMPORT_MAPPING = {
    "change_oil": "from states.change_oil import change_oil",
    "drive": "from states.drive import drive",
    "deflate_tires": "from states.deflate_tires import deflate_tires",
    "refuel": "from states.refuel import refuel",
    "inflate_tires": "from states.inflate_tires import inflate_tires",
    "open_car": "from states.preparation import open_car",
    "preparation_phase": "from states.preparation import preparation_phase",
    "print_fuel_level": "from states.print_fuel_level import print_fuel_level",
    "CarInfoPrinter": "from states.car_info_printer import CarInfoPrinter",
    "nested_step": "from states.car_info_printer import nested_step",
}

def translate_content(content: str) -> str:
    # Comments translation
    content = content.replace("Añade:", "Adds:")
    content = content.replace("Acumula:", "Accumulates:")
    content = content.replace("DIAGRAMA:", "DIAGRAM:")
    content = content.replace("NUEVO EN L", "NEW IN L")
    content = content.replace("Inicia", "Starts")
    content = content.replace("Finaliza", "Finishes")
    content = content.replace("éxito", "success")
    content = content.replace("CONSEJO:", "TIP:")
    content = content.replace("Ver history", "View history")
    content = content.replace("Pipeline completo", "Complete pipeline")
    content = content.replace("Demo final", "Final demo")
    content = content.replace("integrando todo", "integrating everything")
    content = content.replace("Continúa", "Continues")
    content = content.replace("Startsndo sistema API...", "Starting API system...")
    content = content.replace("Procesando datos...", "Processing data...")
    content = content.replace("Demo completado con success!", "Demo completed with success!")
    content = content.replace("Total en history", "Total in history")
    content = content.replace("Historial de alerts...", "Alerts history...")
    content = content.replace("Corriendo segundo pipeline...", "Running second pipeline...")

    # Name mapping
    for pattern, replacement in MAPPING.items():
        content = re.sub(pattern, replacement, content)

    return content

def refactor_imports(content: str) -> str:
    # Find from states import (...)
    states_import_match = re.search(r"from states import \((.*?)\)", content, re.DOTALL)
    if states_import_match:
        imports_text = states_import_match.group(1)
        imports = [i.strip() for i in imports_text.replace(",", " ").split() if i.strip()]
        new_imports = []
        for imp in imports:
            if imp in IMPORT_MAPPING:
                new_imports.append(IMPORT_MAPPING[imp])
            else:
                # Fallback for unexpected imports
                new_imports.append(f"from states import {imp}")
        
        content = content.replace(states_import_match.group(0), "\n".join(new_imports))
    
    # Simple imports from states import X
    simple_states_import = re.findall(r"from states import (\w+)", content)
    for imp in simple_states_import:
        if imp in IMPORT_MAPPING:
            content = content.replace(f"from states import {imp}", IMPORT_MAPPING[imp])

    return content

def fix_docstrings_and_typing(content: str) -> str:
    # Fix triple-quoted docstrings with too many empty lines (found in L100 and L130)
    def clean_docstring(match):
        indent = match.group(1)
        doc_content = match.group(2)
        lines = [line.strip() for line in doc_content.split("\n") if line.strip()]
        new_lines = []
        if lines:
            new_lines.append(f'{indent}    """{lines[0]}')
            if len(lines) > 1:
                new_lines.append("")
                for line in lines[1:]:
                    if line.startswith("Args:") or line.startswith("Returns:"):
                        new_lines.append(f"{indent}        {line}")
                    elif ":" in line and not line.endswith(":"): # Argument description
                         new_lines.append(f"{indent}            {line}")
                    else:
                         new_lines.append(f"{indent}        {line}")
            new_lines.append(f'{indent}    """')
        return "\n".join(new_lines)

    # This is complex, let's use a simpler approach for @step functions
    def step_refactor(match):
        indent = match.group(1)
        decorator = match.group(2)
        func_name = match.group(3)
        args = match.group(4)
        
        # Determine typing
        typed_args = []
        for arg in args.split(","):
            arg = arg.strip()
            if not arg: continue
            if ":" in arg:
                typed_args.append(arg)
            elif arg == "data":
                typed_args.append("data: dict")
            elif arg == "context" or arg == "ctx":
                typed_args.append(f"{arg}: Any")
            elif arg == "error":
                typed_args.append("error: dict")
            else:
                typed_args.append(f"{arg}: Any")
        
        ret_type = " -> dict"
        if "return" not in match.group(0) and "yield" not in match.group(0):
            ret_type = " -> None"
        elif "return None" in match.group(0):
            ret_type = " -> None"

        new_def = f"{indent}{decorator}\ndef {func_name}({', '.join(typed_args)}){ret_type}:"
        
        # Docstring
        doc_name = func_name.replace("_", " ").capitalize()
        docstring = f'\n{indent}    """{doc_name} step.\n\n{indent}    Args:\n{indent}        {typed_args[0].split(":")[0] if typed_args else "data"}: Input data for the step.\n\n{indent}    Returns:\n{indent}        {"dict" if ret_type == " -> dict" else "None"}: Result of the step.\n{indent}    """'
        
        return new_def + docstring

    # Target local functions with @step decorator
    content = re.sub(r"^(\s*)(@step\(.*?\))\s*\n\s*def (\w+)\((.*?)\):(?:\s*\n\s*\"\"\"(.*?)\"\"\"|)", step_refactor, content, flags=re.MULTILINE | re.DOTALL)

    return content

def final_polish(content: str) -> str:
    # Ensure Any and Dict are imported from typing if used
    if ("Any" in content or "Dict" in content) and "from typing import" not in content:
        imports = []
        if "Any" in content: imports.append("Any")
        if "Dict" in content: imports.append("Dict")
        content = f"from typing import {', '.join(imports)}\n" + content
    
    # Remove redundant empty lines
    content = re.sub(r"\n{3,}", "\n\n", content)
    
    return content.strip() + "\n"

def process_file(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = translate_content(content)
    content = refactor_imports(content)
    content = fix_docstrings_and_typing(content)
    content = final_polish(content)
    
    # Pylint fixes:
    # 1. Pipeline name should be snake_case or follow specific pattern? 
    # Usually PIPELINE_NAME is fine, but maybe it wants trip_l130 instead of Viaje_L130
    def snake_case_pipe(match):
        name = match.group(1)
        name = name.lower().replace(" ", "_")
        return f'pipeline_name="{name}"'
    
    content = re.sub(r'pipeline_name="(.*?)"', snake_case_pipe, content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    for i in LEVEL_RANGE:
        filename = f"demo_level{i}.py"
        file_path = BASE_DIR / filename
        if file_path.exists():
            print(f"Refactoring {filename}...")
            process_file(file_path)
        
        # Check for special files like 54_2, 54_3
        for extra in ["_2", "_3"]:
            extra_file = f"demo_level{i}{extra}.py"
            extra_path = BASE_DIR / extra_file
            if extra_path.exists():
                 print(f"Refactoring {extra_file}...")
                 process_file(extra_path)
