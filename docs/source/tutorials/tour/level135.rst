Nivel 135: Background para Logging/Telemetría
=============================================

.. meta::
   :description: Caso de uso práctico: logging sin bloquear.
   :keywords: background, logging, telemetry, wpipe

Objetivo
--------
Demostrar el caso de uso más común: enviar logs/telemetría sin impactar el performance.

Código Fuente
-------------

.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level135.py
   :language: python
   :linenos:

Key Takeaway
------------
Perfecto para enviar métricas a sistemas externos sin afectar el tiempo de respuesta del pipeline.