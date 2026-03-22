Error Handling
==============

Robust error handling and recovery patterns for pipelines.

Overview
--------

wpipe provides comprehensive error handling to keep your pipelines stable during failures.

::::{mermaid}
graph TB
    A[Execute Step] --> B{Success?}
    B -->|Yes| C[Continue]
    B -->|No| D[Log Error]
    D --> E{Can Recover?}
    E -->|Yes| F[Recovery]
    E -->|No| G[Raise Exception]
::::

Exception Types
---------------

TaskError
~~~~~~~~~

Raised when a single step fails:

.. code-block:: python

    from wpipe.exception import TaskError

    try:
        pipeline.run({"x": 10})
    except TaskError as e:
        print(f"Step '{e.step_name}' failed: {e}")

ProcessError
~~~~~~~~~~~

Raised when the entire pipeline fails:

.. code-block:: python

    from wpipe.exception import ProcessError

    try:
        pipeline.run({"x": 10})
    except ProcessError as e:
        print(f"Pipeline failed: {e}")

ApiError
~~~~~~~~

Raised for API-related errors:

.. code-block:: python

    from wpipe.exception import ApiError

    try:
        pipeline.run({"x": 10})
    except ApiError as e:
        print(f"API error: {e}")

Error Codes
-----------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Code
     - Description
   * - 501
     - API communication error
   * - 502
     - Task execution failed
   * - 503
     - Process update succeeded
   * - 504
     - Process update failed
   * - 505
     - Task update operation

Handling Errors
----------------

Basic Try-Catch
~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe import Pipeline
    from wpipe.exception import TaskError, ProcessError

    def failing_step(data):
        raise ValueError("Something went wrong")

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (failing_step, "Failing Step", "v1.0"),
    ])

    try:
        result = pipeline.run({"x": 10})
    except (TaskError, ProcessError) as e:
        print(f"Pipeline failed: {e}")
        print(f"Error code: {e.error_code}")

Conditional Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def validate(data):
        if "required_field" not in data:
            raise ValueError("Missing required field")
        return {"validated": True}

    def process(data):
        return {"processed": True}

    def fallback(data):
        return {"fallback": True, "used": True}

    try:
        pipeline.run({"data": "value"})
    except (TaskError, ProcessError):
        # Run fallback pipeline
        result = fallback({})

Error Recovery
--------------

Recovery Pattern
~~~~~~~~~~~~~~~~

.. code-block:: python

    def unreliable_step(data):
        import random
        if random.random() < 0.3:
            raise ConnectionError("Network error")
        return {"success": True}

    def recovery_step(data):
        return {"recovered": True, "data": data.get("data")}

    try:
        pipeline.run({"data": "important"})
    except (TaskError, ProcessError):
        # Attempt recovery
        recovery_pipeline = Pipeline()
        recovery_pipeline.set_steps([
            (recovery_step, "Recover", "v1.0"),
        ])
        result = recovery_pipeline.run({"data": "recovered"})

Accessing Partial Results
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    try:
        result = pipeline.run({"x": 10})
    except (TaskError, ProcessError) as e:
        # Access accumulated data before failure
        if hasattr(e, 'data'):
            print(f"Partial results: {e.data}")

Best Practices
--------------

1. **Always catch exceptions**: Prevent silent failures
2. **Log errors**: Track failure patterns
3. **Provide fallbacks**: Graceful degradation
4. **Use specific exceptions**: Better error handling
5. **Monitor error rates**: Alert on high failure rates

Next Steps
---------

- Learn about :doc:`retry` for automatic retries
- Explore :doc:`api_integration` for API error handling
