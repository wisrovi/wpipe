"""
Ejemplo 02: Procesador de Mensajes

Este ejemplo demonstra un procesador de mensajes que simula
la recepcion de mensajes y los procesa con pipelines.
"""

import time
from datetime import datetime
from wpipe import Pipeline
from wpipe.log import new_logger


def paso_extraccion(data: dict) -> dict:
    """Extrae datos del mensaje."""
    print("    [EXTRACCION] Extrayendo campos...")
    return {
        "extraido": True,
        "id": data.get("id", "N/A"),
        "tipo": data.get("tipo", "unknown"),
    }


def paso_transformacion(data: dict) -> dict:
    """Transforma los datos extraidos."""
    print("    [TRANSFORMACION] Transformando datos...")
    return {
        "transformado": True,
        "datos_transformados": {
            "id_upper": str(data.get("id", "")).upper(),
            "tipo_normalizado": data.get("tipo", "").lower(),
        },
    }


def paso_enriquecimiento(data: dict) -> dict:
    """Enriquece con metadatos."""
    print("    [ENRIQUECIMIENTO] Agregando metadatos...")
    return {
        "enriquecido": True,
        "metadatos": {
            "procesado_en": datetime.now().isoformat(),
            "pipeline_version": "v1.0",
        },
    }


def paso_persistencia(data: dict) -> dict:
    """Prepara datos para persistencia."""
    print("    [PERSISTENCIA] Preparando guardado...")
    return {
        "listo_para_guardar": True,
        "registro": {
            "id": data.get("id"),
            "datos": data.get("datos_transformados"),
            "metadatos": data.get("metadatos"),
        },
    }


class ProcesadorMensajes:
    """Procesador de mensajes con pipeline."""

    def __init__(self, nombre: str = "procesador"):
        self.nombre = nombre
        self.mensajes_procesados = 0
        self.errores = 0

        self.logger = new_logger(
            process_name=nombre, path_file="logs/procesador_{time}.log"
        )

        self.pipeline = Pipeline(verbose=False)
        self.pipeline.set_steps(
            [
                (paso_extraccion, "Extraccion", "v1.0"),
                (paso_transformacion, "Transformacion", "v1.0"),
                (paso_enriquecimiento, "Enriquecimiento", "v1.0"),
                (paso_persistencia, "Persistencia", "v1.0"),
            ]
        )

    def procesar(self, mensaje: dict) -> dict:
        """Procesa un mensaje con el pipeline."""
        try:
            print(f"\n[PROCESANDO] Mensaje ID: {mensaje.get('id', 'N/A')}")
            resultado = self.pipeline.run(mensaje)
            self.mensajes_procesados += 1
            self.logger.info(f"Mensaje {mensaje.get('id')} procesado exitosamente")
            return resultado
        except Exception as e:
            self.errores += 1
            self.logger.error(f"Error procesando mensaje: {e}")
            return {"error": str(e)}

    def obtener_estadisticas(self) -> dict:
        """Retorna estadisticas del procesador."""
        return {
            "nombre": self.nombre,
            "procesados": self.mensajes_procesados,
            "errores": self.errores,
            "tasa_exito": (self.mensajes_procesados - self.errores)
            / max(self.mensajes_procesados, 1),
        }


def generar_mensaje_simulado(indice: int) -> dict:
    """Genera un mensaje simulado."""
    tipos = ["usuario", "producto", "orden", "pago"]
    return {
        "id": f"MSG-{indice:04d}",
        "tipo": tipos[indice % len(tipos)],
        "datos": {"valor": indice * 100, "activo": True},
    }


def main():
    print("=" * 70)
    print("PROCESADOR DE MENSAJES")
    print("=" * 70)

    print("\n--- Creando Procesador ---")
    procesador = ProcesadorMensajes("procesador_principal")

    print("\n--- Simulando Recepciones ---")

    mensajes_simulados = [generar_mensaje_simulado(i) for i in range(1, 6)]

    print(f"Mensajes a procesar: {len(mensuales for _ in mensajes_simulados)}")

    for i, msg in enumerate(mensajes_simulados, 1):
        print(f"\n{'=' * 50}")
        print(f"MENSAJE {i}/{len(mensajes_simulados)}")
        print(f"{'=' * 50}")
        print(f"ID: {msg['id']}")
        print(f"Tipo: {msg['tipo']}")

        resultado = procesador.procesar(msg)

        print(f"\n[RESULTADO]")
        print(f"  Extraido: {resultado.get('extraido', False)}")
        print(f"  Transformado: {resultado.get('transformado', False)}")
        print(f"  Enriquecido: {resultado.get('enriquecido', False)}")
        print(f"  Listo para guardar: {resultado.get('listo_para_guardar', False)}")

    print(f"\n{'=' * 70}")
    print("ESTADISTICAS FINALES")
    print(f"{'=' * 70}")

    estadisticas = procesador.obtener_estadisticas()
    print(f"\nProcesador: {estadisticas['nombre']}")
    print(f"Mensajes procesados: {estadisticas['procesados']}")
    print(f"Errores: {estadisticas['errores']}")
    print(f"Tasa de exito: {estadisticas['tasa_exito']:.1%}")

    print("\n" + "=" * 70)
    print("FLUJO DE PROCESAMIENTO")
    print("=" * 70)
    print("""
Flujo de un mensaje a traves del procesador:

1. RECEPCION
   - Mensaje llega al procesador
   - Log de recepcion

2. EXTRACCION
   - Extrae campos relevantes
   - Valida estructura

3. TRANSFORMACION
   - Convierte datos a formato estandar
   - Normaliza valores

4. ENRIQUECIMIENTO
   - Agrega metadatos
   - Anade timestamps

5. PERSISTENCIA
   - Prepara registro para guardar
   - Devuelve resultado
""")


if __name__ == "__main__":
    main()
