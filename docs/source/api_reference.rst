API Technical Specification
===========================

.. meta::
   :description: Complete technical reference for WPipe v2.1.1-LTS. Detailed classes, methods, and decorators.
   :keywords: api, reference, technical, documentation, wpipe, classes

This is the exhaustive technical specification for the **WPipe v2.1.1-LTS** engine. Designed for precision and reliability.

.. raw:: html

    <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 25px; border-radius: 12px; border-left: 5px solid #00f2fe; margin-bottom: 40px;">
        <h4 style="color: #00f2fe; margin-top: 0;">🛠️ Engineering Standard</h4>
        <p style="color: #94a3b8; margin-bottom: 0; font-size: 0.95em;">
            All public APIs adhere to <strong>Semantic Versioning 2.0.0</strong>. 
            Method signatures are type-hinted and documented following the Google Python Style Guide.
        </p>
    </div>

1. Core Orchestration
---------------------

.. card:: class wpipe.Pipeline
    :shadow: md

    The primary synchronization engine. It coordinates step execution and context management.

    **Constructor:**
    ``Pipeline(pipeline_name: str, verbose: bool = False, tracking_db: str = None, ...)``

    **Key Methods:**
    *   ``.set_steps(steps: List)``: Registers the execution chain.
    *   ``.run(initial_data: Dict) -> Dict``: Triggers the orchestration.
    *   ``.add_checkpoint(name: str, expression: str)``: Gated state persistence.

.. card:: class wpipe.PipelineAsync
    :shadow: md

    The high-concurrency variant of the engine. Fully compatible with ``asyncio``.

    **Usage:**
    .. code-block:: python

        result = await pipe_async.run(data)

2. Logical Control Blocks
-------------------------

.. grid:: 1 1 3 3
    :gutter: 2

    .. grid-item-card:: Condition
        
        Ramificación lógica.
        ^^^
        ``Condition(expression, branch_true, branch_false)``

    .. grid-item-card:: For
        
        Bucles controlados.
        ^^^
        ``For(iterations, validation_expression, steps)``

    .. grid-item-card:: Parallel
        
        Multi-executor block.
        ^^^
        ``Parallel(steps, max_workers, use_processes)``

3. Decorators & Intelligence
----------------------------

.. card:: @wpipe.step
    :shadow: sm

    The universal task decorator. Injects metadata and resiliency settings into pure functions.

    **Parameters:**
    *   ``name``: Logical identifier for the Dashboard.
    *   ``version``: Version tag for CI/CD tracking.
    *   ``retry_count``: Number of automatic recovery attempts.
    *   ``timeout``: Execution deadline in seconds.

.. card:: class wpipe.AutoRegister
    :shadow: sm

    Helper for large projects. Automatically discovers and registers all ``@step`` functions in a module.

4. Persistence (WSQLite)
------------------------

.. grid:: 1 1 2 2
    :gutter: 3

    .. grid-item-card:: 🗄️ Wsqlite (Context Wrapper)
        
        The recommended high-level API for data persistence.
        ^^^
        .. code-block:: python

            with Wsqlite(db_name="data.db") as db:
                db.input = ...
                db.output = ...

    .. grid-item-card:: ⚙️ SQLite (Core Engine)
        
        The low-level driver optimized with WAL mode and thread-safe connection pooling.

5. Industrial Observability
---------------------------

.. card:: class wpipe.ResourceMonitor
    :shadow: md

    Real-time system probe. Measures CPU load and RSS Memory without blocking the main event loop.

    **Methods:**
    *   ``.get_summary()``: Returns peak and average metrics.

.. card:: class wpipe.PipelineExporter
    :shadow: md

    Data bridge for external analysis.
    
    *   ``.export_pipeline_logs(format="json|csv")``
    *   ``.export_statistics()``

6. Error Architecture
---------------------

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Exception
     - Context
   * - ``TaskError``
     - Generic failure in a step. Contains forensic metadata.
   * - ``ProcessError``
     - Orchestration-level failure.
   * - ``ApiError``
     - Failure communicating with the API/Dashboard.
   * - ``Codes``
     - Constants for standardized error reporting (500-505).

7. Technical Utilities
----------------------

*   ``leer_yaml / escribir_yaml``: Thread-safe YAML IO with environment variable support.
*   ``new_logger``: Loguru configuration for industrial rotation and retention.
*   ``memory_limit``: Linux-specific memory cgroup control.

----

**Looking for the full Python Auto-Docs?**
Visit the :doc:`user_guide/index` or inspect the docstrings directly in the source code.
