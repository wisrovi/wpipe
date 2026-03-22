Troubleshooting
===============

This guide helps you diagnose and fix common issues with wpipe.

1. Common Errors
----------------

1.1 Step Must Return Dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error Message:**

::

    TypeError: Step must return a dictionary

**Cause:** A step function returned None or a non-dictionary value.

**Solution:**

.. code-block:: python

    # Wrong
    def bad_step(data):
        process(data)
        # Missing return!

    def bad_step2(data):
        return None  # Explicit None

    # Correct
    def good_step(data):
        process(data)
        return {"processed": True}

1.2 KeyError - Missing Key
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error Message:**

::

    KeyError: 'some_key'

**Cause:** Step tried to access a key that doesn't exist in the data.

**Solution:**

.. code-block:: python

    # Wrong - assumes key exists
    def bad_step(data):
        return {"doubled": data["x"] * 2}

    # Correct - use .get() with default
    def good_step(data):
        return {"doubled": data.get("x", 0) * 2}

    # Or validate and provide context
    def safe_step(data):
        if "x" not in data:
            return {"error": "Missing 'x' in data", "doubled": None}
        return {"doubled": data["x"] * 2}

1.3 TypeError - Wrong Type
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error Message:**

::

    TypeError: unsupported operand type(s) for *: 'str' and 'int'

**Cause:** Operation on incompatible types.

**Solution:**

.. code-block:: python

    # Wrong
    def bad_step(data):
        return {"result": data["value"] * 2}  # 'value' might be string

    # Correct - cast types
    def good_step(data):
        value = int(data.get("value", 0))
        return {"result": value * 2}

    # Or validate types
    def validated_step(data):
        value = data.get("value")
        if not isinstance(value, (int, float)):
            raise ValueError(f"Expected number, got {type(value)}")
        return {"result": value * 2}

1.4 TaskError - Step Failed
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error Message:**

::

    wpipe.exception.TaskError: Step 'Step Name' failed: Original error message

**Cause:** A step raised an exception.

**Solution:**

.. code-block:: python

    from wpipe.exception import TaskError

    def my_step(data):
        try:
            return do_work(data)
        except ValueError as e:
            raise TaskError(
                f"Validation failed: {e}",
                step_name="My Step",
                original_error=e
            )

2. Installation Issues
----------------------

2.1 Python Version Not Supported
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error:**

::

    ERROR: Python 3.8 is not supported. Please use Python 3.9 or higher.

**Solution:**

.. code-block:: bash

    # Check Python version
    python --version

    # Install newer Python or use pyenv
    pyenv install 3.10.12
    pyenv local 3.10.12

2.2 pip Not Found
~~~~~~~~~~~~~~~~~

**Error:**

::

    bash: pip: command not found

**Solution:**

.. code-block:: bash

    # Use python -m pip
    python -m pip install wpipe

    # Or install pip first
    python ensurepip

2.3 Permission Denied
~~~~~~~~~~~~~~~~~~~~~

**Error:**

::

    ERROR: Could not install packages due to an OSError: [Errno 13] Permission denied

**Solution:**

.. code-block:: bash

    # Use virtual environment (recommended)
    python -m venv venv
    source venv/bin/activate
    pip install wpipe

    # Or install for current user
    pip install --user wpipe

3. Import Issues
---------------

3.1 Module Not Found
~~~~~~~~~~~~~~~~~~~

**Error:**

::

    ModuleNotFoundError: No module named 'wpipe'

**Solution:**

.. code-block:: bash

    # Install wpipe
    pip install wpipe

    # Or install from source
    git clone https://github.com/wisrovi/wpipe
    cd wpipe
    pip install -e .

3.2 Circular Import
~~~~~~~~~~~~~~~~~~~

**Error:**

::

    ImportError: cannot import name 'X' from partially initialized module

**Solution:**

Circular imports usually indicate a code structure issue. Restructure your imports:

.. code-block:: python

    # module_a.py
    from module_b import function_b

    # module_b.py
    # Don't import from module_a here - causes circular import

4. API Integration Issues
--------------------------

4.1 Cannot Connect to API
~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms:**

- Pipeline hangs indefinitely
- Timeout errors
- Connection refused

**Debugging:**

.. code-block:: python

    import requests

    # Test connectivity
    api_config = {
        "base_url": "http://localhost:8418",
        "token": "my-token"
    }

    # Direct test
    response = requests.get(
        f"{api_config['base_url']}/health",
        headers={"Authorization": f"Bearer {api_config['token']}"},
        timeout=5
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

**Checklist:**

1. Is the API server running?
2. Is the base_url correct?
3. Is the token valid?
4. Is there a network/firewall issue?

4.2 Authentication Failed
~~~~~~~~~~~~~~~~~~~~~~~~~

**Error:**

::

    ApiError: Authentication failed

**Solutions:**

.. code-block:: python

    # Check token is correct
    api_config = {
        "base_url": "http://localhost:8418",
        "token": "correct-token-here"
    }

    # Token shouldn't have extra spaces
    api_config["token"] = api_config["token"].strip()

4.3 Worker Registration Failed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error:**

::

    ApiError: Failed to register worker

**Solutions:**

.. code-block:: python

    # Check API is running
    pipeline = Pipeline(api_config=api_config, verbose=True)

    # Register with explicit parameters
    try:
        worker = pipeline.worker_register(
            name="my_worker",
            version="1.0.0"
        )
        print(f"Worker ID: {worker.get('id')}")
    except Exception as e:
        print(f"Registration failed: {e}")

5. SQLite Issues
----------------

5.1 Database Locked
~~~~~~~~~~~~~~~~~~~

**Error:**

::

    sqlite3.OperationalError: database is locked

**Solutions:**

.. code-block:: python

    # Use context manager for proper cleanup
    with Wsqlite(db_name="results.db") as db:
        db.input = data
        result = pipeline.run(data)
        db.output = result
    # Database automatically released here

    # Or close explicitly
    db = Wsqlite(db_name="results.db")
    try:
        # ... use database
        pass
    finally:
        db.close()  # Release lock

5.2 Table Not Found
~~~~~~~~~~~~~~~~~~

**Error:**

::

    sqlite3.OperationalError: no such table: pipeline_executions

**Solutions:**

.. code-block:: python

    # Create table if not exists
    db = Wsqlite(db_name="results.db", create=True)
    # Table is created automatically

    # Or create manually
    db = Sqlite(db_name="results.db", create=True)
    db.create_table()

5.3 Data Not Persisting
~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms:** Data is not saved to database after pipeline runs.

**Solutions:**

.. code-block:: python

    # Wrong order - output set before run
    with Wsqlite(db_name="results.db") as db:
        db.input = {"x": 10}
        db.output = {"result": 20}  # WRONG - not from pipeline
        result = pipeline.run({"x": 10})  # Result not saved!

    # Correct order
    with Wsqlite(db_name="results.db") as db:
        db.input = {"x": 10}
        result = pipeline.run({"x": 10})
        db.output = result  # CORRECT - save pipeline result

6. Performance Issues
---------------------

6.1 Pipeline Very Slow
~~~~~~~~~~~~~~~~~~~~~~

**Causes:**

- Large data processing
- Network latency
- Inefficient algorithms

**Optimization:**

.. code-block:: python

    # Profile to find bottleneck
    from wpipe.ram import memory

    start_mem = memory()
    result = pipeline.run(data)
    end_mem = memory()

    print(f"Memory used: {end_mem - start_mem:.2f} MB")

    # Optimize slow steps
    def slow_step(data):
        # Inefficient - processes all items
        results = []
        for item in data["items"]:
            results.append(process(item))
        return {"results": results}

    def fast_step(data):
        # Efficient - batch processing
        return {"results": batch_process(data["items"])}

6.2 Memory Usage Too High
~~~~~~~~~~~~~~~~~~~~~~~~

**Solutions:**

.. code-block:: python

    # Monitor memory
    from wpipe.ram import memory

    def step_with_monitoring(data):
        before = memory()
        result = do_work(data)
        after = memory()
        print(f"Step memory: {after - before:.2f} MB")
        return result

    # Process in chunks
    def chunked_processing(data):
        for chunk in chunked(data["large_dataset"], size=1000):
            yield from process_chunk(chunk)

7. Debugging Techniques
----------------------

7.1 Enable Verbose Mode
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    pipeline = Pipeline(verbose=True)
    result = pipeline.run(data)

7.2 Add Debug Steps
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def debug_step(data):
        print(f"DEBUG: Current data keys: {list(data.keys())}")
        print(f"DEBUG: Sample values: { {k: data[k] for k in list(data.keys())[:3]} }")
        return data  # Pass through unchanged

    pipeline.set_steps([
        (step1, "Step 1", "v1.0"),
        (debug_step, "DEBUG", "v1.0"),  # Insert debug step
        (step2, "Step 2", "v1.0"),
    ])

7.3 Test Steps Individually
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Test each step in isolation
    test_data = {"x": 10}

    print("Testing step1:")
    result1 = step1(test_data)
    print(f"  Result: {result1}")

    print("Testing step2:")
    result2 = step2({**test_data, **result1})
    print(f"  Result: {result2}")

7.4 Use Try/Except
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe.exception import TaskError

    try:
        result = pipeline.run(data)
    except TaskError as e:
        print(f"Failed at: {e.step_name}")
        print(f"Error code: {e.code}")
        print(f"Original error: {e.original_error}")
        print(f"Partial results: {getattr(e, 'partial_results', 'N/A')}")

8. Getting Help
---------------

8.1 Collect Information
~~~~~~~~~~~~~~~~~~~~~~~

When reporting an issue, include:

.. code-block:: python

    import sys
    import wpipe

    print(f"Python: {sys.version}")
    print(f"wpipe: {wpipe.__version__}")

    # Your environment info
    import platform
    print(f"OS: {platform.platform()}")
    print(f"Architecture: {platform.machine()}")

8.2 Check Existing Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~

Visit https://github.com/wisrovi/wpipe/issues to see if your issue is already reported.

8.3 Report New Issues
~~~~~~~~~~~~~~~~~~~~~

Include:

- Python version
- wpipe version
- Minimal reproducible example
- Full error traceback
- Expected vs actual behavior
