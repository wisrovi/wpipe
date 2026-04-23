Getting Started with |wpipe|
=============================

.. meta::
   :description: Quick start guide for wpipe v2.1.1-LTS. Learn how to install and build your first pipeline.
   :keywords: quickstart, installation, tutorial, python, pipeline

Welcome to the future of Python orchestration. This guide will help you set up **wpipe v2.1.1-LTS** and execute your first industrial-grade pipeline in minutes.

.. raw:: html

    <div style="background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); padding: 2px; border-radius: 12px; margin-bottom: 30px;">
        <div style="background: #0f172a; padding: 25px; border-radius: 10px;">
            <h2 style="color: #00f2fe; margin-top: 0; border: none;">⚡ Fast-Track to Power</h2>
            <p style="color: #f8fafc; margin-bottom: 0;">
                WPipe is designed for engineers who value <strong>performance, zero-boilerplate</strong>, and <strong>resilience</strong>. 
                Let's get your environment ready.
            </p>
        </div>
    </div>

1. Installation
---------------

Install the core engine via PyPI. We recommend using a virtual environment for your projects.

.. tab-set::

    .. tab-item:: Standard
        :sync: pip

        .. code-block:: bash

            pip install wpipe

    .. tab-item:: Full (Dev/Docs)
        :sync: full

        .. code-block:: bash

            pip install "wpipe[dev,docs]"

    .. tab-item:: Source
        :sync: source

        .. code-block:: bash

            git clone https://github.com/wisrovi/wpipe
            cd wpipe
            pip install -e .

2. Verification
---------------

Ensure the engine is correctly synchronized with your system.

.. code-block:: python

    import wpipe
    from wpipe import Pipeline
    
    print(f"🚀 WPipe v{wpipe.__version__} - Engine Synchronized.")
    # Expected: 🚀 WPipe v2.1.1 - Engine Synchronized.

3. Build Your First Pipeline
----------------------------

Follow these three steps to master the basic mental model.

.. grid:: 1 1 3 3
    :gutter: 3

    .. grid-item-card:: 🏗️ 1. Define Steps
        :padding: 2

        Create pure Python functions that return a dictionary (the context update).
        ^^^
        .. code-block:: python

            def fetch(data):
                return {"user": "wisrovi"}

    .. grid-item-card:: 🧩 2. Orchestrate
        :padding: 2

        Instantiate the `Pipeline` and register your steps with version control.
        ^^^
        .. code-block:: python

            pipe = Pipeline(verbose=True)
            pipe.set_steps([
                (fetch, "FetchUser", "v1.0")
            ])

    .. grid-item-card:: ⚡ 3. Execute
        :padding: 2

        Invoke the `.run()` method with initial data. Watch the magic happen.
        ^^^
        .. code-block:: python

            result = pipe.run({})
            # {'user': 'wisrovi'}

4. The "Hello World" of Orchestration
-------------------------------------

Here is a complete, production-ready example demonstrating data accumulation.

.. code-block:: python
    :linenos:
    :emphasize-lines: 15,22

    from wpipe import Pipeline, step

    # Each step automatically receives all data from previous steps
    @step(name="Step_Alpha", version="1.0.0")
    def step_alpha(data):
        return {"a": 10}

    @step(name="Step_Beta", version="1.0.0")
    def step_beta(data):
        # Accessing data['a'] from previous step
        return {"b": data["a"] * 2}

    if __name__ == "__main__":
        # Initialize engine
        engine = Pipeline(pipeline_name="MyFirstLTS", verbose=True)

        # Build the chain
        engine.set_steps([
            step_alpha,
            step_beta
        ])

        # Execute
        final_warehouse = engine.run({"input": "raw_signal"})
        
        print(f"Result: {final_warehouse}")
        # Result: {'input': 'raw_signal', 'a': 10, 'b': 20}

5. Enterprise Capabilities at a Glance
--------------------------------------

WPipe v2.1.1-LTS is not just about sequences. It's about industrial reliability.

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Capability
     - Why it matters
   * - **Parallel Execution**
     - Run independent tasks in Threads or Processes with zero complexity.
   * - **Smart Checkpoints**
     - Auto-resume from milestones if the system crashes or fails.
   * - **SQLite WAL Mode**
     - Ultra-fast persistence with zero-lock concurrency.
   * - **Dashboard**
     - Real-time visual monitoring of your entire pipeline fleet.

Next Steps
----------

.. raw:: html

    <div style="display: flex; gap: 15px; margin-top: 20px;">
        <a href="usage.html" style="flex: 1; text-align: center; background: #1e293b; padding: 20px; border-radius: 12px; text-decoration: none; border: 1px solid #334155;">
            <h4 style="color: #00f2fe; margin: 0;">Explore Usage →</h4>
            <p style="color: #94a3b8; font-size: 0.9em; margin-top: 10px;">Deep dive into every parameter and configuration.</p>
        </a>
        <a href="tutorials/tour/index.html" style="flex: 1; text-align: center; background: #1e293b; padding: 20px; border-radius: 12px; text-decoration: none; border: 1px solid #334155;">
            <h4 style="color: #f59e0b; margin: 0;">Start The Tour →</h4>
            <p style="color: #94a3b8; font-size: 0.9em; margin-top: 10px;">Master all 130 levels of the learning path.</p>
        </a>
    </div>
