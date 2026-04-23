Nivel 1: Conceptos Básicos de Pipeline
======================================

.. meta::
   :description: Fundamentos de WPipe: Creación de tu primer pipeline.
   :keywords: pipeline, setup, beginner, tutorial, wpipe

Objetivo
--------
Aprender a instanciar el motor de orquestación de **WPipe** y ejecutar una tarea atómica para verificar que el sistema está correctamente instalado y configurado.

Conceptos Clave
---------------
* **Instanciación**: Creación del objeto `Pipeline`.
* **Verbose Mode**: Uso del flag `verbose=True` para ver el progreso detallado en consola.
* **Flujo de Trabajo**: Registro de funciones simples como pasos del pipeline.

¿Qué estamos probando?
----------------------
En este nivel validamos la conectividad básica del motor. Estamos probando que una función estándar de Python pueda ser inyectada en el orquestador, ejecutada sin errores y que el sistema sea capaz de mostrar la barra de progreso de `Rich`.

Código Fuente
------------

.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level1.py
   :language: python
   :linenos:

Análisis de la Ejecución
------------------------

Al ejecutar este código, el orquestador:
1. Registra la función `girar_llave` en la cola de ejecución.
2. Inicia un nuevo contexto de datos vacío `{}`.
3. Muestra una barra de progreso indicando el estado de la tarea.
4. Imprime el log interno de la función.

Resultado de Ejecución
----------------------

.. code-block:: text

   🔑 Girando llave: Motor encendido.
   Viaje_L1 - Processing pipeline tasks ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
