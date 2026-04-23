import os
import re
from typing import Dict

base_dir = "/home/wisrovi/Documentos/w_libraries/wpipe/wpipe/examples/00_honey_pot/03_yield/"

translation_map = {
    "inflar_neumaticos": "inflate_tires",
    "conducir": "drive",
    "cambiar_aceite": "change_oil",
    "hechar_gasolina": "refuel",
    "A_abrir_coche": "open_car",
    "Print_info": "CarInfoPrinter",
    "nested": "nested_step",
    "fase_preparacion": "preparation_phase",
    "viaje": "trip",
    "coche": "car",
    "medir": "measure",
    "iniciar": "start",
    "procesar": "process",
    "medir_eficiencia": "measure_efficiency",
    "navegacion_activa": "active_navigation",
    "revisar_luces": "check_lights",
    "pinchazo_aleatorio": "random_flat_tire",
    "notificar_telegram_error": "notify_telegram_error",
    "combustible_bajo": "low_fuel",
    "inicio_viaje": "trip_start",
    "tarea": "task",
    "gasolina": "fuel",
    "aceite": "oil",
    "neumaticos": "tires",
    "luces": "lights",
    "tramo": "stretch",
    "Autopista": "Highway",
    "medir_distancia": "measure_distance",
    "estimar_tiempo": "estimate_time",
    "calcular_ruta": "calculate_route",
    "verificar_estado": "verify_status",
    "finalizar": "finish",
    "exito": "success",
    "falla": "failure",
    "alerta": "alert",
    "historial": "history",
    "registro": "record",
    "eficiencia": "efficiency",
    "consumo": "consumption",
    "velocidad": "speed",
}

def translate_content(content: str) -> str:
    # 1. First, translate names in the content to avoid issues later
    for es, en in translation_map.items():
        content = re.sub(fr"\b{es}\b", en, content)

    # 2. Add typing and Google docstrings to local functions
    def add_docs_and_typing(match):
        indent = match.group(1)
        decorator = match.group(2)
        func_name = match.group(3)
        args = match.group(4)
        
        # Add typing if missing
        if ":" not in args and args:
            new_args = []
            for arg in args.split(","):
                arg = arg.strip()
                if arg == "data":
                    new_args.append("data: dict")
                elif arg == "context":
                    new_args.append("context: Any")
                elif arg:
                    new_args.append(f"{arg}: Any")
            args = ", ".join(new_args)
        
        ret_type = " -> dict"
        if "return" not in match.group(0) and "yield" not in match.group(0):
            ret_type = " -> None"
            
        docstring = f'\n{indent}    """{func_name.replace("_", " ").capitalize()} step.\n\n{indent}    Args:\n{indent}        {args.split(":")[0] if ":" in args else args}: Input data for the step.\n\n{indent}    Returns:\n{indent}        dict: Result of the step.\n{indent}    """'
        
        return f"{indent}{decorator}\ndef {func_name}({args}){ret_type}:{docstring}"

    # Target local functions with @step decorator. Group 2 captures the decorator.
    content = re.sub(r"^(\s*)(@step\(.*?\))\s*\n\s*def (\w+)\((.*?)\):", add_docs_and_typing, content, flags=re.MULTILINE | re.DOTALL)

    # 3. Translate comments and strings
    content = content.replace("NUEVO EN L", "NEW IN L")
    content = content.replace("Añade:", "Adds:")
    content = content.replace("Acumula:", "Accumulates:")
    content = content.replace("DIAGRAMA:", "DIAGRAM:")
    content = content.replace("Inicia", "Starts")
    content = content.replace("Finaliza", "Finishes")
    content = content.replace("éxito", "success")
    content = content.replace("CONSEJO:", "TIP:")
    content = content.replace("Abrir terminal", "Open terminal")
    content = content.replace("Abre una terminal", "Open a terminal")
    content = content.replace("Gráficos", "Charts")
    content = content.replace("Tiempos", "Times")
    content = content.replace("Alertas", "Alerts")
    content = content.replace("Guiando al destino", "Guiding to destination")
    content = content.replace("Datos grabándose", "Data being recorded")
    content = content.replace("Añade:", "Adds:")
    
    return content

def refactor_demos():
    files = [f for f in os.listdir(base_dir) if f.startswith("demo_level") and f.endswith(".py")]
    
    def extract_number(f):
        match = re.search(r"level(\d+)", f)
        return int(match.group(1)) if match else 0
    files.sort(key=extract_number)

    for filename in files:
        level_num = extract_number(filename)
        if level_num < 26:
            continue
            
        file_path = os.path.join(base_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content = translate_content(content)
        
        # Ensure typing imports if Any is used
        if "Any" in new_content and "from typing import" not in new_content:
            new_content = "from typing import Any, Dict\n" + new_content

        new_content = new_content.strip() + "\n"
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            
    print(f"Refactored {len(files)} demo files.")

if __name__ == "__main__":
    refactor_demos()
