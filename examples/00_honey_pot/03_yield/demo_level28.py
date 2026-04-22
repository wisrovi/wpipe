"""
DEMO LEVEL 28: El Diario del Conductor (Events)
-----------------------------------------------
Añade: Marcadores manuales en la línea de tiempo.
Acumula: Métricas y Tracking.

DIAGRAMA:
[Viaje] ---- [Evento: 'Radar Detectado'] ---- [Viaje] ---- [Evento: 'Pausa Café']
"""

from wpipe import Pipeline, step


@step(name="cruzar_frontera")
def cruzar_paso(data):
    print("🌍 Cruzando frontera: Cambiando normativa de tráfico...")
    return {"pais": "Portugal"}


if __name__ == "__main__":
    pipe = Pipeline(
        pipeline_name="Travel_Log_L28",
        tracking_db="output/coche_eventos.db",
        verbose=True,
    )

    # NUEVO EN L28: Anotamos hitos que no cambian la bodega, pero quedan registrados
    pipe.add_event(
        event_type="annotation",
        event_name="Inicio de Ruta",
        message="Conductor: William R. | Clima: Despejado",
    )

    pipe.set_steps([cruzar_paso])
    pipe.run({})
