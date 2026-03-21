"""
Ejemplo 03: Microservicio con Pipeline Integrado

Este ejemplo demuestra un microservicio completo con pipeline,
configuracion YAML, y registro de worker.
"""

import time
import os
from datetime import datetime
from wpipe import Pipeline
from wpipe.util import leer_yaml, escribir_yaml
from wpipe.log import new_logger
from wpipe.sqlite import Wsqlite


def paso_validar(data: dict) -> dict:
    """Valida el mensaje de entrada."""
    print("    [STEP] Validando mensaje...")
    if "tipo" not in data:
        raise ValueError("Campo 'tipo' requerido")
    return {"validado": True, "tipo": data["tipo"]}


def paso_procesar(data: dict) -> dict:
    """Procesa los datos."""
    print("    [STEP] Procesando datos...")
    tipo = data.get("tipo", "desconocido")
    return {
        "procesado": True,
        "resultado": f"procesado_{tipo}",
        "timestamp": datetime.now().isoformat(),
    }


def paso_guardar(data: dict) -> dict:
    """Guarda el resultado en SQLite."""
    print("    [STEP] Guardando resultado...")
    return {"guardado": True, "db_name": data.get("db_name", "default.db")}


class MicroservicioConPipeline:
    """Microservicio completo con pipeline."""

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = self._crear_config_default()

        self.config = leer_yaml(config_path)
        self.config_path = config_path

        self.nombre = self.config.get("nombre", "microservicio")
        self.version = self.config.get("version", "v1.0")

        os.makedirs("logs", exist_ok=True)
        self.logger = new_logger(
            process_name=self.nombre, path_file=f"logs/{self.nombre}_{{time}}.log"
        )

        api_config = self._crear_api_config()
        self.pipeline = Pipeline(
            api_config=api_config, worker_name=self.nombre, verbose=True
        )
        self.pipeline.set_steps(
            [
                (paso_validar, "Validar", "v1.0"),
                (paso_procesar, "Procesar", "v1.0"),
                (paso_guardar, "Guardar", "v1.0"),
            ]
        )

        self.worker_id_file = self.config.get("worker_id_file", "worker_id.yaml")
        self.mensajes_procesados = 0

        self.logger.info(f"Microservicio {self.nombre} v{self.version} iniciado")

    def _crear_config_default(self) -> str:
        """Crea configuracion por defecto."""
        config = {
            "nombre": "microservicio_ejemplo",
            "version": "1.0.0",
            "pipeline_use": True,
            "pipeline_server": "http://localhost:8418",
            "pipeline_token_server": "mysecrettoken",
            "sqlite_db_name": "microservicio.db",
            "worker_id_file": "worker_id.yaml",
        }
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            escribir_yaml(f.name, config)
            return f.name

    def _crear_api_config(self):
        """Crea configuracion de API."""
        if self.config.get("pipeline_use"):
            return {
                "base_url": self.config.get("pipeline_server"),
                "token": self.config.get("pipeline_token_server"),
            }
        return None

    def registrar_worker(self):
        """Registra el worker con la API."""
        try:
            worker_info = self.pipeline.worker_register(
                name=self.nombre, version=self.version
            )
            if worker_info and "id" in worker_info:
                worker_info["registro"] = datetime.now().isoformat()
                escribir_yaml(self.worker_id_file, worker_info)
                self.pipeline.set_worker_id(worker_info["id"])
                self.logger.info(f"Worker registrado: {worker_info['id']}")
                return worker_info
        except Exception as e:
            self.logger.warning(f"Registro de worker fallido: {e}")
        return None

    def ejecutar(self, mensaje: dict) -> dict:
        """Ejecuta el pipeline con un mensaje."""
        self.mensajes_procesados += 1
        self.logger.info(f"Procesando mensaje {self.mensajes_procesados}")

        try:
            mensaje["db_name"] = self.config.get("sqlite_db_name", "microservicio.db")
            resultado = self.pipeline.run(mensaje)
            self.logger.info("Mensaje procesado exitosamente")
            return resultado
        except Exception as e:
            self.logger.error(f"Error procesando mensaje: {e}")
            return {"error": str(e)}

    def obtener_estado(self) -> dict:
        """Obtiene el estado del microservicio."""
        return {
            "nombre": self.nombre,
            "version": self.version,
            "mensajes_procesados": self.mensajes_procesados,
            "pipeline_activo": self.pipeline is not None,
            "worker_id": self.pipeline.worker_id if self.pipeline else None,
        }


def main():
    print("=" * 70)
    print("MICROSERVICIO CON PIPELINE INTEGRADO")
    print("=" * 70)

    print("\n--- Creando Microservicio ---")
    servicio = MicroservicioConPipeline()

    print(f"\nConfiguracion:")
    print(f"  Nombre: {servicio.nombre}")
    print(f"  Version: {servicio.version}")
    print(f"  Archivo config: {servicio.config_path}")

    print("\n--- Registrando Worker ---")
    registro = servicio.registrar_worker()
    if registro:
        print(f"  Worker registrado: {registro.get('id', 'N/A')}")
    else:
        print("  Registro no disponible (modo offline)")

    print("\n--- Procesando Mensajes ---")

    mensajes = [
        {"tipo": "usuario", "datos": {"nombre": "Juan"}},
        {"tipo": "producto", "datos": {"sku": "PROD-001"}},
        {"tipo": "orden", "datos": {"id": 12345}},
    ]

    for i, msg in enumerate(mensajes, 1):
        print(f"\n[MENSAJE {i}] Tipo: {msg['tipo']}")
        resultado = servicio.ejecutar(msg)
        print(f"  Validado: {resultado.get('validado', False)}")
        print(f"  Procesado: {resultado.get('procesado', False)}")
        print(f"  Guardado: {resultado.get('guardado', False)}")

    print("\n--- Estado del Microservicio ---")
    estado = servicio.obtener_estado()
    print(f"\nEstado actual:")
    for clave, valor in estado.items():
        print(f"  {clave}: {valor}")

    os.unlink(servicio.config_path)
    print(f"\n[OK] Archivo temporal eliminado")

    print("\n" + "=" * 70)
    print("COMPONENTES DEL MICROSERVICIO")
    print("=" * 70)
    print("""
Componentes integrados:

1. CONFIGURACION (YAML)
   - Lee configuracion de archivo
   - Parametros por entorno

2. PIPELINE (wpipe)
   - Pasos de procesamiento
   - Manejo de errores

3. WORKER (API)
   - Registro con API
   - Health checking

4. PERSISTENCIA (SQLite)
   - Guardar resultados
   - Historial de mensajes

5. LOGGING
   - Registro de eventos
   - Diagnosticos
""")


if __name__ == "__main__":
    main()
