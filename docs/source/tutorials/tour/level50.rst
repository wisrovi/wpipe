Nivel 50: Integración Final - El Viaje Completo
==============================================

.. meta::
   :description: Integración de todas las funcionalidades de WPipe en un único flujo complejo.
   :keywords: integration, complex, parallel, for-loop, checkpoints, alerts, wpipe

Objetivo
--------
Consolidar todos los conocimientos adquiridos en los primeros 50 niveles. Crearemos un pipeline de "Viaje en Coche" que utiliza paralelismo, bucles, condiciones, alertas de rendimiento, manejo de errores forense y exportación de datos.

Conceptos Clave
---------------
* **Orquestación Compleja**: Combinación de `Parallel`, `For` y `Condition` en una estructura jerárquica.
* **Alertas de Rendimiento**: Uso de `add_alert_threshold` para detectar cuellos de botella en tiempo real.
* **Resiliencia Extrema**: Captura de errores con notificaciones personalizadas (simulación de Telegram).
* **Observabilidad**: Monitoreo de recursos del sistema (CPU/RAM) y exportación a JSON/CSV.

¿Qué estamos probando?
----------------------
Este nivel es la prueba de fuego para el motor. Validamos:
1. La capacidad de manejar **objetos no serializables** en el contexto sin romper la persistencia.
2. La ejecución de tareas en paralelo mientras se mantiene el registro de logs thread-safe.
3. La activación de **checkpoints inteligentes** basados en expresiones lógicas.
4. La recuperación automática mediante reintentos en pasos específicos (`random_flat_tire`).

Código Fuente
------------

.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level50.py
   :language: python
   :linenos:

Análisis de la Ejecución
------------------------

Este pipeline realiza las siguientes acciones:
1. **Preparación**: Inicia una fase de preparación global.
2. **Bucle de Viajes**: Realiza 3 iteraciones de viaje.
3. **Mantenimiento en Paralelo**: En cada viaje, reposta combustible, cambia el aceite y revisa luces simultáneamente.
4. **Conducción Dinámica**: Conduce mientras el tanque no esté vacío, inflando neumáticos si la presión baja.
5. **Gestión de Fallos**: Si ocurre un pinchazo aleatorio, reintenta hasta 10 veces antes de reportar un error.
6. **Auditoría**: Al finalizar, genera un reporte completo de consumo de recursos y exporta los resultados.

Resultado de Ejecución
----------------------

.. code-block:: text

   >>> [CHECKPOINT] Inicio del viaje
   --- Nuevo viaje --- (Iteración: 0)
   viaje - print_info ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
   ...
   Resource Summary:
     - Peak RAM: 4200 MB
     - Avg CPU: 55%
   
   📊 PERFORMANCE ANALYSIS
   -----------------------
   Total Ejecuciones: 121
   Tasa de Éxito: 29.8%
   
   ✓ Exportación completada en output/export_output/
