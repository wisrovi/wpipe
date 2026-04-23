from typing import Any

"""
DEMO LEVEL 85: Export a YAML
-------------------------------
Adds: Exportar configuración a YAML.
Continues: L84.

DIAGRAM:
Pipeline --> YAML config
"""

import os
from pathlib import Path

from wpipe import Pipeline, step


@step(name="start")
def start(data: dict) -> None:
    """Start step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("🔑 Motor iniciado")
    return {"motor": "on"}


if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)

    pipe = Pipeline(
        pipeline_name="viaje_l85_exportyaml",
        verbose=True,
        tracking_db="output/export_yaml.db",
    )
    pipe.set_steps([start])
    pipe.run({})

    print("\n📤 Verificando YAML...")
    yaml_path = Path("pipeline_configs/Viaje_L85_ExportYAML.yaml")
    if yaml_path.exists():

        """Start step.

        Args:

            data: Input data for the step.

        Returns:

            dict: Result of the step.

        """
        content = yaml_path.read_text()
        print(f"✅ YAML guardado en {yaml_path}")
        print(f"   Tamaño: {len(content)} bytes")
    else:
        print("⚠️ YAML no encontrado")
