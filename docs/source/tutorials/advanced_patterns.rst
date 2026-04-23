Advanced Patterns Tutorial
============================

Learn advanced patterns for complex pipeline scenarios using WPipe v2.1.0 features.

.. contents::
   :local:
   :depth: 2

1. Native Parallel Execution
----------------------------

WPipe provides a native ``Parallel`` block that handles concurrency automatically, supporting both threads and processes.

1.1 Using Parallel Blocks
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe import Pipeline, Parallel

    pipeline = Pipeline()
    pipeline.set_steps([
        Parallel(
            steps=[task_a, task_b, task_c],
            max_workers=3,
            use_processes=False # Set to True for CPU-bound tasks
        )
    ])

1.2 Parallel Properties
~~~~~~~~~~~~~~~~~~~~~~~

- **Resolution**: Results from all parallel tasks are merged back into the main context.
- **Safety**: Each task receives a copy of the context to avoid race conditions.
- **Flexibility**: You can mix ``Parallel`` blocks with ``For`` loops and ``Condition`` branches.

2. Intelligent Checkpoints
--------------------------

Checkpoints allow your pipeline to resume execution from a specific milestone after a system failure.

2.1 Defining Checkpoints
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe import Pipeline

    pipeline = Pipeline()
    
    # Milestone that triggers when a specific data condition is met
    pipeline.add_checkpoint(
        checkpoint_name="data_ready",
        expression="count > 100",
        steps=[notify_admin] # Optional steps to run when reached
    )

2.2 Logic Flow
~~~~~~~~~~~~~~

- **Persistence**: Checkpoints are stored in the tracking database via WSQLite.
- **Auto-Resume**: When running a pipeline with a ``checkpoint_id``, WPipe automatically skips already completed milestones.

3. Forensic Error Capture
-------------------------

Gain deep insights into failures with high-resolution error reporting.

3.1 Adding Error Handlers
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def telegram_alert(context, error):
        print(f"Error in {error['step_name']} at line {error['line_number']}")
        return context

    pipeline = Pipeline()
    pipeline.add_error_capture([telegram_alert])

3.2 Captured Metadata
~~~~~~~~~~~~~~~~~~~~~

The error handler receives a dictionary with:
- ``step_name``: Name of the failed task.
- ``file_path``: Absolute path to the source file.
- ``line_number``: Exact line where the exception occurred.
- ``error_message``: The exception string.
- ``timestamp``: When the error happened.

4. High-Performance Monitoring
------------------------------

WPipe v2.1.0 features a non-blocking ``ResourceMonitor`` using WAL mode for SQLite.

.. code-block:: python

    from wpipe import ResourceMonitor

    with ResourceMonitor("HeavyTask") as monitor:
        # Perform computation
        pass
    
    summary = monitor.get_summary()
    print(f"Peak RAM: {summary['peak_ram_mb']} MB")

5. Best Practices
-----------------

- Use **Threads** for I/O bound tasks (API calls, DB writes).
- Use **Processes** for CPU-bound tasks (Data processing, Image manipulation).
- Always define **PipelineContext** for strict data contracts in production.

6. Next Steps
-------------

- :doc:`production_deployment` - Deploy to production
- :doc:`api_integration` - Advanced API tracking
