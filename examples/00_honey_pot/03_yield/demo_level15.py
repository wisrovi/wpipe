"""
DEMO LEVEL 15: Reanudación tras Avería (Resume)
----------------------------------------------
Añade: Recuperación automática desde el último checkpoint.
Acumula: Persistencia (L14).

DIAGRAMA:
[¿Avería detectada?] -> [Cargar último Checkpoint]
      |
      v
(Saltar pasos ya hechos) -> (Continuar desde el punto de fallo)
"""

import random

from wpipe import CheckpointManager, Pipeline, step


@step(name="fase_preparacion")
def fase_1(d):
    print("🏠 Saliendo de casa (Paso ya hecho en el pasado)...")
    return {"ubicacion": "carretera"}


@step(name="fase_critica")
def fase_2(d):
    if random.random() < 0.7:
        print("💥 ¡AVERÍA ELÉCTRICA! El sistema se apaga.")
        raise RuntimeError("Fallo de batería")
    print("🏁 Llegada al destino final.")
    return {"status": "Llegado"}


if __name__ == "__main__":
    ck_mgr = CheckpointManager("output/viaje_emergencia.db")
    session = "viaje_retorno"

    pipe = Pipeline(pipeline_name="Viaje_L15_Recovery", verbose=True)
    pipe.set_steps([fase_1, fase_2])

    print(f">>> ¿Podemos reanudar viaje previo? {ck_mgr.can_resume(session)}")
    try:
        pipe.run({}, checkpoint_mgr=ck_mgr, checkpoint_id=session)
    except:
        print("\n[!] El coche se ha detenido. Ejecuta de nuevo para reanudar.")
