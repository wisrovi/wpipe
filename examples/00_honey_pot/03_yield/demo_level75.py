"""
DEMO LEVEL 75: For con Parallel
-----------------------------------
Añade: Parallel dentro de For loop.
Continúa: L74.

DIAGRAMA:
For() {
    Parallel(sensores) {
        camara, radar, lidar
    }
}
"""

from wpipe import Pipeline, For, Parallel, step


@step(name="leer_camara")
def leer_camara(data):
    print("  📷 Cámara")


@step(name="leer_radar")
def leer_radar(data):
    print("  📡 Radar")


@step(name="leer_lidar")
def leer_lidar(data):
    print("  🔴 LiDAR")


@step(name="procesar")
def procesar(data):
    print("🧠 Fusionando datos...")
    return {"fusion": "completa"}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L75_ForParallel", verbose=True)
    pipe.set_steps(
        [
            For(
                iterations=2,
                steps=[
                    Parallel(
                        steps=[leer_camara, leer_radar, leer_lidar], max_workers=3
                    ),
                    procesar,
                ],
            )
        ]
    )
    print("\n>>> Sensores en paralelo dentro de bucle...\n")
    pipe.run({})
