Nivel 61: demo_level61.py
=========================

Este es el nivel 61 del tour de aprendizaje.

Código Fuente
------------

.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level61.py
   :language: python
   :linenos:

Resultado de Ejecución
----------------------

.. code-block:: text

   
   >>> Probando retry a nivel de Pipeline...
   
   [RETRY] conectar_api failed (attempt 1/4): API no disponible
   [RETRY] conectar_api failed (attempt 2/4): API no disponible
   [RETRY] conectar_api failed (attempt 3/4): API no disponible
   
   [ERROR] Step 'conectar_api' failed: [Error Code: 502] API no disponible
   Viaje_L61_PipelineRetry - Processing pipeline tasks                                            0% -:--:--
   Traceback (most recent call last):
     File "/home/wisrovi/Documentos/w_libraries/wpipe/wpipe/wpipe/pipe/pipe.py", line 945, in _task_invoke
       result = _run()
     File "/home/wisrovi/Documentos/w_libraries/wpipe/wpipe/wpipe/pipe/pipe.py", line 933, in _run
       return func(*args, **kwargs)
     File "/home/wisrovi/Documentos/w_libraries/wpipe/wpipe/wpipe/decorators/step.py", line 147, in wrapper
       return func(*args, **kwargs)
     File "/home/wisrovi/Documentos/w_libraries/wpipe/wpipe/examples/00_honey_pot/03_yield/demo_level61.py", line 24, in conectar_api
       raise ConnectionError("API no disponible")
   ConnectionError: API no disponible
   
   The above exception was the direct cause of the following exception:
   
   Traceback (most recent call last):
     File "/home/wisrovi/Documentos/w_libraries/wpipe/wpipe/wpipe/pipe/pipe.py", line 682, in _pipeline_run_with_report
       result = self._pipeline_run(*args, **kwargs)
     File "/home/wisrovi/Documentos/w_libraries/wpipe/wpipe/wpipe/pipe/pipe.py", line 1470, in _pipeline_run
       data = self._execute_step(item, data, **step_kwargs)
     File "/home/wisrovi/Documentos/w_libraries/wpipe/wpipe/wpipe/pipe/pipe.py", line 1222, in _execute_step
       result_data = self._task_invoke(func, name, *(data,), **current_kwargs)
     File "/home/wisrovi/Documentos/w_libraries/wpipe/wpipe/wpipe/pipe/pipe.py", line 984, in _task_invoke
       raise TaskError(str(e), Codes.TASK_FAILED) from e
   wpipe.exception.api_error.TaskError: [Error Code: 502] API no disponible
   
   The above exception was the direct cause of the following exception:
   
   Traceback (most recent call last):
     File "/home/wisrovi/Documentos/w_libraries/wpipe/wpipe/examples/00_honey_pot/03_yield/demo_level61.py", line 44, in <module>
       pipe.run({})
       ~~~~~~~~^^^^
     File "/home/wisrovi/Documentos/w_libraries/wpipe/wpipe/wpipe/pipe/pipe.py", line 1562, in run
       return self._pipeline_run_with_report(*args, **kwargs)
              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
     File "/home/wisrovi/Documentos/w_libraries/wpipe/wpipe/wpipe/pipe/pipe.py", line 707, in _pipeline_run_with_report
       raise ProcessError(str(te), Codes.TASK_FAILED) from te
   wpipe.exception.api_error.ProcessError: [Error Code: 502] API no disponible

