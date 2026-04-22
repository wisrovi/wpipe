"""
DEMO LEVEL 47: Async con For Loop (Simulado)
--------------------------------------
Añade: Bucle en pipeline async (simulado con pasos secuenciales).
Continúa: L46.

DIAGRAMA:
Pasos ejecutados 3 veces secuencialmente
"""

import asyncio

from wpipe import PipelineAsync


async def procesar_frame_0(data):
    print("🖼️ [ASYNC] Frame 0")


async def procesar_frame_1(data):
    print("🖼️ [ASYNC] Frame 1")


async def procesar_frame_2(data):
    print("🖼️ [ASYNC] Frame 2")


async def main():
    pipe = PipelineAsync(pipeline_name="Viaje_L47_AsyncFor", verbose=True)
    pipe.set_steps([procesar_frame_0, procesar_frame_1, procesar_frame_2])
    print("\n>>> Probando async con loop...\n")
    try:
        await pipe.run({})
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
