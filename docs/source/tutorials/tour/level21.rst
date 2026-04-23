Nivel 21: demo_level21.py
=========================

Este es el nivel 21 del tour de aprendizaje.

Código Fuente
------------

.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level21.py
   :language: python
   :linenos:

Resultado de Ejecución
----------------------

.. code-block:: text

   >>> Test de seguridad: Comprobando que el radar no bloquee el sistema...
   📡 Radar: Escaneando entorno...
   
   [ERROR CAPTURE] Processing error in state 'radar_proximidad'...
   
   🚨 ALERTA CRÍTICA: El sensor 'radar_proximidad' no responde.
   🛑 ACCIÓN: Cambiando a modo de conducción manual.
   
   
   [ERROR] Step 'radar_proximidad' failed: [Error Code: 502] Task 'radar_proximidad' timed out after 0.2s
   Viaje_L21_Timeout - Processing pipeline tasks ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00

