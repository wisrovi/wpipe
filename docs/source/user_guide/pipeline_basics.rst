Pipeline Basics
===============

This guide covers the fundamental concepts of pipelines in wpipe, from basic usage to advanced patterns.

1. Overview
-----------

A pipeline is a sequence of steps that process data. Each step receives the accumulated results from all previous steps and returns its own results, which are then passed to the next step.

**Key Characteristics:**

- **Sequential**: Steps execute in the order they are defined
- **Accumulating**: Data builds up as it flows through the pipeline
- **Failing Fast**: Pipeline stops on the first error
- **Reusable**: Same pipeline can run with different data

2. Core Concepts
----------------

2.1 Pipeline Class
~~~~~~~~~~~~~~~~~~

The ``Pipeline`` class is the main entry point for creating and executing pipelines.

.. code-block:: python

    from wpipe import Pipeline

    pipeline = Pipeline(
        verbose=True,
        log_level="INFO"
    )

**Constructor Parameters:**

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parameter
     - Description
   * - ``verbose``
     - Enable detailed progress output
   * - ``log_level``
     - Logging level: DEBUG, INFO, WARNING, ERROR
   * - ``api_config``
     - API configuration for external tracking
   * - ``max_retries``
     - Maximum retry attempts for failed steps

2.2 Step Structure
~~~~~~~~~~~~~~~~~~

A step is a tuple containing three elements:

.. code-block:: python

    step = (callable, name, version)

**Elements:**

- **callable**: A function or class instance that accepts data and returns results
- **name**: A human-readable string identifier (used in logging)
- **version**: A version string for tracking (e.g., "v1.0", "2.0.0")

2.3 Data Flow Mechanics
~~~~~~~~~~~~~~~~~~~~~~~~

Data flows through the pipeline as follows:

::

    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   Input: {'initial': 'value'}                                      │
    │                                                                     │
    │   Step 1 receives: {'initial': 'value'}                            │
    │   Step 1 returns: {'a': 10}                                        │
    │                                                                     │
    │   Step 2 receives: {'initial': 'value', 'a': 10}                   │
    │   Step 2 returns: {'b': 20}                                        │
    │                                                                     │
    │   Step 3 receives: {'initial': 'value', 'a': 10, 'b': 20}          │
    │   Step 3 returns: {'c': 30}                                        │
    │                                                                     │
    │   Output: {'initial': 'value', 'a': 10, 'b': 20, 'c': 30}          │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

3. Creating Pipelines
----------------------

3.1 Minimal Pipeline
~~~~~~~~~~~~~~~~~~~~

The simplest possible pipeline:

.. code-block:: python

    from wpipe import Pipeline

    def step(data):
        return {"result": "Hello, World!"}

    pipeline = Pipeline()
    pipeline.set_steps([(step, "Simple Step", "v1.0")])

    result = pipeline.run({})
    print(result)  # {'result': 'Hello, World!'}

3.2 Multi-Step Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~

A pipeline with multiple processing steps:

.. code-block:: python

    from wpipe import Pipeline

    def load_data(data):
        return {"numbers": [1, 2, 3, 4, 5]}

    def calculate_sum(data):
        return {"sum": sum(data["numbers"])}

    def calculate_average(data):
        return {"average": data["sum"] / len(data["numbers"])}

    def format_output(data):
        return {
            "output": f"Sum={data['sum']}, Avg={data['average']}"
        }

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (load_data, "Load Data", "v1.0"),
        (calculate_sum, "Calculate Sum", "v1.0"),
        (calculate_average, "Calculate Average", "v1.0"),
        (format_output, "Format Output", "v1.0"),
    ])

    result = pipeline.run({})
    # Output: {'output': 'Sum=15, Avg=3.0'}

3.3 ETL Pipeline
~~~~~~~~~~~~~~~~~

Extract, Transform, Load pattern:

.. code-block:: python

    from wpipe import Pipeline

    def extract(data):
        return {
            "raw_users": [
                {"name": "Alice", "age": 30},
                {"name": "Bob", "age": 25},
            ]
        }

    def transform(data):
        transformed = [
            {**user, "age_category": "adult" if u["age"] >= 18 else "minor"}
            for u, user in enumerate(data["raw_users"])
        ]
        return {"processed_users": transformed}

    def load(data):
        # Simulate saving to database
        saved_count = len(data["processed_users"])
        return {"status": "loaded", "count": saved_count}

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (extract, "Extract", "v1.0"),
        (transform, "Transform", "v1.0"),
        (load, "Load", "v1.0"),
    ])

    result = pipeline.run({})

4. Step Types
-------------

4.1 Function Steps
~~~~~~~~~~~~~~~~~~

The most common step type - regular Python functions:

.. code-block:: python

    def fetch_data(data):
        """Fetch data from an external source."""
        api_response = {"items": [1, 2, 3]}
        return {"fetched": api_response}

    def process_items(data):
        """Process fetched items."""
        items = data["fetched"]["items"]
        return {"processed": [x * 2 for x in items]}

    def save_results(data):
        """Save results (returns status, not the data itself)."""
        return {"saved": True, "count": len(data["processed"])}

4.2 Lambda Steps
~~~~~~~~~~~~~~~~

For simple, single-expression transformations:

.. code-block:: python

    pipeline.set_steps([
        (lambda d: {"x2": d["x"] * 2}, "Double", "v1.0"),
        (lambda d: {"x4": d["x2"] * 2}, "Quadruple", "v1.0"),
    ])

**Warning:** Avoid complex logic in lambda steps. Use named functions for readability.

4.3 Class Steps
~~~~~~~~~~~~~~~

For stateful processing or complex behavior:

.. code-block:: python

    class DataProcessor:
        def __init__(self, multiplier: float, offset: float = 0):
            self.multiplier = multiplier
            self.offset = offset
            self.processed_count = 0

        def __call__(self, data: dict) -> dict:
            self.processed_count += 1
            value = data.get("value", 0)
            return {
                "processed_value": value * self.multiplier + self.offset,
                "processing_count": self.processed_count,
            }

    processor = DataProcessor(multiplier=2.5, offset=10)

    pipeline.set_steps([
        (processor, "Process Data", "v1.0"),
    ])

4.4 Method Steps
~~~~~~~~~~~~~~~~

Bind methods as steps:

.. code-block:: python

    class DataHandler:
        def __init__(self):
            self.results = []

        def validate(self, data):
            return {"valid": "value" in data}

        def process(self, data):
            return {"processed": data["value"] * 2}

        def finalize(self, data):
            self.results.append(data)
            return {"finalized": True}

    handler = DataHandler()

    pipeline.set_steps([
        (handler.validate, "Validate", "v1.0"),
        (handler.process, "Process", "v1.0"),
        (handler.finalize, "Finalize", "v1.0"),
    ])

5. Step Best Practices
-----------------------

5.1 Always Return Dictionaries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Steps must always return a dictionary:

.. code-block:: python

    # Good
    def good_step(data):
        return {"result": data["x"] * 2}

    # Bad - returns None
    def bad_step(data):
        print(data["x"] * 2)
        # Missing return!

    # Bad - returns wrong type
    def wrong_type(data):
        return data["x"] * 2  # Returns int, not dict

5.2 Handle Missing Keys
~~~~~~~~~~~~~~~~~~~~~~~

Use ``.get()`` with defaults for optional data:

.. code-block:: python

    def robust_step(data):
        value = data.get("value", 0)
        multiplier = data.get("multiplier", 1)
        return {"result": value * multiplier}

5.3 Keep Steps Focused
~~~~~~~~~~~~~~~~~~~~~~

Each step should do one thing well:

.. code-block:: python

    # Good: Focused steps
    def fetch_user(data):
        return {"user": get_user_from_db(data["user_id"])}

    def validate_email(data):
        return {"email_valid": "@" in data["user"].get("email", "")}

    def send_welcome(data):
        return {"welcome_sent": True}

    # Bad: Monolithic step
    def everything(data):
        user = get_user_from_db(data["user_id"])
        if "@" in user.get("email", ""):
            send_email(user)
        update_status(user, "welcomed")
        return {"status": "done"}

5.4 Use Descriptive Names
~~~~~~~~~~~~~~~~~~~~~~~~~

Clear names help with debugging:

.. code-block:: python

    # Good
    pipeline.set_steps([
        (fetch_users, "Fetch Users from Database", "v1.0"),
        (validate_emails, "Validate Email Addresses", "v1.0"),
        (send_notifications, "Send Welcome Emails", "v1.0"),
    ])

    # Bad
    pipeline.set_steps([
        (step1, "Step 1", "v1.0"),
        (step2, "Step 2", "v1.0"),
        (step3, "Step 3", "v1.0"),
    ])

5.5 Version Your Steps
~~~~~~~~~~~~~~~~~~~~~~

Track changes with version strings:

.. code-block:: python

    pipeline.set_steps([
        (fetch_data, "Fetch Data", "v1.0"),      # Initial version
        (process_data, "Process Data", "v1.0"),
    ])

    # Later, update to new version
    pipeline.set_steps([
        (fetch_data_v2, "Fetch Data", "v2.0"),    # Updated version
        (process_data_v2, "Process Data", "v2.0"),
    ])

6. Data Flow Examples
----------------------

6.1 Accumulating Data
~~~~~~~~~~~~~~~~~~~~~

Each step adds to the accumulated data:

.. code-block:: python

    def step1(data):
        return {"a": 1}

    def step2(data):
        # Can access data from step1
        return {"b": data["a"] + 1}

    def step3(data):
        # Can access data from step1 and step2
        return {"c": data["a"] + data["b"]}

    pipeline.set_steps([
        (step1, "Step 1", "v1.0"),
        (step2, "Step 2", "v1.0"),
        (step3, "Step 3", "v1.0"),
    ])

    result = pipeline.run({})
    # result = {'a': 1, 'b': 2, 'c': 3}

6.2 Modifying Existing Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Steps can modify existing values:

.. code-block:: python

    def add_field(data):
        return {"z": data.get("y", 0) + data.get("x", 0)}

    def transform_fields(data):
        return {
            "x": data["x"] * 2,
            "y": data["y"] * 3,
            "z": data["z"] * 4,
        }

    def clean_fields(data):
        return {
            "x": int(data["x"]),
            "y": int(data["y"]),
            "z": int(data["z"]),
        }

6.3 Conditional Data
~~~~~~~~~~~~~~~~~~~~

Different branches produce different data:

.. code-block:: python

    def check_mode(data):
        mode = data.get("mode", "normal")
        return {"mode": mode}

    def normal_processing(data):
        return {"result": data["value"] * 1}

    def special_processing(data):
        return {"result": data["value"] * 10}

7. Pipeline Execution
----------------------

7.1 Synchronous Execution
~~~~~~~~~~~~~~~~~~~~~~~~~~

Standard blocking execution:

.. code-block:: python

    result = pipeline.run({"input": "value"})
    print(result)  # Blocks until complete

7.2 With Initial Data
~~~~~~~~~~~~~~~~~~~~~

Pass initial data to the pipeline:

.. code-block:: python

    initial_data = {
        "user_id": 123,
        "action": "process",
        "options": {"verbose": True},
    }

    result = pipeline.run(initial_data)

7.3 Verbose Output
~~~~~~~~~~~~~~~~~~~

Enable detailed logging:

.. code-block:: python

    # Via constructor
    pipeline = Pipeline(verbose=True)

    # Via run method
    result = pipeline.run(data, verbose=True)

**Verbose output shows:**

- Step names as they execute
- Step completion status
- Final results

7.4 Error Handling
~~~~~~~~~~~~~~~~~~

Wrap execution in try/except:

.. code-block:: python

    from wpipe.exception import TaskError

    try:
        result = pipeline.run({"x": 5})
    except TaskError as e:
        print(f"Pipeline failed at step: {e.step_name}")
        print(f"Error: {e.original_error}")
        print(f"Partial results: {e.partial_results if hasattr(e, 'partial_results') else 'N/A'}")

8. Pipeline Reuse
-----------------

8.1 Reconfigure Steps
~~~~~~~~~~~~~~~~~~~~~

Same pipeline, different steps:

.. code-block:: python

    pipeline = Pipeline()

    # First configuration
    pipeline.set_steps([
        (step_a, "Task A", "v1.0"),
        (step_b, "Task B", "v1.0"),
    ])
    result1 = pipeline.run({"x": 1})

    # Second configuration
    pipeline.set_steps([
        (step_c, "Task C", "v1.0"),
        (step_d, "Task D", "v1.0"),
    ])
    result2 = pipeline.run({"x": 2})

8.2 Reuse with Different Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Same steps, different data:

.. code-block:: python

    pipeline = Pipeline()
    pipeline.set_steps([
        (fetch_user, "Fetch User", "v1.0"),
        (process_user, "Process User", "v1.0"),
    ])

    for user_id in [1, 2, 3]:
        result = pipeline.run({"user_id": user_id})
        print(result)

9. Advanced Patterns
---------------------

9.1 Pipeline Factory
~~~~~~~~~~~~~~~~~~~~~

Create pipelines programmatically:

.. code-block:: python

    def create_pipeline(config: dict) -> Pipeline:
        pipeline = Pipeline(verbose=config.get("verbose", False))

        steps = []
        for step_config in config["steps"]:
            step_func = globals()[step_config["function"]]
            steps.append((
                step_func,
                step_config["name"],
                step_config["version"],
            ))

        pipeline.set_steps(steps)
        return pipeline

    config = {
        "verbose": True,
        "steps": [
            {"function": "fetch_data", "name": "Fetch", "version": "v1.0"},
            {"function": "process_data", "name": "Process", "version": "v1.0"},
        ],
    }

    pipeline = create_pipeline(config)

9.2 Composable Pipelines
~~~~~~~~~~~~~~~~~~~~~~~~

Build pipelines from smaller pipelines:

.. code-block:: python

    # Sub-pipeline for data loading
    load_pipeline = Pipeline()
    load_pipeline.set_steps([
        (fetch_users, "Fetch Users", "v1.0"),
        (fetch_orders, "Fetch Orders", "v1.0"),
    ])

    # Sub-pipeline for processing
    process_pipeline = Pipeline()
    process_pipeline.set_steps([
        (join_data, "Join Data", "v1.0"),
        (aggregate, "Aggregate", "v1.0"),
    ])

    # Main pipeline
    main_pipeline = Pipeline()
    main_pipeline.set_steps([
        (load_pipeline.run, "Load Data", "v1.0"),
        (process_pipeline.run, "Process Data", "v1.0"),
        (save_results, "Save Results", "v1.0"),
    ])

10. Troubleshooting
--------------------

10.1 Step Not Returning Dict
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Error: "Step must return a dictionary"

.. code-block:: python

    # Wrong
    def bad_step(data):
        return None  # Error!

    # Correct
    def good_step(data):
        return {}  # Always return dict

10.2 Missing Key in Data
~~~~~~~~~~~~~~~~~~~~~~~~

Error: KeyError when accessing data

.. code-block:: python

    # Wrong - assumes key exists
    def bad_step(data):
        return {"result": data["x"] * 2}  # KeyError if 'x' missing

    # Correct - use .get() with default
    def good_step(data):
        return {"result": data.get("x", 0) * 2}

10.3 Step Order Matters
~~~~~~~~~~~~~~~~~~~~~~~~

Data dependencies must be satisfied:

.. code-block:: python

    # Wrong order - step2 depends on step1's output
    pipeline.set_steps([
        (step2, "Step 2", "v1.0"),  # Fails - data["result"] missing
        (step1, "Step 1", "v1.0"),
    ])

    # Correct order
    pipeline.set_steps([
        (step1, "Step 1", "v1.0"),  # step1 runs first
        (step2, "Step 2", "v1.0"),  # step2 can use step1's output
    ])

11. Next Steps
--------------

Now that you understand pipeline basics:

- Learn about :doc:`conditions` for conditional execution
- Explore :doc:`retry` for automatic retries on failure
- Check :doc:`api_integration` for API tracking
- See :doc:`nested_pipelines` for complex workflows
