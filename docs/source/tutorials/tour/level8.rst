Nivel 8: demo_level8.py
=======================

Este es el nivel 8 del tour de aprendizaje.


.. thebe-button:: ACTIVAR MODO INTERACTIVO


Código Fuente
------------
.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level8.py
   :language: python
   :class: thebe


Resultado de Ejecución
----------------------
.. code-block:: text


   🖼️ Frame 0 | Danger: False
   [CONDITION] Evaluating: obstacle == True
   🛣️ Clear road. Accelerating... Data: {'_pipeline_start_time': '2026-04-28T08:50:06.496340', 'stream': <generator object simulate_video at 0x7977a9d65620>, '_loop_iteration': 0, 'progress_rich': <rich.progress.Progress object at 0x7977a9d45400>, 'current_frame': 0, 'obstacle': False}
   🖼️ Frame 1 | Danger: False
   [CONDITION] Evaluating: obstacle == True
   🛣️ Clear road. Accelerating... Data: {'_pipeline_start_time': '2026-04-28T08:50:06.496340', 'stream': <generator object simulate_video at 0x7977a9d65620>, '_loop_iteration': 1, 'progress_rich': <rich.progress.Progress object at 0x7977a9d45400>, 'current_frame': 1, 'obstacle': False, 'action': 'Accelerating'}
   🖼️ Frame 2 | Danger: False
   [CONDITION] Evaluating: obstacle == True
   🛣️ Clear road. Accelerating... Data: {'_pipeline_start_time': '2026-04-28T08:50:06.496340', 'stream': <generator object simulate_video at 0x7977a9d65620>, '_loop_iteration': 2, 'progress_rich': <rich.progress.Progress object at 0x7977a9d45400>, 'current_frame': 2, 'obstacle': False, 'action': 'Accelerating'}
   🖼️ Frame 3 | Danger: False
   [CONDITION] Evaluating: obstacle == True
   🛣️ Clear road. Accelerating... Data: {'_pipeline_start_time': '2026-04-28T08:50:06.496340', 'stream': <generator object simulate_video at 0x7977a9d65620>, '_loop_iteration': 3, 'progress_rich': <rich.progress.Progress object at 0x7977a9d45400>, 'current_frame': 3, 'obstacle': False, 'action': 'Accelerating'}
   🖼️ Frame 4 | Danger: True
   [CONDITION] Evaluating: obstacle == True
   🛑 EMERGENCY BRAKE ACTIVATED! Data: {'_pipeline_start_time': '2026-04-28T08:50:06.496340', 'stream': <generator object simulate_video at 0x7977a9d65620>, '_loop_iteration': 4, 'progress_rich': <rich.progress.Progress object at 0x7977a9d45400>, 'current_frame': 4, 'obstacle': True, 'action': 'Accelerating'}
   Trip_L8 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00