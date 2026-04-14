"""
Example 01: Basic Microservice Structure

Demonstrates the basic structure of a microservice using wpipe,
without requiring Kafka for local testing.
"""

from datetime import datetime

from wpipe import Pipeline
from wpipe.log import new_logger


def paso_validacion(data: dict) -> dict:
    """Validates incoming messages.

    Args:
        data: Dictionary containing the message to validate.

    Returns:
        Dictionary with validation result and message.

    Example:
        >>> result = paso_validacion({"mensaje": "test"})
        >>> print(result["validado"])
        True
    """
    print("  [PASO] Validando mensaje...")
    if "mensaje" not in data:
        raise ValueError("Campo 'mensaje' requerido")
    return {"validado": True, "mensaje": data["mensaje"]}


def paso_procesamiento(data: dict) -> dict:
    """Processes message data.

    Args:
        data: Dictionary containing the message to process.

    Returns:
        Dictionary with processing result and metadata.

    Example:
        >>> result = paso_procesamiento({"mensaje": "hello"})
        >>> print(result["procesado"])
        True
    """
    print("  [PASO] Procesando datos...")
    mensaje = data.get("mensaje", "")
    return {
        "procesado": True,
        "mensaje_upper": mensaje.upper(),
        "longitud": len(mensaje),
    }


def paso_enriquecimiento(data: dict) -> dict:
    """Enriches data with metadata.

    Args:
        data: Dictionary containing data to enrich.

    Returns:
        Dictionary with enriched data and metadata.

    Example:
        >>> result = paso_enriquecimiento({"origen": "test"})
        >>> print(result["enriquecido"])
        True
    """
    print("  [PASO] Enriqueciendo datos...")
    return {
        "enriquecido": True,
        "timestamp": datetime.now().isoformat(),
        "origen": data.get("origen", "unknown"),
    }


class MicroservicioBasico:
    """Basic microservice with integrated pipeline.

    Attributes:
        nombre: Service name identifier.
        ejecutando: Whether the service is running.
        contador_mensajes: Number of messages processed.
    """

    def __init__(self, nombre: str = "microservicio_basico") -> None:
        """Initializes the basic microservice.

        Args:
            nombre: Service name identifier. Defaults to "microservicio_basico".
        """
        self.nombre = nombre
        self.ejecutando = False
        self.contador_mensajes = 0

        self.logger = new_logger(
            process_name=nombre, path_file="logs/microservicio_{time}.log"
        )

        self.pipeline = Pipeline(verbose=True)
        self.pipeline.set_steps(
            [
                (paso_validacion, "Validacion", "v1.0"),
                (paso_procesamiento, "Procesamiento", "v1.0"),
                (paso_enriquecimiento, "Enriquecimiento", "v1.0"),
            ]
        )

        self.logger.info(f"[INIT] {self.nombre} inicializado")

    def procesar_mensaje(self, mensaje: dict) -> dict:
        """Processes a message through the pipeline.

        Args:
            mensaje: Dictionary containing the message to process.

        Returns:
            Dictionary with processing result or error.

        Example:
            >>> servicio = MicroservicioBasico("test")
            >>> result = servicio.procesar_mensaje({"mensaje": "test"})
            >>> print("error" in result or result.get("validado"))
            True
        """
        self.contador_mensajes += 1
        mensaje_id = self.contador_mensajes

        self.logger.info(f"[MSG-{mensaje_id}] Procesando mensaje...")

        try:
            mensaje["origen"] = self.nombre
            resultado = self.pipeline.run(mensaje)
            self.logger.info(f"[MSG-{mensaje_id}] Completado")
            return resultado
        except Exception as e:
            self.logger.error(f"[MSG-{mensaje_id}] Error: {e}")
            return {"error": str(e)}

    def iniciar(self) -> None:
        """Starts the microservice.

        Example:
            >>> servicio = MicroservicioBasico("test")
            >>> servicio.iniciar()  # doctest: +SKIP
        """
        self.ejecutando = True
        self.logger.info(f"[START] {self.nombre} iniciado")
        print(f"\n[MICROSERVICIO] {self.nombre} iniciado")
        print(f"  Mensajes procesados: {self.contador_mensajes}")

    def detener(self) -> None:
        """Stops the microservice.

        Example:
            >>> servicio = MicroservicioBasico("test")
            >>> servicio.detener()  # doctest: +SKIP
        """
        self.ejecutando = False
        self.logger.info(f"[STOP] {self.nombre} detenido")
        print(f"\n[MICROSERVICIO] {self.nombre} detenido")
        print(f"  Total mensajes procesados: {self.contador_mensajes}")


def main() -> None:
    """Runs the basic microservice example."""
    print("=" * 70)
    print("MICROSERVICIO BASICO")
    print("=" * 70)

    print("\n--- Creando Microservicio ---")
    servicio = MicroservicioBasico("servicio_prueba")
    servicio.iniciar()

    print("\n--- Simulando Mensajes ---")

    mensajes = [
        {"mensaje": "hola mundo"},
        {"mensaje": "procesando datos"},
        {"mensaje": "mensaje de prueba"},
        {"mensaje": "otro mensaje"},
    ]

    for i, msg in enumerate(mensajes, 1):
        print(f"\n[MENSAJE {i}] Enviando: {msg}")
        resultado = servicio.procesar_mensaje(msg)
        print(f"[RESULTADO {i}] {resultado}")

    print("\n--- Deteniendo Microservicio ---")
    servicio.detener()

    print("\n" + "=" * 70)
    print("RESUMEN DE ESTRUCTURA")
    print("=" * 70)
    print(
        """
Estructura de un Microservicio Basico:

1. Inicializacion:
   - Crear logger
   - Crear pipeline con pasos
   - Configurar servicios

2. Procesamiento:
   - Recibir mensaje
   - Validar mensaje
   - Ejecutar pipeline
   - Devolver resultado

3. Control de vida:
   - iniciar(): Iniciar servicios
   - detener(): Limpiar recursos

Esta estructura puede extenderse con:
- Kafka para recibir mensajes
- SQLite para persistencia
- API para health checks
"""
    )


if __name__ == "__main__":
    main()
