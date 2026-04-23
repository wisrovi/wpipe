Best Practices for Industrial Pipelines
========================================

.. meta::
   :description: Professional engineering guidelines for building robust pipelines with wpipe v2.1.1-LTS.
   :keywords: best practices, engineering, guidelines, clean code, wpipe, industrial

Building a pipeline is easy. Building an **industrial-grade** pipeline that survives network failures, database locks, and evolving data schemas requires discipline. Follow these standards to ensure your **WPipe** implementations are world-class.

.. raw:: html

    <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 30px; border-radius: 12px; border-left: 8px solid #f59e0b; margin-bottom: 40px;">
       <h4 style="color: #f59e0b; margin-top: 0;">📜 The Golden Rule</h4>
       <p style="color: #94a3b8; margin-bottom: 0;">
           Every step must be <strong>Atomic, Idempotent, and Type-Safe</strong>. 
           If a pipeline fails and resumes, it should never corrupt your target data.
       </p>
    </div>

1. Step Architecture: Atomic & Pure
-----------------------------------

Each step should have a single responsibility. Avoid "Mega-steps" that handle fetching, cleaning, and saving in one go.

.. grid:: 1 1 2 2
    :gutter: 3

    .. grid-item-card:: ✅ GOOD: Atomic Steps
        :class-card: card-good

        .. code-block:: python

            def validate(data): ...
            def transform(data): ...
            def save(data): ...
            
            pipe.set_steps([validate, transform, save])

    .. grid-item-card:: ❌ BAD: The Mega-Step
        :class-card: card-bad

        .. code-block:: python

            def do_everything(data):
                raw = api.get()
                clean = clean(raw)
                db.save(clean)
                return {"ok": True}

2. Data Contract Management
---------------------------

The "Warehouse" model allows steps to access all previous data. This is powerful but dangerous if not governed.

**Guidelines:**
*   **Key Names**: Use unique, descriptive keys (e.g., ``user_metadata`` instead of ``data``).
*   **Immutability**: Avoid modifying keys created by previous steps unless explicitly required. Always add new keys.
*   **Type Hinting**: Use Python type hints to document the expected structure of the Warehouse.

.. code-block:: python

    from typing import Dict, Any

    def process_user(warehouse: Dict[str, Any]) -> Dict[str, Any]:
        """
        Expects: 'user_id' (str)
        Provides: 'user_email' (str), 'is_active' (bool)
        """
        user_id = warehouse.get("user_id")
        return {"user_email": "...", "is_active": True}

3. Resiliency & Failure Strategy
--------------------------------

Production pipelines **will** encounter transient failures. Use WPipe's built-in resiliency layer.

.. tab-set::

    .. tab-item:: Retries
        :sync: retry

        Use `@step` decorators to configure retries for unstable I/O tasks.
        
        .. code-block:: python

            @step(name="Fetch", retry_count=3, retry_delay=1.0)
            def fetch_unstable_api(data): ...

    .. tab-item:: Checkpoints
        :sync: checkpoint

        For long-running tasks (>10 min), add checkpoints at logical milestones.
        
        .. code-block:: python

            pipeline.add_checkpoint("phase_1_complete", "True")

    .. tab-item:: Deadlines
        :sync: timeout

        Always enforce timeouts on external network calls.
        
        .. code-block:: python

            @timeout_sync(seconds=30)
            def call_slow_service(data): ...

4. Performance & Scalability
----------------------------

Don't wait for things you can do in parallel.

*   **IO-Bound**: Use `Parallel` for API calls or database operations.
*   **CPU-Bound**: Use `use_processes=True` for heavy math or AI tasks to bypass the GIL.
*   **Batching**: If processing millions of rows, process in chunks within a `For` loop to manage memory.

5. Monitoring & Governance
--------------------------

*   **Tracking DB**: Always provide a `tracking_db` path for production runs.
*   **Resource Probing**: Enable `collect_system_metrics=True` for high-load pipelines to detect memory leaks.
*   **Dashboard**: Use the Dashboard visualizer during development to debug complex DAGs.

.. raw:: html

    <style>
        .card-good { border-left: 5px solid #10b981 !important; }
        .card-bad { border-left: 5px solid #ef4444 !important; }
    </style>
