Nivel 131: Background Tasks - Ejecución No Bloqueante
=====================================================

.. meta::
   :description: Aprende a ejecutar tareas en background sin bloquear el pipeline.
   :keywords: background, fire and forget, async, threading, wpipe

Objetivo
--------
Introducir el concepto de **Background Tasks** - tareas que se ejecutan en un hilo daemon sin bloquear la ejecución del pipeline principal.

Conceptos Clave
---------------
* **Fire & Forget**: Ejecutar tareas sin esperar a que terminen.
* **Daemon Threads**: Hilos que no bloquean la terminación del proceso.
* **No Blocking**: El pipeline continúa inmediatamente.

¿Qué estamos probando?
----------------------
Validamos que el pipeline pueda ejecutar tareas secundarias (logging, telemetría) sin esperar su finalización:

1. La tarea principal se ejecuta normalmente.
2. La tarea background se inicia en paralelo.
3. El pipeline continúa sin esperar.


.. thebe-button:: ACTIVAR MODO INTERACTIVO


Código Fuente
------------
.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level131.py
   :language: python
   :class: thebe


Resultado de Ejecución
----------------------
.. code-block:: text


   >>> DEMO 131: Background Task Básico
   ==================================================
   📌 Ejecutando tarea principal...
   🔄 [BACKGROUND] Iniciando tarea en segundo plano...
   ✅ Continuando con el siguiente paso...
   demo_131 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
   
   ⏱️ Tiempo total: 58ms
   ✅ El pipeline NO esperó 200ms del background!