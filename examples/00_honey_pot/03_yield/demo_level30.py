"""
DEMO LEVEL 30: Ruta desde el Satélite (External YAML)
-----------------------------------------------------
Añade: Carga de la configuración del viaje desde un archivo YAML.
Acumula: Modularización (L19).

DIAGRAMA:
[satelite.yaml] -> (leer_yaml) -> [Configuración] -> Pipeline.run()
"""

import os

from wpipe import Pipeline, step
from wpipe.util import escribir_yaml, leer_yaml


@step(name="mostrar_destino")
def mostrar_destino(data):
    config = data.get("config_externa", {})
    print(
        f"📡 Satélite: Recibida ruta a {config.get('destino')} via {config.get('ruta')}"
    )
    return {"llegada_estimada": "14:00"}


if __name__ == "__main__":
    # Creamos un archivo de configuración simulando la app del móvil
    os.makedirs("pipeline_configs", exist_ok=True)
    mock_config = {"destino": "Lisboa", "ruta": "Peaje", "paradas": 2}
    config_path = "pipeline_configs/satelite.yaml"
    escribir_yaml(config_path, mock_config)

    # NUEVO EN L30: Cargamos los datos antes de arrancar
    datos_satelite = leer_yaml(config_path)

    pipe = Pipeline(pipeline_name="Connected_Car_L30", verbose=True)
    pipe.set_steps([mostrar_destino])

    print(">>> Sincronizando con el móvil...")
    pipe.run({"config_externa": datos_satelite})
