Tutorials
=========

This section contains step-by-step tutorials for learning how to use wpipe.

1. Basic Pipeline Tutorial
-------------------------

This tutorial covers creating your first pipeline with wpipe.

1.1 What You'll Learn
~~~~~~~~~~~~~~~~~~~~~

- Create a basic pipeline
- Define step functions
- Run the pipeline with input data
- Understand data flow between steps

1.2 Step-by-Step Instructions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Step 1: Import the Pipeline class**

.. code-block:: python

    from wpipe import Pipeline

**Step 2: Define your step functions**

Each step receives data and returns modified data:

.. code-block:: python

    def load_data(data):
        """Load initial data for processing."""
        return {"numbers": [1, 2, 3, 4, 5]}

    def calculate_sum(data):
        """Calculate the sum of numbers."""
        numbers = data["numbers"]
        total = sum(numbers)
        return {"sum": total}

    def calculate_average(data):
        """Calculate the average of numbers."""
        numbers = data["numbers"]
        average = sum(numbers) / len(numbers)
        return {"average": average}

**Step 3: Create and configure the pipeline**

.. code-block:: python

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (load_data, "Load Data", "v1.0"),
        (calculate_sum, "Calculate Sum", "v1.0"),
        (calculate_average, "Calculate Average", "v1.0"),
    ])

**Step 4: Run the pipeline**

.. code-block:: python

    result = pipeline.run({})

    print(result)
    # {'numbers': [1, 2, 3, 4, 5], 'sum': 15, 'average': 3.0}

1.3 Complete Example
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe import Pipeline

    def load_data(data):
        return {"numbers": [1, 2, 3, 4, 5]}

    def calculate_sum(data):
        return {"sum": sum(data["numbers"])}

    def calculate_average(data):
        return {"average": sum(data["numbers"]) / len(data["numbers"])}

    def format_result(data):
        return {
            "formatted": f"Sum: {data['sum']}, Avg: {data['average']}"
        }

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (load_data, "Load Data", "v1.0"),
        (calculate_sum, "Calculate Sum", "v1.0"),
        (calculate_average, "Calculate Average", "v1.0"),
        (format_result, "Format Result", "v1.0"),
    ])

    result = pipeline.run({})
    print(result["formatted"])  # Sum: 15, Avg: 3.0

2. Using Classes as Steps
-------------------------

This tutorial shows how to use classes with the ``__call__`` method as pipeline steps.

2.1 Why Use Classes?
~~~~~~~~~~~~~~~~~~~~

Classes are useful when you need to:

- Maintain state between calls
- Configure step behavior at initialization
- Encapsulate related functionality

2.2 Creating a Step Class
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class DataTransformer:
        def __init__(self, multiplier: float, offset: float = 0):
            """Initialize the transformer.
            
            Args:
                multiplier: Value to multiply by
                offset: Value to add after multiplication
            """
            self.multiplier = multiplier
            self.offset = offset

        def __call__(self, data: dict) -> dict:
            """Transform the data.
            
            Args:
                data: Input data dictionary
                
            Returns:
                Data with transformed values
            """
            value = data["value"]
            transformed = value * self.multiplier + self.offset
            return {"transformed": transformed}

2.3 Using the Class in a Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe import Pipeline

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (DataTransformer(2.0, 10.0), "Double and Add Ten", "v1.0"),
        (DataTransformer(3.0), "Triple", "v1.0"),
    ])

    result = pipeline.run({"value": 5})
    # First step: 5 * 2.0 + 10 = 20
    # Second step: 20 * 3.0 = 60
    print(result)  # {'value': 5, 'transformed': 60}

2.4 Stateful Processing
~~~~~~~~~~~~~~~~~~~~~~~

Classes can maintain state across multiple steps:

.. code-block:: python

    class RunningTotal:
        def __init__(self):
            self.total = 0

        def __call__(self, data: dict) -> dict:
            self.total += data.get("value", 0)
            return {"running_total": self.total}

    pipeline = Pipeline()
    pipeline.set_steps([
        (RunningTotal(), "Add 10", "v1.0"),
        (RunningTotal(), "Add 20", "v1.0"),
        (RunningTotal(), "Add 30", "v1.0"),
    ])

    result = pipeline.run({"value": 10})
    print(result["running_total"])  # 60 (10 + 20 + 30)

3. API Integration Tutorial
----------------------------

This tutorial covers integrating your pipeline with an external API.

3.1 Prerequisites
~~~~~~~~~~~~~~~~~

You'll need:

- An API server running (or mock server)
- API endpoint URL
- Authentication token

3.2 Basic API Setup
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    api_config = {
        "base_url": "http://localhost:8418",
        "token": "my-secure-token"
    }

    pipeline = Pipeline(api_config=api_config)

3.3 Registering a Worker
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    worker_id = pipeline.worker_register(
        name="data_processor",
        version="1.0.0"
    )

    print(f"Registered worker ID: {worker_id}")
    # {'id': 'worker_123', 'name': 'data_processor', ...}

    # Set the worker ID for subsequent operations
    pipeline.set_worker_id(worker_id.get("id"))

3.4 Reporting Task Status
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def process_data(data):
        # Your processing logic here
        return {"result": data["input"] * 2}

    pipeline.set_steps([
        (process_data, "Process Data", "v1.0"),
    ])

    # The pipeline will automatically report status to the API

3.5 Health Checks
~~~~~~~~~~~~~~~~~

Configure automatic health checks:

.. code-block:: python

    pipeline = Pipeline(
        api_config=api_config,
        health_check_interval=60  # Check every 60 seconds
    )

4. Error Handling Tutorial
-------------------------

This tutorial covers robust error handling in pipelines.

4.1 Basic Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe.exception import TaskError

    def risky_operation(data):
        if data.get("value", 0) < 0:
            raise ValueError("Value cannot be negative")
        return {"result": data["value"] * 2}

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (risky_operation, "Risky Operation", "v1.0"),
    ])

    try:
        result = pipeline.run({"value": -1})
    except TaskError as e:
        print(f"Pipeline failed: {e}")
        print(f"Failed at step: {e.step_name}")

4.2 Custom Error Codes
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe.exception import TaskError, Codes

    def validate_input(data):
        if "email" not in data:
            raise TaskError(
                "Email is required",
                step_name="Validate Input",
                code=Codes.VALIDATION_ERROR
            )
        return data

4.3 Recoverable vs Non-Recoverable Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe.exception import Codes

    def network_call(data):
        """Network errors are typically recoverable."""
        try:
            return {"data": fetch_from_api()}
        except NetworkError:
            raise TaskError(
                "Network error occurred",
                code=Codes.RETRYABLE_ERROR
            )

    def invalid_input(data):
        """Validation errors are not recoverable."""
        if not validate(data):
            raise TaskError(
                "Invalid input data",
                code=Codes.VALIDATION_ERROR
            )

5. Retry Logic Tutorial
-----------------------

This tutorial covers implementing automatic retries for failed steps.

5.1 Manual Retry Implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def unreliable_step(data):
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                return call_unreliable_api()
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise
                print(f"Attempt {attempt + 1} failed, retrying...")

5.2 Using the Retry Decorator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from functools import wraps

    def retry(max_attempts=3, delay=1.0):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(max_attempts):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        if attempt == max_attempts - 1:
                            raise
                        print(f"Retry {attempt + 1}/{max_attempts}")
                return None
            return wrapper
        return decorator

    @retry(max_attempts=3, delay=2.0)
    def may_fail(data):
        # Implementation here
        ...

6. Nested Pipelines Tutorial
----------------------------

This tutorial shows how to compose pipelines together.

6.1 Creating Nested Pipelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe import Pipeline

    # Create the inner pipeline
    inner_pipeline = Pipeline(verbose=True)
    inner_pipeline.set_steps([
        (lambda d: {"inner_result": d["x"] * 2}, "Inner Step 1", "v1.0"),
        (lambda d: {"inner_squared": d["inner_result"] ** 2}, "Inner Step 2", "v1.0"),
    ])

    # Create the outer pipeline
    outer_pipeline = Pipeline(verbose=True)
    outer_pipeline.set_steps([
        (lambda d: {"x": 5}, "Initialize", "v1.0"),
        (inner_pipeline.run, "Run Inner", "v1.0"),
        (lambda d: {"final": d.get("inner_squared", 0) + 10}, "Finalize", "v1.0"),
    ])

    result = outer_pipeline.run({})
    # x=5 -> inner_result=10 -> inner_squared=100 -> final=110
    print(result["final"])  # 110

6.2 Reusing Pipeline Logic
~~~~~~~~~~~~~~~~~~~~~~~~~~

Define reusable pipeline factories:

.. code-block:: python

    def create_processing_pipeline(name: str, multiplier: float):
        """Factory function for creating processing pipelines."""
        pipeline = Pipeline()
        pipeline.set_steps([
            (lambda d: {"step1": d["input"] * multiplier}, f"{name} Step 1", "v1.0"),
            (lambda d: {"step2": d["step1"] + 1}, f"{name} Step 2", "v1.0"),
        ])
        return pipeline

    pipeline1 = create_processing_pipeline("data1", 2.0)
    pipeline2 = create_processing_pipeline("data2", 3.0)

7. SQLite Integration Tutorial
------------------------------

This tutorial covers persisting pipeline execution results.

7.1 Basic SQLite Usage
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe import Pipeline
    from wpipe.sqlite import Wsqlite

    pipeline = Pipeline()
    pipeline.set_steps([
        (lambda d: {"result": d["x"] * 2}, "Process", "v1.0"),
    ])

    with Wsqlite(db_name="pipeline_results.db") as db:
        input_data = {"x": 10}
        db.input = input_data
        
        result = pipeline.run(input_data)
        db.output = result

7.2 Querying Results
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe.sqlite import Wsqlite

    with Wsqlite(db_name="pipeline_results.db") as db:
        # Get the last execution
        cursor = db.execute("SELECT * FROM pipeline_executions ORDER BY id DESC LIMIT 1")
        last_execution = cursor.fetchone()

7.3 Multiple Executions
~~~~~~~~~~~~~~~~~~~~~~~

Track multiple pipeline runs:

.. code-block:: python

    from wpipe import Pipeline
    from wpipe.sqlite import Wsqlite

    pipeline = Pipeline()
    pipeline.set_steps([
        (lambda d: {"processed": d["value"] * 2}, "Process", "v1.0"),
    ])

    test_cases = [
        {"value": 1},
        {"value": 2},
        {"value": 3},
    ]

    with Wsqlite(db_name="test_results.db") as db:
        for test_data in test_cases:
            db.input = test_data
            result = pipeline.run(test_data)
            db.output = result

8. YAML Configuration Tutorial
------------------------------

This tutorial covers loading pipeline configuration from YAML files.

8.1 Creating a Configuration File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    # pipeline_config.yaml
    pipeline:
      name: "data_processing"
      version: "1.0.0"
      verbose: true

    api:
      base_url: "http://localhost:8418"
      token: "your-token-here"

    logging:
      level: "INFO"
      file: "pipeline.log"

8.2 Loading Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe.util import load_config

    config = load_config("pipeline_config.yaml")

    pipeline = Pipeline(
        verbose=config["pipeline"]["verbose"],
        api_config=config["api"]
    )

8.3 Environment Variables in YAML
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    # config.yaml
    api:
      token: ${API_TOKEN}  # Will be replaced with environment variable

    database:
      path: ${DB_PATH:-default.db}  # With default value

9. Advanced Patterns
--------------------

9.1 Conditional Step Execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe import Pipeline, Condition

    pipeline = Pipeline()
    pipeline.set_steps([
        (lambda d: {"mode": "production"}, "Detect Mode", "v1.0"),
    ])

    pipeline.add_condition(
        condition=Condition(data_key="mode", operator="==", value="production"),
        then_steps=[(process_production, "Process Production", "v1.0")],
        else_steps=[(process_staging, "Process Staging", "v1.0")],
    )

9.2 Parallel Execution
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

9.3 Pipeline Callbacks
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def on_step_complete(step_name, result):
        print(f"Step {step_name} completed with result: {result}")

    def on_pipeline_complete(final_result):
        print(f"Pipeline complete: {final_result}")

    pipeline = Pipeline(callbacks={
        "on_step_complete": on_step_complete,
        "on_pipeline_complete": on_pipeline_complete,
    })

10. Best Practices
-----------------

10.1 Step Functions Should Be Pure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Avoid side effects in step functions:

.. code-block:: python

    # Good: Pure function
    def add_numbers(data):
        return {"sum": data["a"] + data["b"]}

    # Avoid: Side effects
    def add_and_print(data):
        print(data)  # Side effect
        return {"sum": data["a"] + data["b"]}

10.2 Validate Input Early
~~~~~~~~~~~~~~~~~~~~~~~~~

Catch invalid data at the start:

.. code-block:: python

    def validate_input(data):
        required_keys = ["email", "name", "age"]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing required key: {key}")
        return data

    pipeline.set_steps([
        (validate_input, "Validate", "v1.0"),
        # ... rest of steps
    ])

10.3 Use Meaningful Step Names
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Good
    pipeline.set_steps([
        (fetch_user_data, "Fetch User Data from API", "v1.0"),
        (validate_email, "Validate Email Format", "v1.0"),
        (save_to_database, "Save User to Database", "v1.0"),
    ])

    # Avoid
    pipeline.set_steps([
        (step1, "Step 1", "v1.0"),
        (step2, "Step 2", "v1.0"),
    ])
