"""
DEMO LEVEL 13: CPU de Alto Rendimiento (Processes)
--------------------------------------------------
Añade: Uso de núcleos reales para procesar mapas de profundidad pesados.
Acumula: Visión 360° (L12).

DIAGRAMA:
[Proceso CPU 1] -> (Analizar Texturas Carretera)
[Proceso CPU 2] -> (Reconocer Señales de Tráfico)
[Proceso CPU 3] -> (Predecir Trayectorias Peatones)
"""

import os
import time

from wpipe import Parallel, Pipeline, step


@step(name="analisis_profundo")
def analisis_profundo(d):
    # Simulamos carga de CPU real de un modelo de red neuronal
    start = time.time()
    while time.time() - start < 0.2:
        pass
    print(f"🧠 Engine IA (PID {os.getpid()}): Mapa de profundidad generado.")
    return {"mapa": "completo"}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L13_HeavyAI", verbose=True)
    pipe.set_steps(
        [
            Parallel(
                steps=[analisis_profundo] * 3,
                max_workers=3,
                use_processes=True,  # <--- Uso de potencia real del motor de IA
            )
        ]
    )
    pipe.run({})
