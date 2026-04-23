"""
DEMO LEVEL 75: For con Parallel
-----------------------------------
Adds: Parallel dentro de For loop.
Continues: L74.

DIAGRAM:
For() {
    Parallel(sensores) {
        camara, radar, lidar
    }
}
"""

from wpipe import Pipeline, For, Parallel, step

@step(name="leer_camara")
def leer_camara(data: dict) -> None:

    """Leer camara step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("  📷 Cámara")

@step(name="leer_radar")
def leer_radar(data: dict) -> None:

    """Leer radar step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("  📡 Radar")

@step(name="leer_lidar")
def leer_lidar(data: dict) -> None:

    """Leer lidar step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("  🔴 LiDAR")

@step(name="process")
def process(data: dict) -> None:

    """Process step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("🧠 Fusionando datos...")
    return {"fusion": "completa"}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="viaje_l75_forparallel", verbose=True)
    pipe.set_steps(
        [
            For(
                iterations=2,
                steps=[
                    Parallel(
                        steps=[leer_camara, leer_radar, leer_lidar], max_workers=3
                    ),
                    process,
                ],
            )
        ]
    )
    print("\n>>> Sensores en paralelo dentro de bucle...\n")
    pipe.run({})
