Nivel 100: Auditoría de Seguridad (Alerts History)
======================================================

.. meta::
   :description: Gestión y consulta del historial de alertas disparadas en WPipe.
   :keywords: alerts, history, audit, monitoring, database, wpipe

Objetivo
--------
Aprender a auditar el comportamiento del sistema a través del tiempo. Verás cómo consultar el historial completo de alertas disparadas, incluso desde diferentes instancias de pipelines que comparten la misma base de datos de seguimiento.

Conceptos Clave
---------------
* **Persistencia de Alertas**: Las alertas no solo se disparan en consola; se guardan con metadatos completos en SQLite.
* **Tracker Querying**: Uso de `get_fired_alerts()` para extraer inteligencia operacional.
* **Correlación de Eventos**: Cómo múltiples ejecuciones (L100 y L100b) contribuyen a un historial común de salud del sistema.

¿Qué estamos probando?
----------------------
Estamos probando la capacidad de "memoria" del motor. Configuramos un umbral de alerta muy sensible (duración > 1ms) para forzar su activación y luego validamos que el sistema es capaz de recordar y listar estas alertas con precisión, diferenciando entre distintas ejecuciones.

Código Fuente
------------

.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level100.py
   :language: python
   :linenos:

Análisis de la Ejecución
------------------------

1. Se configura el `tracking_db` en una ubicación común (`output/alerts100.db`).
2. Se define una alerta crítica sobre la duración total del pipeline.
3. Se ejecutan dos pipelines distintos.
4. Se invoca el historial de alertas, lo que devuelve una lista de diccionarios con el `timestamp`, el `mensaje` y la `severidad` de cada incidencia detectada.

Resultado de Ejecución
----------------------

.. code-block:: text

   >>> Alerts history...
   viaje_l100_history - Processing pipeline tasks ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
   
   >>> Running second pipeline...
   
   🚨 Total in history: 2
   (Cada ejecución disparó una alerta de rendimiento)
