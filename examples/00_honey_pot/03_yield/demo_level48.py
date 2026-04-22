"""
DEMO LEVEL 48: Async con Métricas
--------------------------------------
Añade: Métricas en pipeline async.
Continúa: L47.

DIAGRAMA:
(async procesar) --> [Metric: tiempo_proceso]
"""

import asyncio

from wpipe import PipelineAsync, Metric


async def procesar_datos(data):
    await asyncio.sleep(0.05)
    print("📊 [ASYNC] Procesando datos...")
    Metric.record("datos_procesados", 100)
    return {"procesado": 100}


async def main():
    pipe = PipelineAsync(pipeline_name="Viaje_L48_AsyncMetric", verbose=True)
    pipe.set_steps([procesar_datos])
    print("\n>>> Probando async con métricas...\n")
    try:
        await pipe.run({})
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
