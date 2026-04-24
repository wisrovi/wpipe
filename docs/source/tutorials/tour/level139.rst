Nivel 139: Background sin capture_error (Default)
=================================================

.. meta::
   :description: Por defecto capture_error=False, errores son silenciados.
   :keywords: background, silent, wpipe

Objetivo
--------
Confirmar el comportamiento por defecto: errores en background son ignorados silenciosamente.

Código Fuente
-------------

.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level139.py
   :language: python
   :linenos:

Key Takeaway
------------
`Background(task)` es equivalente a `Background(task, capture_error=False)` - los errores se ignoran.