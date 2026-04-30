Nivel 139: Background sin capture_error (Default)
=================================================

.. meta::
   :description: Por defecto capture_error=False, errores son silenciados.
   :keywords: background, silent, wpipe

Objetivo
--------
Confirmar el comportamiento por defecto: errores en background son ignorados silenciosamente.


.. thebe-button:: ACTIVAR MODO INTERACTIVO


Código Fuente
-------------
.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level139.py
   :language: python
   :class: thebe


Resultado de Ejecución
----------------------
----------------------


   >>> DEMO 139: Background sin capture_error
   ==================================================
   📌 Iniciando...
   🔄 [BACKGROUND] Tarea que fallará (sin capture)...
   ✅ Pipeline continúa (error ignorado)...
   demo_139 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
   
   ✅ El error fue ignorado (silent fail)!