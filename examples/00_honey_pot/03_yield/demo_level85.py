"""
DEMO LEVEL 85: Export a YAML
-------------------------------
Añade: Exportar configuración a YAML.
Continúa: L84.

DIAGRAMA:
Pipeline --> YAML config
"""

import os

from pathlib import Path

from wpipe import Pipeline, step


@step(name="iniciar")
def iniciar(data):
    print("🔑 Motor iniciado")
    return {"motor": "on"}


if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)

    pipe = Pipeline(
        pipeline_name="Viaje_L85_ExportYAML",
        verbose=True,
        tracking_db="output/export_yaml.db",
    )
    pipe.set_steps([iniciar])
    pipe.run({})

    print("\n📤 Verificando YAML...")
    yaml_path = Path("pipeline_configs/Viaje_L85_ExportYAML.yaml")
    if yaml_path.exists():
        content = yaml_path.read_text()
        print(f"✅ YAML guardado en {yaml_path}")
        print(f"   Tamaño: {len(content)} bytes")
    else:
        print("⚠️ YAML no encontrado")
