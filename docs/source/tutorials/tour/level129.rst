Nivel 129: demo_level129.py
===========================

Este es el nivel 129 del tour de aprendizaje.


.. thebe-button:: ACTIVAR MODO INTERACTIVO


Código Fuente
------------
.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level129.py
   :language: python
   :class: thebe


Resultado de Ejecución
----------------------
.. code-block:: text


   >>> API error handling...
   ⚠️ Intentando conexión...
   ✅ Sistema tolerante a errores
   Error in GET request to https://nonexistent.example.com/test: HTTPSConnectionPool(host='nonexistent.example.com', port=443): Max retries exceeded with url: /test (Caused by NameResolutionError("HTTPSConnection(host='nonexistent.example.com', port=443): Failed to resolve 'nonexistent.example.com' ([Errno -5] No address associated with hostname)"))