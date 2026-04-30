Nivel 15: demo_level15.py
=========================

Este es el nivel 15 del tour de aprendizaje.


.. thebe-button:: ACTIVAR MODO INTERACTIVO


Código Fuente
-------------
.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level15.py
   :language: python
   :class: thebe


Resultado de Ejecución
----------------------
----------------------


   >>> Can we resume previous trip? False
   🏠 Leaving home (Step already done in the past)...
   💥 ELECTRICAL BREAKDOWN! The system is shutting down.
   trip_l15_recovery ━━━━━━━━━━━━━━━━━━━━                      50% -:--:--
   Traceback (most recent call last):
     File "/home/william.rodriguez/miniconda3/lib/python3.13/site-packages/wpipe/pipe/pipe.py", line 708, in _task_invoke
       result = _run()
     File "/home/william.rodriguez/miniconda3/lib/python3.13/site-packages/wpipe/pipe/pipe.py", line 701, in _run
       return func(*args, **kwargs)
     File "/home/william.rodriguez/miniconda3/lib/python3.13/site-packages/wpipe/decorators/step.py", line 209, in wrapper
       return func(*args, **kwargs)
     File "/home/william.rodriguez/Documents/wpipe/examples/00_honey_pot/03_yield/demo_level15.py", line 47, in critical_phase
       raise RuntimeError("Battery failure")
   RuntimeError: Battery failure
   
   The above exception was the direct cause of the following exception:
   
   Traceback (most recent call last):
     File "/home/william.rodriguez/miniconda3/lib/python3.13/site-packages/wpipe/pipe/pipe.py", line 459, in _pipeline_run_with_report
       result = self._pipeline_run(*args, **kwargs)
     File "/home/william.rodriguez/miniconda3/lib/python3.13/site-packages/wpipe/pipe/pipe.py", line 1290, in _pipeline_run
       data, error_msg, error_step = self._execute_all_pipeline_steps(
                                     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
           data, start_at_step, progress_bar_gen, total_steps,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
           checkpoint_mgr, checkpoint_id, step_kwargs
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
       )
       ^
     File "/home/william.rodriguez/miniconda3/lib/python3.13/site-packages/wpipe/pipe/pipe.py", line 1200, in _execute_all_pipeline_steps
       data = self._execute_step(item, data, **step_kwargs)
     File "/home/william.rodriguez/miniconda3/lib/python3.13/site-packages/wpipe/pipe/pipe.py", line 801, in _execute_step
       return self._execute_task_step(item, data, parent_step_id, parallel_group, **kwargs)
              ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
     File "/home/william.rodriguez/miniconda3/lib/python3.13/site-packages/wpipe/pipe/pipe.py", line 967, in _execute_task_step
       result_data = self._task_invoke(func, name, data, __step_meta__=step_meta, **kwargs)
     File "/home/william.rodriguez/miniconda3/lib/python3.13/site-packages/wpipe/pipe/pipe.py", line 747, in _task_invoke
       raise TaskError(str(e), Codes.TASK_FAILED) from e
   wpipe.exception.api_error.TaskError: [Error Code: 502] Battery failure
   
   The above exception was the direct cause of the following exception:
   
   Traceback (most recent call last):
     File "/home/william.rodriguez/Documents/wpipe/examples/00_honey_pot/03_yield/demo_level15.py", line 60, in <module>
       pipe.run({}, checkpoint_mgr=ck_mgr, checkpoint_id=session)
       ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
     File "/home/william.rodriguez/miniconda3/lib/python3.13/site-packages/wpipe/pipe/pipe.py", line 1327, in run
       result = self._pipeline_run_with_report(*args, **kwargs)
     File "/home/william.rodriguez/miniconda3/lib/python3.13/site-packages/wpipe/pipe/pipe.py", line 477, in _pipeline_run_with_report
       raise ProcessError(str(te), Codes.TASK_FAILED) from te
   wpipe.exception.api_error.ProcessError: [Error Code: 502] Battery failure