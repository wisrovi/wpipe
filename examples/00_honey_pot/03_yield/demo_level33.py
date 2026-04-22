"""
DEMO LEVEL 33: Fusión de Visión 360° (Deltas)
---------------------------------------------
Añade: Paralelismo de procesos que suman datos sin colisionar.
Acumula: Multiproceso (L13) y Delta Merging (Librería).

DIAGRAMA:
Parallel(PROCESSES)
  [CPU 1] -> (IA_Señales)  -> Añade 'señales'
  [CPU 2] -> (IA_Objetos)  -> Añade 'objetos'
      |
      v
[Bodega Final] -> Posee AMBOS resultados (Fusión inteligente).
"""

from wpipe import Parallel, Pipeline, step


@step(name="ia_senales")
def ia_senales(d):
    print("🛑 CPU-1: Analizando señales de tráfico...")
    return {"senales": ["Stop", "60km/h"]}


@step(name="ia_objetos")
def ia_objetos(d):
    print("🚶 CPU-2: Analizando peatones y obstáculos...")
    return {"objetos": ["Peatón cruzando"]}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Vision_360_L33", verbose=True)
    pipe.set_steps(
        [Parallel(steps=[ia_senales, ia_objetos], max_workers=2, use_processes=True)]
    )

    final_data = pipe.run({})
    print(f"\n📊 MAPA 360 COMPLETO: {list(final_data.keys())}")
    print(f"   Detecciones: {final_data.get('senales')} + {final_data.get('objetos')}")
