"""
DEMO LEVEL 14: Parada en Área de Servicio (Checkpoints)
-------------------------------------------------------
Añade: Guardado del estado del viaje en una parada.
Acumula: Toda la telemetría del viaje.

DIAGRAMA:
(Tramo 1: Ciudad) -> (Llegada Área Servicio)
      |
      v
[CHECKPOINT: 'descanso_1'] --> (Guarda Gasolina, Km, Destino en DB)
      |
      v
(Tramo 2: Autopista)
"""

import os

from wpipe import CheckpointManager, Pipeline, step


@step(name="conducir_hasta_area")
def conducir_hasta_area(d):
    print("🛣️  Conduciendo 100km hasta el área de servicio...")
    return {"km": 100, "gasolina": 70}


@step(name="descanso")
def descanso(d):
    print("☕ Tomando un café. El coche guarda el progreso automáticamente.")
    return {"descansado": True}


if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    ck_mgr = CheckpointManager("output/viaje_progreso.db")

    pipe = Pipeline(pipeline_name="Viaje_L14_Checkpoints", verbose=True)
    pipe.set_steps([conducir_hasta_area, descanso])

    # El sistema registra el hito 'parada_1'
    pipe.run(
        {"viaje_id": "vacaciones_2026"}, checkpoint_mgr=ck_mgr, checkpoint_id="viaje_1"
    )
