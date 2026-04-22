"""
DEMO LEVEL 34: Aislamiento de Fallos (Continue on Error)
--------------------------------------------------------
Añade: continue_on_error=True para sistemas secundarios.
Acumula: Gestión de Errores (L11).

DIAGRAMA:
(Frenado_Seguridad) -> OK
      |
(Radio_Spotify)     -> ERROR! (Sin internet)
      |
(Control_Velocidad) -> ¡SIGUE FUNCIONANDO!
"""

from wpipe import Pipeline, step


@step(name="sistema_pilotaje")
def pilotaje(d):
    return {"pilotaje": "ACTIVO"}


@step(name="infoentretenimiento")
def infoentretenimiento(d):
    print("🎵 Radio: Intentando conectar a la nube...")
    raise RuntimeError("Error de red: Streaming no disponible")


@step(name="mantener_distancia")
def mantener_distancia(d):
    print("📏 Radar: Manteniendo distancia de seguridad activa.")
    return {"distancia_ok": True}


if __name__ == "__main__":
    # NUEVO EN L34: Un error en la radio no detiene la navegación
    pipe = Pipeline(
        pipeline_name="Isolation_System_L34", continue_on_error=True, verbose=True
    )

    pipe.set_steps([pilotaje, infoentretenimiento, mantener_distancia])

    print(">>> Iniciando viaje: Los fallos secundarios no afectarán a la conducción.")
    pipe.run({})
