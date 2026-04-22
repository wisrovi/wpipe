"""
DEMO LEVEL 19: Tramos Modulares (Nested Pipelines)
--------------------------------------------------
Añade: Uso de un Pipeline como un paso de otro.
Acumula: Modularización de la conducción.

DIAGRAMA:
Pipeline(Viaje Completo) [
  (Preparación)
  Pipeline(Tramo_Ciudad) [
     (Pasar Semáforos)
     (Control de Peatones)
  ]
  (Llegada)
]
"""

from wpipe import Pipeline, step


@step(name="preparar_motor")
def preparar_motor(d):
    return {"motor": "READY"}


# NUEVO EN L19: Definimos un 'sub-viaje' independiente
tramo_urbano = Pipeline(pipeline_name="Conduccion_Urbana")


@step(name="cruzar_paso_cebra")
def cruzar_paso_cebra(d):
    print("🚶 Tramo Urbano: Cediedo el paso a peatones...")
    return {"peatones_cruzando": False}


tramo_urbano.set_steps([cruzar_paso_cebra])

if __name__ == "__main__":
    viaje_total = Pipeline(pipeline_name="Viaje_L19_Modular", verbose=True)

    viaje_total.set_steps(
        [
            preparar_motor,
            tramo_urbano,  # <--- El pipeline urbano actúa como una pieza del viaje
            (lambda d: print("🏁 Viaje completado."), "finalizar", "v1"),
        ]
    )

    viaje_total.run({})
