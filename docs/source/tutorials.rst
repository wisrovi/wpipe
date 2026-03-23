Tutorials
=========

This section contains comprehensive step-by-step tutorials for learning how to use wpipe, from basic concepts to advanced patterns.

.. toctree::
   :maxdepth: 2
   :numbered: 3

   tutorials/basic_pipeline
   tutorials/class_steps
   tutorials/api_integration
   tutorials/error_handling
   tutorials/retry_logic
   tutorials/nested_pipelines
   tutorials/sqlite_integration
   tutorials/yaml_config
   tutorials/conditions
   tutorials/advanced_patterns
   tutorials/production_deployment

1. Tutorial Overview
--------------------

This tutorials section is organized in a progressive manner, where each tutorial builds upon the concepts learned in previous tutorials.

.. list-table::
   :header-rows: 1
   :widths: 20 60 20

   * - Tutorial
     - Description
     - Difficulty
   * - :doc:`tutorials/basic_pipeline`
     - Create your first pipeline and understand data flow
     - Beginner
   * - :doc:`tutorials/class_steps`
     - Use classes with __call__ as pipeline steps
     - Beginner
   * - :doc:`tutorials/api_integration`
     - Integrate with external APIs for tracking
     - Intermediate
   * - :doc:`tutorials/error_handling`
     - Handle errors gracefully with custom exceptions
     - Intermediate
   * - :doc:`tutorials/retry_logic`
     - Implement automatic retries for failed steps
     - Intermediate
   * - :doc:`tutorials/nested_pipelines`
     - Compose complex workflows from smaller pipelines
     - Advanced
   * - :doc:`tutorials/sqlite_integration`
     - Persist pipeline execution results to database
     - Intermediate
   * - :doc:`tutorials/yaml_config`
     - Load pipeline configuration from YAML files
     - Beginner
   * - :doc:`tutorials/conditions`
     - Execute conditional branches based on data
     - Intermediate
   * - :doc:`tutorials/advanced_patterns`
     - Advanced patterns like parallel execution, callbacks
     - Advanced
   * - :doc:`tutorials/production_deployment`
     - Deploy pipelines to production environments
     - Advanced

2. Prerequisites
----------------

Before starting these tutorials, ensure you have:

2.1 Python Environment
~~~~~~~~~~~~~~~~~~~~~~~

- Python 3.9 or higher installed
- Virtual environment set up (recommended)

.. code-block:: bash

    python --version  # Should show Python 3.9+
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

2.2 Install wpipe
~~~~~~~~~~~~~~~~~

.. code-block:: bash

    pip install wpipe

Or install with development dependencies:

.. code-block:: bash

    pip install -e ".[dev]"

3. Learning Path
----------------

We recommend following this learning path:

3.1 Week 1: Fundamentals
~~~~~~~~~~~~~~~~~~~~~~~~

- Day 1-2: :doc:`tutorials/basic_pipeline`
- Day 3-4: :doc:`tutorials/class_steps`
- Day 5-7: :doc:`tutorials/yaml_config`

3.2 Week 2: Integration
~~~~~~~~~~~~~~~~~~~~~~~

- Day 8-10: :doc:`tutorials/api_integration`
- Day 11-12: :doc:`tutorials/sqlite_integration`
- Day 13-14: :doc:`tutorials/error_handling`

3.3 Week 3: Advanced
~~~~~~~~~~~~~~~~~~~~

- Day 15-17: :doc:`tutorials/retry_logic`
- Day 18-20: :doc:`tutorials/conditions`
- Day 21: :doc:`tutorials/advanced_patterns`

3.4 Week 4: Production
~~~~~~~~~~~~~~~~~~~~~~

- Day 22-28: :doc:`tutorials/production_deployment`

4. Quick Reference
------------------

4.1 Common Patterns
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Basic Pipeline
    from wpipe import Pipeline
    
    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (step1, "Step 1", "v1.0"),
        (step2, "Step 2", "v1.0"),
    ])
    result = pipeline.run(input_data)

.. code-block:: python

    # Conditional Pipeline
    from wpipe import Pipeline, Condition
    
    pipeline = Pipeline()
    pipeline.set_steps([
        (fetch_data, "Fetch", "v1.0"),
        Condition(
            expression="status == 'success'",
            branch_true=[(process_success, "Success", "v1.0")],
            branch_false=[(handle_error, "Error", "v1.0")],
        ),
    ])

.. code-block:: python

    # With SQLite
    from wpipe import Pipeline
    from wpipe.sqlite import Wsqlite
    
    with Wsqlite(db_name="results.db") as db:
        db.input = input_data
        result = pipeline.run(input_data)
        db.output = result

5. Troubleshooting
-----------------

If you encounter issues during the tutorials:

5.1 Common Issues
~~~~~~~~~~~~~~~~~

- **ImportError**: Ensure wpipe is installed correctly
- **TypeError in step**: Verify your step functions return dictionaries
- **API connection errors**: Check your API configuration

5.2 Getting Help
~~~~~~~~~~~~~~~~

- Check :doc:`user_guide/troubleshooting`
- Review :doc:`faq`
- Open an issue on GitHub

6. Next Steps
-------------

After completing these tutorials:

- Explore the :doc:`user_guide/index` for in-depth topics
- Check the :doc:`api_reference` for complete API documentation
- Review :doc:`architecture` to understand the design