SQLite Integration Tutorial
===========================

Learn how to persist pipeline execution results to SQLite databases.

.. contents::
   :local:
   :depth: 2

1. Introduction
---------------

SQLite integration allows you to:

- Track pipeline execution history
- Store input/output data for auditing
- Query past executions for analysis
- Build data pipelines with persistence

2. Basic SQLite Usage
---------------------

2.1 Using Wsqlite
~~~~~~~~~~~~~~~~~

The Wsqlite class provides a simple interface:

.. code-block:: python

    from wpipe import Pipeline
    from wpipe.sqlite import Wsqlite

    pipeline = Pipeline()
    pipeline.set_steps([
        (lambda d: {"result": d["x"] * 2}, "Process", "v1.0"),
    ])

    with Wsqlite(db_name="results.db") as db:
        input_data = {"x": 10}
        db.input = input_data
        
        result = pipeline.run(input_data)
        db.output = result

3. Querying Results
-------------------

3.1 Reading Records
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe.sqlite import Wsqlite

    with Wsqlite(db_name="results.db") as db:
        # Access stored data
        print(f"Input: {db.input}")
        print(f"Output: {db.output}")
        print(f"ID: {db.id}")

4. Advanced Patterns
--------------------

4.1 Multiple Executions
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe import Pipeline
    from wpipe.sqlite import Wsqlite

    pipeline = Pipeline()
    pipeline.set_steps([
        (lambda d: {"processed": d["value"] * 2}, "Process", "v1.0"),
    ])

    test_cases = [{"value": 1}, {"value": 2}, {"value": 3}]

    with Wsqlite(db_name="test_results.db") as db:
        for test_data in test_cases:
            db.input = test_data
            result = pipeline.run(test_data)
            db.output = result

5. Complete Example
------------------

.. code-block:: python

    from wpipe import Pipeline
    from wpipe.sqlite import Wsqlite
    import json


    class PersistentPipeline(Pipeline):
        """Pipeline that automatically saves results to SQLite."""
        
        def __init__(self, db_name: str, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.db_name = db_name
        
        def run(self, *args, **kwargs):
            with Wsqlite(db_name=self.db_name) as db:
                db.input = args[0] if args else {}
                
                result = super().run(*args, **kwargs)
                
                db.output = result
                return result


    # Create and run
    pipeline = PersistentPipeline(db_name="pipeline_history.db", verbose=True)
    pipeline.set_steps([
        (lambda d: {"data": [1, 2, 3]}, "Load", "v1.0"),
        (lambda d: {"sum": sum(d["data"])}, "Sum", "v1.0"),
    ])

    result = pipeline.run({"test": True})
    print(f"Result: {result}")

6. Best Practices
-----------------

- Use context managers for automatic cleanup
- Keep database files in dedicated directories
- Index frequently queried fields

7. Next Steps
-------------

- :doc:`yaml_config` - Use YAML configuration
- :doc:`production_deployment` - Deploy to production