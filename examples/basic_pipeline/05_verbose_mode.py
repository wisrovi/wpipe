"""
Ejemplo 05: Modo Verbose

El modo verbose muestra información detallada de la ejecución.
Útil para depuración y seguimiento del pipeline.
"""

from wpipe import Pipeline


def paso_largo(data):
    """Simula un paso que procesa datos."""
    import time

    time.sleep(0.1)
    return {"procesado": True, "datos": [1, 2, 3, 4, 5]}


def paso_validar(data):
    """Valida los datos procesados."""
    datos = data["datos"]
    return {"valido": len(datos) > 0, "cantidad": len(datos)}


def paso_guardar(data):
    """Guarda el resultado (simulado)."""
    return {"guardado": True}


def main():
    print("=" * 50)
    print("Pipeline SIN modo verbose")
    print("=" * 50)

    pipeline_silencioso = Pipeline(verbose=False)
    pipeline_silencioso.set_steps(
        [
            (paso_largo, "Paso Largo", "v1.0"),
            (paso_validar, "Validar", "v1.0"),
        ]
    )
    resultado = pipeline_silencioso.run({})
    print(f"Resultado: {resultado}")

    print("\n" + "=" * 50)
    print("Pipeline CON modo verbose")
    print("=" * 50)

    pipeline_verbose = Pipeline(verbose=True)
    pipeline_verbose.set_steps(
        [
            (paso_largo, "Paso Largo", "v1.0"),
            (paso_validar, "Validar", "v1.0"),
            (paso_guardar, "Guardar", "v1.0"),
        ]
    )
    resultado = pipeline_verbose.run({})
    print(f"\nResultado final: {resultado}")


if __name__ == "__main__":
    main()
