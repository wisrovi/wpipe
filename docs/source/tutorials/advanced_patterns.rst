Advanced Patterns Tutorial
============================

.. meta::
   :description: Advanced design patterns for complex pipeline architectures.
   :keywords: design patterns, advanced, parallel, monitor, wpipe

Learn advanced design patterns for complex pipeline scenarios using **WPipe v2.1.1** high-end features. This tutorial is intended for senior developers building distributed systems or high-throughput data processing engines.

.. contents::
   :local:
   :depth: 2

1. DAG Scheduling (Directed Acyclic Graphs)
------------------------------------------

When your tasks don't follow a linear sequence, you need a **DAG Scheduler**. WPipe allows you to define dependencies between steps, and the engine will automatically calculate the execution order.

**Pattern: Dependency-Based Execution**

.. code-block:: python

    from wpipe.parallel import ParallelExecutor, ExecutionMode

    executor = ParallelExecutor(max_workers=4)

    # Define steps with explicit dependencies
    executor.add_step("fetch", fetch_data, mode=ExecutionMode.IO_BOUND)
    executor.add_step("clean", clean_data, depends_on=["fetch"])
    executor.add_step("analyze", analyze_data, depends_on=["clean"])
    executor.add_step("report", generate_report, depends_on=["analyze"])

    result = executor.execute({})

**Why use this?**
- **Horizontal Scaling**: Independent branches run in parallel automatically.
- **Complexity Management**: Visually map your workflow as a graph.

2. Native Parallelism (IO vs CPU)
---------------------------------

WPipe differentiates between tasks that wait for external resources (IO) and tasks that consume CPU.

*   **ThreadPoolExecutor (IO-Bound)**: Best for API calls, database queries, and file operations.
*   **ProcessPoolExecutor (CPU-Bound)**: Best for heavy calculations, image processing, or data transformations that bypass the Python GIL.

.. code-block:: python

    from wpipe import Parallel

    pipeline.set_steps([
        Parallel(
            steps=[heavy_math_1, heavy_math_2],
            use_processes=True,  # Full GIL bypass
            max_workers=2
        )
    ])

3. Forensic Error Capture
-------------------------

Standard logging often misses the context of a failure. WPipe's forensic capture provides the exact state of the warehouse at the moment of impact.

.. code-block:: python

    def alert_handler(context, error):
        print(f"FAILED: {error['step_name']} at line {error['line_number']}")
        # send to slack/telegram/email

    pipeline.add_error_capture([alert_handler])

**Metadata available in error object:**
- ``step_name``: The failing task.
- ``error_message``: The exception string.
- ``file_path``: Exact location in source code.
- ``line_number``: Where it happened.
- ``timestamp``: When the error happened.

4. High-Performance Monitoring
------------------------------

WPipe v2.1.1 features a non-blocking ``ResourceMonitor`` using **WAL (Write-Ahead Logging)** mode for SQLite. This allows you to track system health without slowing down the primary processing.

.. code-block:: python

    from wpipe import ResourceMonitor

    with ResourceMonitor("Heavy_Process") as monitor:
        pipeline.run(large_dataset)
        
    stats = monitor.get_summary()
    print(f"Peak Memory: {stats['peak_ram_mb']} MB")

**Key metrics captured:**
- **RSS RAM**: Real memory usage of the process.
- **CPU %**: Core utilization (normalized for multi-core).
- **Disk IO**: Read/Write intensity.

5. Dynamic Pipeline Composition
-------------------------------

Treat pipelines as first-class citizens. You can nest pipelines within pipelines to create recursive or modular architectures.

.. code-block:: python

    sub_pipe = Pipeline(pipeline_name="Worker")
    sub_pipe.set_steps([validate, transform])

    main_pipe = Pipeline(pipeline_name="Master")
    main_pipe.set_steps([
        fetch_raw,
        sub_pipe,  # Nested execution
        save_final
    ])

**Benefits:**
- **Encapsulation**: Hide complexity inside sub-pipelines.
- **Reusability**: Use the same sub-pipeline in multiple projects.
