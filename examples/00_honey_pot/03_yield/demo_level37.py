"""
DEMO LEVEL 37: Protocolos de Apagado (Hooks)
--------------------------------------------
Añade: Eventos con pasos asociados para ejecución post-pipeline.
Acumula: Gestión de Errores (L11).

DIAGRAMA:
(Ejecución del Viaje) -- [Éxito o Fracaso] --> (Disparar Hooks)
      |
      v
(enviar_resumen_viaje) -> (apagar_sistemas_ia)
"""

from wpipe import Pipeline, step


@step(name="conducir_tramo_final")
def conducir(d):
    print("🚗 Conduciendo los últimos metros...")
    return {"llegada": "Parking"}


@step(name="protocolo_apagado")
def protocolo_apagado(d):
    print("🧹 HOOK SEGURIDAD: Desactivando cámaras y limpiando memoria temporal...")
    return {"sistemas_dormidos": True}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Safety_Hooks_L37", verbose=True)

    # NUEVO EN L37: Este evento asegura que el paso 'protocolo_apagado' se ejecute AL FINAL
    pipe.add_event(
        event_type="cleanup", event_name="Final de Trayecto", steps=[protocolo_apagado]
    )

    pipe.set_steps([conducir])
    print(">>> Iniciando viaje. Los protocolos de seguridad saltarán al terminar.")
    pipe.run({})
