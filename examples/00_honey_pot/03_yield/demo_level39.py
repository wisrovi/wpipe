"""
DEMO LEVEL 39: Modo Producción (Silent)
---------------------------------------
Añade: Configuración para ejecución en segundo plano sin ruido visual.
Acumula: Rendimiento de Sistemas.

DIAGRAMA:
[Pipeline Normal] -> Prints, Barras, TiempoOs...
[Pipeline Silent] -> ⚡ Silencio total -> Resultados Directos.
"""

from wpipe import Pipeline, step
import time


@step(name="procesar_datos_flota")
def procesar(d):
    return {"sync": "Cloud"}


if __name__ == "__main__":
    # NUEVO EN L39: Configuración ideal para el servidor central que controla la flota
    pipe = Pipeline(
        pipeline_name="Fleet_Control_L39",
        verbose=False,  # Desactiva prints de pasos
        show_progress=False,  # Desactiva barras de carga
    )

    # Ejecutamos 1000 micro-tareas de sincronización
    pipe.set_steps([procesar] * 1000)

    start = time.time()
    print(">>> Iniciando sincronización de flota en modo SILENCIOSO (1000 tareas)...")
    pipe.run({})
    print(f"⚡ Sincronización completada en {time.time() - start:.4f}s con cero logs.")
