"""
DEMO LEVEL 24: El Odómetro Total (Shared Memory)
-----------------------------------------------
Añade: Uso del módulo 'memory' para datos que trascienden el viaje.
Acumula: Persistencia (L14).

DIAGRAMA:
(Viaje Mañana) -> Actualiza memory['total_km']
      |
(Viaje Tarde)  -> Lee memory['total_km'] y lo aumenta
"""

from wpipe import Pipeline, memory, step


@step(name="registrar_tramo")
def registrar_tramo(data):
    km_actuales = 40
    # NUEVO EN L24: Guardamos en RAM global persistente
    total = memory.get("odometro_coche", 0) + km_actuales
    memory.set("odometro_coche", total)

    print(f"🛣️  Tramo: +{km_actuales}km | Odómetro Total en Memoria: {total}km")
    return {"km_totales": total}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L24_Memory", verbose=True)
    pipe.set_steps([registrar_tramo])

    print(">>> Arrancando el coche por primera vez:")
    pipe.run({})
    print("\n>>> Arrancando el coche por segunda vez (Memoria mantenida):")
    pipe.run({})
