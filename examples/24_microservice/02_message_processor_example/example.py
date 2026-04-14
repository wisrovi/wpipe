"""
Example 02: Message Processor

Demonstrates a message processor that simulates receiving
messages and processes them through pipelines.
"""

from datetime import datetime

from wpipe import Pipeline
from wpipe.log import new_logger


def paso_extraccion(data: dict) -> dict:
    """Extracts data from the message.

    Args:
        data: Dictionary containing the message.

    Returns:
        Dictionary with extracted fields.

    Example:
        >>> result = paso_extraccion({"id": "123", "tipo": "user"})
        >>> print(result["extraido"])
        True
    """
    print("    [EXTRACCION] Extrayendo campos...")
    return {
        "extraido": True,
        "id": data.get("id", "N/A"),
        "tipo": data.get("tipo", "unknown"),
    }


def paso_transformacion(data: dict) -> dict:
    """Transforms extracted data.

    Args:
        data: Dictionary containing extracted data.

    Returns:
        Dictionary with transformed data.

    Example:
        >>> result = paso_transformacion({"id": "abc", "tipo": "USER"})
        >>> print(result["transformado"])
        True
    """
    print("    [TRANSFORMACION] Transformando datos...")
    return {
        "transformado": True,
        "datos_transformados": {
            "id_upper": str(data.get("id", "")).upper(),
            "tipo_normalizado": data.get("tipo", "").lower(),
        },
    }


def paso_enriquecimiento(data: dict) -> dict:
    """Enriches data with metadata.

    Args:
        data: Dictionary containing data to enrich.

    Returns:
        Dictionary with enriched data and metadata.

    Example:
        >>> result = paso_enriquecimiento({})
        >>> print(result["enriquecido"])
        True
    """
    print("    [ENRIQUECIMIENTO] Agregando metadatos...")
    return {
        "enriquecido": True,
        "metadatos": {
            "procesado_en": datetime.now().isoformat(),
            "pipeline_version": "v1.0",
        },
    }


def paso_persistencia(data: dict) -> dict:
    """Prepares data for persistence.

    Args:
        data: Dictionary containing processed data.

    Returns:
        Dictionary ready for storage.

    Example:
        >>> result = paso_persistencia({"id": "123", "datos_transformados": {}})
        >>> print(result["listo_para_guardar"])
        True
    """
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
    """Message processor with integrated pipeline.

    Attributes:
        nombre: Processor name identifier.
        mensajes_procesados: Count of successfully processed messages.
        errores: Count of processing errors.
    """

    def __init__(self, nombre: str = "procesador") -> None:
        """Initializes the message processor.

        Args:
            nombre: Processor name identifier. Defaults to "procesador".
        """
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
        """Processes a message through the pipeline.

        Args:
            mensaje: Dictionary containing the message to process.

        Returns:
            Dictionary with processing result or error.

        Example:
            >>> proc = ProcesadorMensajes("test")
            >>> result = proc.procesar({"id": "1", "tipo": "test"})
            >>> print(result.get("extraido", False) or "error" in result)
            True
        """
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
        """Returns processor statistics.

        Returns:
            Dictionary with processor statistics.

        Example:
            >>> proc = ProcesadorMensajes("test")
            >>> stats = proc.obtener_estadisticas()
            >>> print(stats["nombre"])
            test
        """
        return {
            "nombre": self.nombre,
            "procesados": self.mensajes_procesados,
            "errores": self.errores,
            "tasa_exito": (self.mensajes_procesados - self.errores)
            / max(self.mensajes_procesados, 1),
        }


def generar_mensaje_simulado(indice: int) -> dict:
    """Generates a simulated message.

    Args:
        indice: Message index for ID generation.

    Returns:
        Dictionary with simulated message data.

    Example:
        >>> msg = generar_mensaje_simulado(1)
        >>> print("id" in msg and "tipo" in msg)
        True
    """
    tipos = ["usuario", "producto", "orden", "pago"]
    return {
        "id": f"MSG-{indice:04d}",
        "tipo": tipos[indice % len(tipos)],
        "datos": {"valor": indice * 100, "activo": True},
    }


def main() -> None:
    """Runs the message processor example."""
    print("=" * 70)
    print("PROCESADOR DE MENSAJES")
    print("=" * 70)

    print("\n--- Creando Procesador ---")
    procesador = ProcesadorMensajes("procesador_principal")

    print("\n--- Simulando Recepciones ---")

    mensajes_simulados = [generar_mensaje_simulado(i) for i in range(1, 6)]

    print(f"Mensajes a procesar: {len(mensajes_simulados)}")

    for i, msg in enumerate(mensajes_simulados, 1):
        print(f"\n{'=' * 50}")
        print(f"MENSAJE {i}/{len(mensajes_simulados)}")
        print(f"{'=' * 50}")
        print(f"ID: {msg['id']}")
        print(f"Tipo: {msg['tipo']}")

        resultado = procesador.procesar(msg)

        print("\n[RESULTADO]")
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
    print(
        """
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
"""
    )


if __name__ == "__main__":
    main()
