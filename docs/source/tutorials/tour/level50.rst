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


.. thebe-button:: ACTIVAR MODO INTERACTIVO


Código Fuente
------------
.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level50.py
   :language: python
   :class: thebe


Resultado de Ejecución
----------------------
.. code-block:: text


   Captured output.

.. raw:: html

    <div style='border:1px solid #00f2fe;padding:15px;text-align:center;border-radius:8px;margin-top:20px;'><h3>Misión 2 Superada</h3><a href='level51.html' style='color:#00f2fe;'>Siguiente Nivel</a></div>