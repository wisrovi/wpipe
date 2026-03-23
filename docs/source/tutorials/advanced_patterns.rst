Advanced Patterns Tutorial
============================

Learn advanced patterns for complex pipeline scenarios.

.. contents::
   :local:
   :depth: 2

1. Parallel Execution
---------------------

1.1 ThreadPoolExecutor
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from concurrent.futures import ThreadPoolExecutor

    def parallel_steps(data):
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(step, data)
                for step in [step1, step2, step3]
            ]
            results = [f.result() for f in futures]
        return {"parallel_results": results}

2. Custom Pipeline Extensions
------------------------------

2.1 Extending Pipeline
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe import Pipeline

    class CustomPipeline(Pipeline):
        """Extended pipeline with additional functionality."""
        
        def run(self, *args, **kwargs):
            print("Custom pre-processing")
            result = super().run(*args, **kwargs)
            print("Custom post-processing")
            return result

3. Complete Example
------------------

.. code-block:: python

    from wpipe import Pipeline
    from concurrent.futures import ThreadPoolExecutor
    import time


    class AdvancedPipeline(Pipeline):
        """Pipeline with advanced features."""
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.execution_log = []
        
        def _task_invoke(self, func, name, *args, **kwargs):
            start = time.time()
            result = super()._task_invoke(func, name, *args, **kwargs)
            elapsed = time.time() - start
            self.execution_log.append({
                "step": name,
                "time": elapsed
            })
            return result


    def step1(data):
        time.sleep(0.1)
        return {"step1": "done"}


    def step2(data):
        time.sleep(0.1)
        return {"step2": "done"}


    pipeline = AdvancedPipeline(verbose=True)
    pipeline.set_steps([
        (step1, "Step 1", "v1.0"),
        (step2, "Step 2", "v1.0"),
    ])

    result = pipeline.run({})
    print(f"Execution log: {pipeline.execution_log}")

4. Best Practices
-----------------

- Keep custom extensions focused
- Test thoroughly
- Document changes

5. Next Steps
-------------

- :doc:`production_deployment` - Deploy to production