Nivel 135: Background para Logging/Telemetría
=============================================

.. meta::
   :description: Caso de uso práctico: logging sin bloquear.
   :keywords: background, logging, telemetry, wpipe

Objetivo
--------
Demostrar el caso de uso más común: enviar logs/telemetría sin impactar el performance.


.. thebe-button:: ACTIVAR MODO INTERACTIVO


Código Fuente
------------
.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level135.py
   :language: python
   :class: thebe


Resultado de Ejecución
----------------------
.. code-block:: text


   >>> DEMO 135: Background para Logging/Telemetría
   ==================================================
   📊 Procesando datos...
   📡 [TELEMETRY] Enviando métricas a servidor...
   💾 Guardando resultado...
   demo_135 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
   
   ⏱️ Pipeline: 8ms
   💡 La telemetría se envió SIN bloquear el pipeline!