Nested Pipelines
=================

Compose complex workflows by nesting pipelines within pipelines.

Overview
--------

Nested pipelines allow you to break complex workflows into smaller, reusable components.

::::{mermaid}
graph TB
    A[Main Pipeline] --> B[Pipeline A]
    A --> C[Pipeline B]
    B --> D[Step 1]
    B --> E[Step 2]
    C --> F[Step 3]
    C --> G[Step 4]
::::

Basic Usage
-----------

Create Sub-Pipelines
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe import Pipeline

    pipeline_a = Pipeline()
    pipeline_a.set_steps([
        (step1, "Step A1", "v1.0"),
        (step2, "Step A2", "v1.0"),
    ])

    pipeline_b = Pipeline()
    pipeline_b.set_steps([
        (step3, "Step B1", "v1.0"),
        (step4, "Step B2", "v1.0"),
    ])

Nest in Main Pipeline
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    main_pipeline = Pipeline()
    main_pipeline.set_steps([
        (pipeline_a, "Pipeline A", "v1.0"),
        (pipeline_b, "Pipeline B", "v1.0"),
    ])

    result = main_pipeline.run({"initial": "data"})

Data Flow in Nested Pipelines
------------------------------

::::{mermaid}
graph LR
    A["Input: {'x': 1}"] --> PA[Pipeline A]
    PA --> A1[Step A1]
    A1 --> A2[Step A2]
    A2 --> DA["Accumulated: {'x': 1, 'a': True}"]
    DA --> PB[Pipeline B]
    PB --> B1[Step B1]
    B1 --> B2[Step B2]
    B2 --> O["Output: {'x': 1, 'a': True, 'b': True}"]
::::

Data is accumulated through the entire nested structure.

Use Cases
---------

Data Processing ETL
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    extract_pipeline = Pipeline()
    extract_pipeline.set_steps([
        (fetch_from_api, "Fetch API", "v1.0"),
        (parse_json, "Parse JSON", "v1.0"),
    ])

    transform_pipeline = Pipeline()
    transform_pipeline.set_steps([
        (clean_data, "Clean", "v1.0"),
        (validate_schema, "Validate", "v1.0"),
        (enrich_data, "Enrich", "v1.0"),
    ])

    load_pipeline = Pipeline()
    load_pipeline.set_steps([
        (format_for_db, "Format", "v1.0"),
        (insert_records, "Insert", "v1.0"),
    ])

    etl_pipeline = Pipeline()
    etl_pipeline.set_steps([
        (extract_pipeline, "Extract", "v1.0"),
        (transform_pipeline, "Transform", "v1.0"),
        (load_pipeline, "Load", "v1.0"),
    ])

Branching Workflows
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    validation_pipeline = Pipeline()
    validation_pipeline.set_steps([
        (check_format, "Check Format", "v1.0"),
        (validate_content, "Validate Content", "v1.0"),
    ])

    processing_pipeline = Pipeline()
    processing_pipeline.set_steps([
        (transform_data, "Transform", "v1.0"),
        (apply_business_rules, "Apply Rules", "v1.0"),
    ])

    main_pipeline = Pipeline()
    main_pipeline.set_steps([
        (validation_pipeline, "Validate", "v1.0"),
        (processing_pipeline, "Process", "v1.0"),
    ])

Complete Example
----------------

.. code-block:: python

    from wpipe import Pipeline

    def fetch(data):
        return {"users": [{"id": 1}, {"id": 2}]}

    def enrich_user(data):
        user = data["current_user"]
        return {"enriched": {"id": user["id"], "name": f"User {user['id']}"}}

    def save_user(data):
        return {"saved": True}

    user_pipeline = Pipeline()
    user_pipeline.set_steps([
        (enrich_user, "Enrich", "v1.0"),
        (save_user, "Save", "v1.0"),
    ])

    main_pipeline = Pipeline()
    main_pipeline.set_steps([
        (fetch, "Fetch", "v1.0"),
        (user_pipeline, "Process Users", "v1.0"),
    ])

Best Practices
--------------

1. **Keep sub-pipelines focused**: Single responsibility
2. **Name nested pipelines clearly**: Easy to understand structure
3. **Test sub-pipelines independently**: Ensure reliability
4. **Document data expectations**: What each nested pipeline needs/produces

Next Steps
---------

- Learn about :doc:`error_handling` for error recovery
- Explore :doc:`conditions` for conditional execution
