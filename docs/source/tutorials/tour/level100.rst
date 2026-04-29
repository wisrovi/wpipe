Nivel 100: Auditoría de Seguridad (Alerts History)
==================================================

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


.. thebe-button:: ACTIVAR MODO INTERACTIVO


Código Fuente
------------
.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level100.py
   :language: python
   :class: thebe


Resultado de Ejecución
----------------------
.. code-block:: text


   >>> Alerts history...
   [PIPELINE STATUS] Registered: PIPE-884B6C3F
   viaje_l100_history ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
   [PIPELINE STATUS] PIPE-884B6C3F: COMPLETED
   >>> Running second pipeline...
   viaje_l100_history ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
   viaje_l100b        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
   
   🚨 Total in history: 50