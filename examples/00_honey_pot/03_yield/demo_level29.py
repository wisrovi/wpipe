"""
DEMO LEVEL 29: Guardado de Seguridad (Smart Checkpoints)
--------------------------------------------------------
Añade: Checkpoints que solo se disparan bajo condiciones críticas.
Acumula: Persistencia (L14).

DIAGRAMA:
(Viaje) -> [¿Gasolina < 15%?] -- SÍ --> (Guardar Punto de Rescate)
"""

import os

from wpipe import CheckpointManager, Pipeline, step


@step(name="consumo_critico")
def consumo_critico(data):
    # Simulamos que la gasolina baja peligrosamente
    fuel_actual = 10
    print(f"⛽ Alerta de Combustible: {fuel_actual}%")
    return {"gasolina": fuel_actual}


if __name__ == "__main__":
    ck_mgr = CheckpointManager("output/coche_seguridad.db")
    pipe = Pipeline(pipeline_name="Safety_First_L29", verbose=True)

    # NUEVO EN L29: El coche guarda partida automáticamente solo si el fuel es bajo
    pipe.add_checkpoint(checkpoint_name="punto_de_rescate", expression="gasolina < 15")

    pipe.set_steps([consumo_critico])
    pipe.run({"gasolina": 100}, checkpoint_mgr=ck_mgr, checkpoint_id="viaje_nocturno")
