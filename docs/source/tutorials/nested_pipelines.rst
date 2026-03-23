Nested Pipelines Tutorial
========================

Learn how to compose complex workflows from smaller, reusable pipelines.

.. contents::
   :local:
   :depth: 2

1. Introduction
---------------

Nested pipelines allow you to:

- Reuse common workflow patterns
- Organize complex processing into logical groups
- Build modular, maintainable pipelines

2. Basic Nested Pipeline
------------------------

2.1 Creating Nested Pipelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe import Pipeline

    # Create inner pipeline
    inner_pipeline = Pipeline(verbose=True)
    inner_pipeline.set_steps([
        (lambda d: {"inner_value": d["x"] * 2}, "Multiply by 2", "v1.0"),
        (lambda d: {"squared": d["inner_value"] ** 2}, "Square", "v1.0"),
    ])

    # Create outer pipeline
    outer_pipeline = Pipeline(verbose=True)
    outer_pipeline.set_steps([
        (lambda d: {"x": 5}, "Initialize", "v1.0"),
        (inner_pipeline.run, "Run Inner Pipeline", "v1.0"),
        (lambda d: {"final": d.get("squared", 0) + 10}, "Finalize", "v1.0"),
    ])

    result = outer_pipeline.run({})
    print(result["final"])  # 60

3. Pipeline Factory Pattern
---------------------------

3.1 Creating Reusable Pipelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def create_data_processing_pipeline(name: str, multiplier: float):
        """Factory function to create processing pipelines."""
        pipeline = Pipeline()
        pipeline.set_steps([
            (lambda d: {"input": d.get("value", 0) * multiplier}, 
             f"{name} Input", "v1.0"),
            (lambda d: {"processed": d["input"] + 1}, 
             f"{name} Process", "v1.0"),
            (lambda d: {"output": d["processed"] * 2}, 
             f"{name} Output", "v1.0"),
        ])
        return pipeline

    # Create multiple pipelines from factory
    pipeline_a = create_data_processing_pipeline("PipelineA", 2.0)
    pipeline_b = create_data_processing_pipeline("PipelineB", 3.0)

4. Complete Example
-------------------

.. code-block:: python

    from wpipe import Pipeline


    # Define reusable sub-pipelines
    def create_etl_pipeline():
        """Create an ETL pipeline."""
        pipeline = Pipeline()
        pipeline.set_steps([
            (lambda d: {"raw_data": [1, 2, 3, 4, 5]}, "Extract", "v1.0"),
            (lambda d: {"cleaned": [x * 2 for x in d["raw_data"]]}, "Transform", "v1.0"),
            (lambda d: {"loaded": True, "count": len(d["cleaned"])}, "Load", "v1.0"),
        ])
        return pipeline


    def create_validation_pipeline():
        """Create a validation pipeline."""
        pipeline = Pipeline()
        pipeline.set_steps([
            (lambda d: {"valid": True}, "Check Format", "v1.0"),
            (lambda d: {"validated": True}, "Check Rules", "v1.0"),
        ])
        return pipeline


    # Main pipeline that combines them
    main_pipeline = Pipeline(verbose=True)
    main_pipeline.set_steps([
        (lambda d: {"source": "database"}, "Initialize", "v1.0"),
        (create_etl_pipeline().run, "ETL Process", "v1.0"),
        (create_validation_pipeline().run, "Validation", "v1.0"),
        (lambda d: {"status": "completed"}, "Complete", "v1.0"),
    ])

    result = main_pipeline.run({})
    print(f"Result: {result}")

5. Best Practices
-----------------

- Keep nested pipelines focused on single responsibility
- Use pipeline factories for configuration
- Test sub-pipelines independently

6. Next Steps
-------------

- :doc:`sqlite_integration` - Add persistence
- :doc:`production_deployment` - Deploy to production