"""
DEMO LEVEL 21: Timeouts (Seguridad de Respuesta)
-----------------------------------------------
Añade: Parámetro timeout para evitar bloqueos del sistema.
Acumula: Inferencia (L10) y Captura de Errores (L11).

DIAGRAMA:
(radar_proximidad) -- [¿Tarda más de 0.2s?] -- ¡ABORTAR!
      |
      v
(alarma_seguridad) -> [Error: Timeout]
"""

import time

from wpipe import Pipeline, step


# NUEVO EN L21: Límite de tiempo estricto para el sensor
@step(name="radar_proximidad", timeout=0.2)
def radar_proximidad(data):
    print("📡 Radar: Escaneando entorno...")
    # Simulamos que el hardware del radar se queda 'colgado'
    time.sleep(1.0)
    return {"obstaculo": False}


def reporte_emergencia(context, error):
    print(f"\n🚨 ALERTA CRÍTICA: El sensor '{error['step_name']}' no responde.")
    print("🛑 ACCIÓN: Cambiando a modo de conducción manual.\n")
    return context


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L21_Timeout", verbose=True)
    pipe.add_error_capture([reporte_emergencia])

    pipe.set_steps([radar_proximidad])

    print(">>> Test de seguridad: Comprobando que el radar no bloquee el sistema...")
    pipe.run({})
