Nivel 62: demo_level62.py
=========================

Este es el nivel 62 del tour de aprendizaje.


.. thebe-button:: ACTIVAR MODO INTERACTIVO


Código Fuente
------------
.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level62.py
   :language: python
   :class: thebe


Resultado de Ejecución
----------------------
.. code-block:: text


   
   >>> Probando callback de excepciones...
   
   
   [ERROR CAPTURE] Processing error in state 'operacion_peligrosa'...
   🔴 [CALLBACK] Error capturado: Operación falló
   📧 Enviando notificación...
   [RETRY] operacion_peligrosa failed (attempt 1): Operación falló
   
   [ERROR CAPTURE] Processing error in state 'operacion_peligrosa'...
   🔴 [CALLBACK] Error capturado: Operación falló
   📧 Enviando notificación...
   [RETRY] operacion_peligrosa failed (attempt 2): Operación falló
   ✅ Operación completada
   viaje_l62_onexception ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00