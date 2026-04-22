"""
DEMO LEVEL 16: Telemetría Segura (Pydantic)
------------------------------------------
Añade: Validación de datos de sensores con modelos Pydantic.
Acumula: Telemetría del vehículo (L3).

DIAGRAMA:
(leer_sensores) -> [presion: 2.2, fuel: 80]
      |
      v
(validar_telemetria @to_obj(Model)) -> ¡Asegura datos físicos reales!
"""

import random

from pydantic import BaseModel, Field

from wpipe import Pipeline, step, to_obj


# NUEVO EN L16: El coche solo acepta datos en rangos físicos lógicos
class SensorData(BaseModel):
    presion_neumaticos: float = Field(..., ge=1.5, le=3.5)
    nivel_gasolina: float = Field(..., ge=0, le=100)


@step(name="leer_obd2")
def leer_obd2(data):
    print("📡 Leyendo bus de datos OBD2...")

    if random.random() < 0.5:
        return {"presion_neumaticos": 2.3, "freno_activado": True}

    return {"presion_neumaticos": 2.3, "nivel_gasolina": 75.0}


@step(name="analizar_seguridad")
@to_obj(SensorData)  # <--- VALIDACIÓN ACTIVA
def analizar_seguridad(ctx: SensorData):
    print(
        f"📊 Telemetría Validada: Presión={ctx.presion_neumaticos}bar, Fuel={ctx.nivel_gasolina}%"
    )
    return {"seguro_para_circular": True}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L16_SecureData", verbose=True)
    pipe.set_steps([leer_obd2, analizar_seguridad])

    try:
        pipe.run({})
    except Exception as e:
        print(str(e))
