Nivel 8: demo_level8.py
=======================

Este es el nivel 8 del tour de aprendizaje.


.. thebe-button:: ACTIVAR MODO INTERACTIVO


Código Fuente
-------------
.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level8.py
   :language: python
   :class: thebe


Resultado de Ejecución
----------------------
----------------------


   🖼️ Frame 0 | Danger: True
   [CONDITION] Evaluating: obstacle == True
   🛑 EMERGENCY BRAKE ACTIVATED! Data: {'_pipeline_start_time': '2026-04-30T13:36:32.231285', 'stream': <generator object simulate_video at 0x72efe6a249e0>, '_loop_iteration': 0, 'progress_rich': <rich.progress.Progress object at 0x72efe6a28c20>, 'current_frame': 0, 'obstacle': True}
   🖼️ Frame 1 | Danger: False
   [CONDITION] Evaluating: obstacle == True
   🛣️ Clear road. Accelerating... Data: {'_pipeline_start_time': '2026-04-30T13:36:32.231285', 'stream': <generator object simulate_video at 0x72efe6a249e0>, '_loop_iteration': 1, 'progress_rich': <rich.progress.Progress object at 0x72efe6a28c20>, 'current_frame': 1, 'obstacle': False, 'action': 'Braking'}
   🖼️ Frame 2 | Danger: False
   [CONDITION] Evaluating: obstacle == True
   🛣️ Clear road. Accelerating... Data: {'_pipeline_start_time': '2026-04-30T13:36:32.231285', 'stream': <generator object simulate_video at 0x72efe6a249e0>, '_loop_iteration': 2, 'progress_rich': <rich.progress.Progress object at 0x72efe6a28c20>, 'current_frame': 2, 'obstacle': False, 'action': 'Accelerating'}
   🖼️ Frame 3 | Danger: True
   [CONDITION] Evaluating: obstacle == True
   🛑 EMERGENCY BRAKE ACTIVATED! Data: {'_pipeline_start_time': '2026-04-30T13:36:32.231285', 'stream': <generator object simulate_video at 0x72efe6a249e0>, '_loop_iteration': 3, 'progress_rich': <rich.progress.Progress object at 0x72efe6a28c20>, 'current_frame': 3, 'obstacle': True, 'action': 'Accelerating'}
   🖼️ Frame 4 | Danger: True
   [CONDITION] Evaluating: obstacle == True
   🛑 EMERGENCY BRAKE ACTIVATED! Data: {'_pipeline_start_time': '2026-04-30T13:36:32.231285', 'stream': <generator object simulate_video at 0x72efe6a249e0>, '_loop_iteration': 4, 'progress_rich': <rich.progress.Progress object at 0x72efe6a28c20>, 'current_frame': 4, 'obstacle': True, 'action': 'Braking'}
   Trip_L8 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00