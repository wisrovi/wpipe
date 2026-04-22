"""
DEMO LEVEL 32: El Túnel de la Resiliencia (Retries)
---------------------------------------------------
Añade: Reintentos con espera prolongada para fallos persistentes.
Acumula: Reintentos (L22).

DIAGRAMA:
(conectar_gps) -- [Fallo 1] -> Espera 0.5s
      |--- [Fallo 2] -> Espera 0.5s
      |--- [Fallo 3] -> Espera 0.5s (Saliendo del túnel...)
      |--- [¡ÉXITO!] -> Señal recuperada.
"""

from wpipe import Pipeline, step

intento_local = 0


@step(name="recuperar_gps", retry_count=3, retry_delay=0.5)
def recuperar_gps(data):
    global intento_local
    intento_local += 1
    if intento_local < 3:
        print(f"📡 Satélite: Intento {intento_local} fallido (Túnel)...")
        raise ConnectionError("Sin visibilidad")

    print("📡 Satélite: ¡Señal GPS fijada!")
    return {"locked": True}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="GPS_Tunnel_L32", verbose=True)
    pipe.set_steps([recuperar_gps])
    print(">>> Entrando en zona de baja cobertura (Túnel)...")
    pipe.run({})
