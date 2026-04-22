"""
DEMO LEVEL 46: Async con Condition
--------------------------------------
Añade: Condition en pipeline async.
Continúa: L45.

DIAGRAMA:
(async evaluar_situacion)
      |
      +-- (obstaculo == True) -> [FRENO]
      +-- (obstaculo == False) -> [ACELERAR]
"""

import asyncio
import random

from wpipe import PipelineAsync, Condition


async def evaluar_situacion(data):
    await asyncio.sleep(0.05)
    obstaculo = random.random() < 0.3
    print(f"🚗 [ASYNC] Evaluación: obstáculo={obstaculo}")
    return {"obstaculo": obstaculo}


async def frenar(data):
    print("🛑 [ASYNC] Frenando de emergencia")
    return {"action": "brake"}


async def acelerar(data):
    print("🚀 [ASYNC] Acelerando")
    return {"action": "accelerate"}


async def main():
    pipe = PipelineAsync(pipeline_name="Viaje_L46_AsyncCondition", verbose=True)
    pipe.set_steps(
        [
            evaluar_situacion,
            Condition(
                expression="obstaculo == True",
                branch_true=[frenar],
                branch_false=[acelerar],
            ),
        ]
    )
    print("\n>>> Probando async con condiciones...\n")
    try:
        await pipe.run({})
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
