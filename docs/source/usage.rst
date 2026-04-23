Mastering |wpipe|: Usage Guide
==================================

.. meta::
   :description: Comprehensive usage guide for wpipe v2.1.1-LTS. From basic functions to complex enterprise patterns.
   :keywords: usage, examples, advanced, patterns, orchestration, python

This guide provides deep-dive examples for every capability of the **WPipe v2.1.1-LTS** engine. Use the tabs below to navigate through different complexity levels.

.. raw:: html

    <div style="margin-bottom: 30px;">
        <p style="font-size: 1.1em; color: #94a3b8;">
            All examples assume you have performed a standard installation: <code>pip install wpipe</code>.
        </p>
    </div>

1. Fundamental Step Types
-------------------------

WPipe is extremely flexible. You can define steps using any Python callable.

.. tab-set::

    .. tab-item:: Pure Functions
        :sync: func

        The most common way to build pipelines. Clean, testable, and simple.

        .. code-block:: python

            def transform(data):
                # 'data' contains everything from previous steps
                return {"cleaned": data["raw"].strip()}

    .. tab-item:: Class Instances
        :sync: class

        Ideal for stateful operations or when you need initialization parameters.

        .. code-block:: python

            class Multiplier:
                def __init__(self, factor):
                    self.factor = factor
                
                def __call__(self, data):
                    return {"result": data["value"] * self.factor}

            pipe.set_steps([ (Multiplier(10), "Scale", "v1.0") ])

    .. tab-item:: Lambdas
        :sync: lambda

        Perfect for quick, one-liner data mapping.

        .. code-block:: python

            pipe.set_steps([
                (lambda d: {"id": d["id"].upper()}, "UpperID", "v1.0")
            ])

2. Advanced Control Flow
------------------------

Beyond linear sequences, WPipe supports complex logical structures.

.. grid:: 1 1 2 2
    :gutter: 3

    .. grid-item-card:: 🌳 Conditional Branching
        :padding: 2

        Execute different paths based on runtime data.
        ^^^
        .. code-block:: python

            from wpipe import Condition

            logic = Condition(
                expression="status == 'CRITICAL'",
                branch_true=[notify_admin],
                branch_false=[log_info]
            )

    .. grid-item-card:: 🔁 Intelligent Loops
        :padding: 2

        Iterate until a condition is met or for a fixed count.
        ^^^
        .. code-block:: python

            from wpipe import For

            loop = For(
                iterations=5,
                validation_expression="fuel > 0",
                steps=[drive_step]
            )

3. Enterprise Resiliency
------------------------

Built for production environments where things **will** fail.

.. tab-set::

    .. tab-item:: Automatic Retries
        :sync: retry

        Configure fine-grained retry strategies for unstable steps.

        .. code-block:: python

            @step(name="API_Call", retry_count=3, retry_delay=2)
            def fetch_remote(data):
                # This will retry up to 3 times on any exception
                return call_api()

    .. tab-item:: Smart Checkpoints
        :sync: checkpoint

        WPipe can save its state to a database and resume exactly where it left off.

        .. code-block:: python

            # Checkpoint is triggered only if the expression matches
            pipeline.add_checkpoint(
                checkpoint_name="data_loaded",
                expression="len(records) > 0"
            )

    .. tab-item:: Forensic Error Capture
        :sync: error

        Global error handlers that receive the full context and traceback.

        .. code-block:: python

            def slack_notifier(context, error):
                send_to_slack(f"Pipeline {error['step_name']} failed!")

            pipeline.add_error_capture([slack_notifier])

4. High Performance
-------------------

Scale your pipelines horizontally and monitor them in real-time.

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Feature
     - Code Example
   * - **Parallelism**
     - .. code-block:: python
        
            from wpipe import Parallel
            Parallel(steps=[t1, t2], use_processes=True)
   * - **Async Engine**
     - .. code-block:: python
        
            from wpipe import PipelineAsync
            result = await pipe.run(data)
   * - **Monitoring**
     - .. code-block:: python
        
            from wpipe import ResourceMonitor
            with ResourceMonitor("Audit") as m:
                pipe.run(data)

5. Operational Integration
--------------------------

WPipe integrates seamlessly with your infrastructure.

.. card:: 🌐 Dashboard Visualizer
    :link: api_integration
    :link-type: doc

    Start the web-based dashboard to see your pipelines in a timeline or graph view.
    ^^^
    .. code-block:: python

        from wpipe import start_dashboard
        start_dashboard(db_path="tracking.db", port=5000)

.. card:: 📋 YAML-Driven Pipelines
    :link: yaml_config
    :link-type: doc

    Define your entire pipeline architecture in clean, version-controlled YAML files.
    ^^^
    .. code-block:: yaml

        name: MyPipeline
        steps:
          - name: Step1
            func: my_module.my_func
            version: v1.1

Looking for more? 
Check the 130-level :doc:`tutorials/tour/index` for specialized patterns.
