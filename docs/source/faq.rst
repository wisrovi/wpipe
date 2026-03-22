FAQ
===

Frequently Asked Questions about wpipe.

1. General Questions
--------------------

1.1 What is wpipe?
~~~~~~~~~~~~~~~~~~

wpipe is a Python library for creating and executing sequential data processing pipelines with task orchestration, API integration, and execution tracking. It provides a simple yet powerful way to define multi-step data processing workflows.

**Key capabilities:**

- Define pipelines as sequences of steps (functions or classes)
- Automatic data flow between steps
- Built-in API integration for worker registration and health checks
- SQLite persistence for execution results
- Rich terminal progress visualization
- Error handling with custom exceptions
- Nested pipelines for complex workflows

1.2 What are the main features?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Pipeline Orchestration**

- Sequential step execution
- Automatic data accumulation between steps
- Step versioning for tracking changes
- Nested pipeline support

**API Integration**

- Worker registration with external services
- Health check monitoring
- Task status reporting
- Process tracking

**Data Persistence**

- SQLite integration for storing execution results
- Input/output tracking
- Execution metadata storage

**Error Handling**

- Custom exception types
- Error codes for categorization
- Detailed error information

**Configuration**

- YAML configuration support
- Environment variable substitution
- Flexible API configuration

1.3 What is the license?
~~~~~~~~~~~~~~~~~~~~~~~~

wpipe is released under the MIT License. You can use it freely in personal and commercial projects.

1.4 Is wpipe production-ready?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes, wpipe v1.0.0 is the first LTS (Long Term Support) release with:

- 206 passing tests
- Stable API with backward compatibility guarantee
- Comprehensive documentation
- Production-ready error handling

2. Installation Questions
-------------------------

2.1 What Python version is required?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wpipe requires **Python 3.9 or higher**.

You can check your Python version:

.. code-block:: bash

    python --version

2.2 How do I install wpipe?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using pip:

.. code-block:: bash

    pip install wpipe

With specific version:

.. code-block:: bash

    pip install wpipe==1.0.0

2.3 How do I install from source?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    git clone https://github.com/wisrovi/wpipe
    cd wpipe
    pip install -e .

For development:

.. code-block:: bash

    pip install -e ".[dev]"

2.4 What are the dependencies?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Core dependencies:**

- ``requests`` - HTTP client for API communication
- ``pyyaml`` - YAML configuration parsing

**Development dependencies:**

- ``pytest`` - Testing framework
- ``ruff`` - Linting
- ``mypy`` - Type checking
- ``sphinx`` - Documentation

3. Getting Started Questions
----------------------------

3.1 How do I create a basic pipeline?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe import Pipeline

    def step1(data):
        return {"result": data["x"] * 2}

    def step2(data):
        return {"final": data["result"] + 10}

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (step1, "Double", "v1.0"),
        (step2, "Add Ten", "v1.0"),
    ])

    result = pipeline.run({"x": 5})
    # {'x': 5, 'result': 10, 'final': 20}

3.2 What is the data flow between steps?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each step receives the accumulated results from all previous steps:

.. code-block:: text

    Input: {'x': 5}
    
    Step 1 returns {'result': 10}
    Data after Step 1: {'x': 5, 'result': 10}
    
    Step 2 receives {'x': 5, 'result': 10}
    Step 2 returns {'final': 20}
    Data after Step 2: {'x': 5, 'result': 10, 'final': 20}

3.3 Can I use classes as steps?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes! Any callable with a ``__call__`` method works:

.. code-block:: python

    class Multiply:
        def __init__(self, factor):
            self.factor = factor

        def __call__(self, data):
            return {"result": data["x"] * self.factor}

    pipeline = Pipeline()
    pipeline.set_steps([
        (Multiply(2), "Double", "v1.0"),
        (Multiply(3), "Triple", "v1.0"),
    ])

3.4 How do I run a pipeline?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    result = pipeline.run(initial_data)

    # With verbose output
    result = pipeline.run(initial_data, verbose=True)

4. API Integration Questions
----------------------------

4.1 How do I connect to an API?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    api_config = {
        "base_url": "http://localhost:8418",
        "token": "your-auth-token"
    }

    pipeline = Pipeline(api_config=api_config)

4.2 How do I register a worker?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    worker_info = pipeline.worker_register(
        name="my_worker",
        version="1.0.0"
    )

    worker_id = worker_info.get("id")
    pipeline.set_worker_id(worker_id)

4.3 How do I perform health checks?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Health checks are performed automatically when configured:

.. code-block:: python

    pipeline = Pipeline(
        api_config=api_config,
        health_check_interval=60  # Check every 60 seconds
    )

5. SQLite Questions
--------------------

5.1 How do I persist results?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe.sqlite import Wsqlite

    with Wsqlite(db_name="results.db") as db:
        db.input = {"x": 10}
        result = pipeline.run({"x": 10})
        db.output = result

5.2 What data is stored?
~~~~~~~~~~~~~~~~~~~~~~~~

- Execution ID
- Input data (JSON)
- Output data (JSON)
- Start/end timestamps
- Status

5.3 How do I query results?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe.sqlite import Wsqlite

    with Wsqlite(db_name="results.db") as db:
        cursor = db.execute(
            "SELECT * FROM pipeline_executions ORDER BY created_at DESC"
        )
        results = cursor.fetchall()

6. Error Handling Questions
---------------------------

6.1 How do I handle errors?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe.exception import TaskError

    try:
        result = pipeline.run(data)
    except TaskError as e:
        print(f"Failed at step: {e.step_name}")
        print(f"Error code: {e.code}")
        print(f"Original error: {e.original_error}")

6.2 What error codes are available?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe.exception import Codes

    # Available codes:
    Codes.UNKNOWN_ERROR      # Generic error
    Codes.VALIDATION_ERROR   # Input validation failed
    Codes.API_ERROR          # API communication error
    Codes.RETRYABLE_ERROR   # Error that may succeed on retry
    Codes.TIMEOUT_ERROR      # Operation timed out

6.3 How do I create custom error codes?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe.exception import TaskError, Codes

    class CustomCodes(Codes):
        MY_CUSTOM_ERROR = "MY_CUSTOM_ERROR"

    raise TaskError(
        "Custom error message",
        code=CustomCodes.MY_CUSTOM_ERROR
    )

7. Configuration Questions
---------------------------

7.1 How do I use YAML configuration?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a YAML file:

.. code-block:: yaml

    # config.yaml
    pipeline:
      verbose: true
      log_level: DEBUG

    api:
      base_url: "http://api.example.com"
      token: "your-token"

Load it:

.. code-block:: python

    from wpipe.util import load_config

    config = load_config("config.yaml")
    pipeline = Pipeline(
        verbose=config["pipeline"]["verbose"],
        api_config=config["api"]
    )

7.2 Can I use environment variables?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes, use the ``${VAR}`` syntax:

.. code-block:: yaml

    api:
      token: ${API_TOKEN}
      path: ${DB_PATH:-default.db}  # With default

8. Troubleshooting Questions
-----------------------------

8.1 My pipeline is not connecting to the API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Checklist:**

1. Verify the API server is running
2. Check the base_url is correct
3. Ensure the token is valid
4. Check network connectivity
5. Verify firewall rules

**Debug:**

.. code-block:: python

    pipeline = Pipeline(api_config=api_config, verbose=True)

8.2 The pipeline is stuck on a step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Possible causes:**

1. Infinite loop in your step function
2. Step not returning (missing return statement)
3. Blocking I/O operation

**Debug:**

.. code-block:: python

    # Add debug output
    def debug_step(data):
        print(f"Received data: {data}")
        result = process(data)
        print(f"Returning: {result}")
        return result

8.3 I'm getting TaskError exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is expected when a step fails. Wrap in try/except:

.. code-block:: python

    try:
        result = pipeline.run(data)
    except TaskError as e:
        # Handle the error
        print(f"Step {e.step_name} failed: {e}")

8.4 How do I enable verbose output?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Option 1: Constructor**

.. code-block:: python

    pipeline = Pipeline(verbose=True)

**Option 2: Run method**

.. code-block:: python

    result = pipeline.run(data, verbose=True)

9. Performance Questions
------------------------

9.1 How fast is wpipe?
~~~~~~~~~~~~~~~~~~~~~~~

Pipeline overhead is minimal (< 1ms per step). Actual performance depends on your step implementations.

9.2 Can I process large datasets?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes, but design steps carefully:

.. code-block:: python

    def chunk_processor(data):
        for chunk in chunked(large_dataset, size=1000):
            yield process_chunk(chunk)

9.3 How do I monitor memory usage?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe.ram import RAM

    ram = RAM()
    print(f"Memory: {ram.get_usage()} MB")

10. Advanced Questions
----------------------

10.1 Can I create conditional branches?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    pipeline.add_condition(
        condition=Condition(data_key="mode", operator="==", value="prod"),
        then_steps=[...],
        else_steps=[...],
    )

10.2 Can I nest pipelines?
~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes:

.. code-block:: python

    inner = Pipeline()
    inner.set_steps([...])

    outer = Pipeline()
    outer.set_steps([
        (inner.run, "Run Inner", "v1.0"),
    ])

10.3 Can I add callbacks?
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def on_complete(result):
        notify(result)

    pipeline.on_complete(on_complete)

11. Contributing Questions
--------------------------

11.1 How do I report bugs?
~~~~~~~~~~~~~~~~~~~~~~~~~~

Report issues at: https://github.com/wisrovi/wpipe/issues

11.2 How do I contribute?
~~~~~~~~~~~~~~~~~~~~~~~~~

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: ``pytest``
5. Run linting: ``ruff check``
6. Submit a pull request

11.3 Where can I get help?
~~~~~~~~~~~~~~~~~~~~~~~~~~

- GitHub Issues: https://github.com/wisrovi/wpipe/issues
- Documentation: https://wpipe.readthedocs.io/
