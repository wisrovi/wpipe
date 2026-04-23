System Architecture: The WPipe Engine
========================================

.. meta::
   :description: Architectural deep dive into wpipe v2.1.1-LTS. Learn about the Warehouse model, WSQLite persistence, and parallel execution.
   :keywords: architecture, design, internal, data flow, persistence, parallel

This document details the internal design and engineering philosophy behind **wpipe v2.1.1-LTS**. Our goal is to provide a zero-boilerplate orchestration engine that remains robust under industrial loads.

.. raw:: html

    <div style="background: rgba(0, 242, 254, 0.05); padding: 30px; border-radius: 12px; border: 1px solid rgba(0, 242, 254, 0.2); margin-bottom: 40px;">
        <h3 style="color: #00f2fe; margin-top: 0;">Philosophy: "Code is the Config"</h3>
        <p style="color: #94a3b8; margin-bottom: 0;">
            Unlike XML or YAML-heavy orchestrators, WPipe treats your Python code as the source of truth. 
            We provide a thin but powerful layer of resiliency and observability over pure logic.
        </p>
    </div>

1. The "Warehouse" Model
-----------------------

The core mental model of WPipe is the **Warehouse**. 

*   **Accumulation**: Instead of steps passing specific arguments to each other, every step updates a global "Warehouse" dictionary.
*   **Context Awareness**: Every task has visibility into all previous results, allowing for complex decision-making without complex parameter passing.
*   **Atomic Updates**: WPipe ensures that context updates are merged safely, even in high-concurrency scenarios.

.. image:: https://raw.githubusercontent.com/wisrovi/wpipe/main/images.jpeg
   :width: 600
   :align: center
   :alt: WPipe Architecture Diagram

2. Core Internal Layers
-----------------------

WPipe is structured into four specialized layers:

.. grid:: 1 1 2 2
    :gutter: 3

    .. grid-item-card:: 🧠 Orchestration Layer
        :padding: 2

        The `Pipeline` and `PipelineAsync` engines. They manage the DAG execution, handle step registration, and coordinate the flow between components.

    .. grid-item-card:: 💾 Persistence Layer (WSQLite)
        :padding: 2

        A unified abstraction over SQLite that forces **WAL (Write-Ahead Logging)** mode. This ensures that tracking logs and metrics never block your primary data tasks.

    .. grid-item-card:: 📊 Observability Layer
        :padding: 2

        Includes the `ResourceMonitor` (CPU/RAM tracking) and the `PipelineTracker`. It captures performance data and forensic error details.

    .. grid-item-card:: 🌐 Integration Layer
        :padding: 2

        The `APIClient` and `Dashboard`. It allows pipelines to communicate with central command centers and provides real-time visual feedback.

3. Persistence Strategy: WSQLite
-------------------------------

One of the most critical components of v2.1.1-LTS is the **WSQLite unification**. 

*   **Zero Raw SQL**: All internal tracking (logs, steps, metrics) is handled through Pydantic-mapped models.
*   **Thread Safety**: Connection pooling and locking mechanisms are built-in to prevent `Database is locked` errors during parallel execution.
*   **WAL Mode**: Mandatory Write-Ahead Logging allows simultaneous reads (Dashboard) and writes (Pipeline) with zero latency.

4. Resiliency & Reliability
---------------------------

WPipe is "Resilient by Design". This is achieved through two main features:

4.1 Smart Checkpointing
~~~~~~~~~~~~~~~~~~~~~~~
Checkpoints are not just periodic saves. They are **logic-gated milestones**. You can define a checkpoint that only triggers if a specific data validation passes, ensuring you never save a "corrupt" state.

4.2 Forensic Error Capture
~~~~~~~~~~~~~~~~~~~~~~~~~
When a step fails, the `LogGestor` captures:
*   The exact state of the Warehouse.
*   The file path and line number of the exception.
*   The system metrics (RAM/CPU) at the moment of failure.

5. Concurrency Model
--------------------

WPipe provides a dual-executor model to bypass the limitations of Python:

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Executor
     - Backend
     - Best for
   * - **IO-Bound**
     - `ThreadPoolExecutor`
     - API calls, DB queries, Web scraping.
   * - **CPU-Bound**
     - `ProcessPoolExecutor`
     - Image processing, AI inference, Heavy math.
   * - **Async**
     - `asyncio` loop
     - High-concurrency network tasks.

6. Module Hierarchy
-------------------

.. code-block:: text

    wpipe/
    ├── pipe/               # Core Engine (Sync/Async/DAG)
    ├── parallel/           # Concurrency Executors
    ├── sqlite/             # WSQLite Unification
    ├── tracking/           # Metrics & Alerts
    ├── resource_monitor/   # CPU/RAM Probing
    ├── checkpoint/         # Resiliency Logic
    └── dashboard/          # Visual Intelligence

Next Steps
----------

*   See :doc:`best_practices` to implement this architecture correctly.
*   Explore :doc:`api_reference` for the technical specifications of each module.
