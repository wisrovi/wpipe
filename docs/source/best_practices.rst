Best Practices
==============

This guide covers recommended patterns and practices for building robust, maintainable pipelines with wpipe.

.. contents::
   :local:
   :depth: 3

1. Pipeline Design Principles
------------------------------

1.1 Single Responsibility
~~~~~~~~~~~~~~~~~~~~~~~~~~

Each step should do one thing well:

.. code-block:: python

    # Good: Focused steps
    def validate_email(data):
        """Validate email format."""
        email = data.get("email", "")
        if "@" not in email:
            raise ValueError("Invalid email format")
        return {"email_valid": True}

    def normalize_name(data):
        """Normalize the name field."""
        name = data.get("name", "").strip().title()
        return {"name": name}

    # Avoid: Multi-purpose steps
    def validate_and_transform(data):
        # This mixes concerns - split it up
        ...

1.2 Pure Functions
~~~~~~~~~~~~~~~~~

Step functions should be pure when possible:

.. code-block:: python

    # Good: Pure function - same input always produces same output
    def calculate_total(data):
        subtotal = data["subtotal"]
        tax = subtotal * 0.1
        return {"total": subtotal + tax}

    # Avoid: Side effects in step functions
    def calculate_and_log(data):
        result = data["price"] * 2
        print(f"Calculated: {result}")  # Side effect
        return {"result": result}

1.3 Fail Fast
~~~~~~~~~~~~~

Validate input early in the pipeline:

.. code-block:: python

    def validate_input(data):
        """First step - validate everything."""
        required = ["email", "name", "age"]
        for field in required:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        if not isinstance(data["age"], int):
            raise ValueError("Age must be an integer")
        
        if data["age"] < 0 or data["age"] > 150:
            raise ValueError("Age must be between 0 and 150")
        
        return {"validation_passed": True}

2. Step Function Best Practices
--------------------------------

2.1 Type Hints
~~~~~~~~~~~~~~

Always use type hints for better IDE support:

.. code-block:: python

    from typing import Dict, Any

    def process_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Process user data.
        
        Args:
            data: Input dictionary with user information
            
        Returns:
            Dictionary with processed results
        """
        value: int = data.get("value", 0)
        result: int = value * 2
        return {"result": result}

2.2 Docstrings
~~~~~~~~~~~~~~

Include clear docstrings:

.. code-block:: python

    def fetch_user_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch user data from the database.
        
        This step connects to the database and retrieves user information
        based on the user_id provided in the input data.
        
        Args:
            data: Dictionary containing 'user_id'
            
        Returns:
            Dictionary with user data
            
        Raises:
            ConnectionError: If database connection fails
        """
        user_id = data["user_id"]
        user_data = database.fetch(user_id)
        return {"user": user_data}

2.3 Meaningful Names
~~~~~~~~~~~~~~~~~~~~

Use descriptive step names:

.. code-block:: python

    # Good: Clear, descriptive names
    pipeline.set_steps([
        (fetch_user_from_database, "Fetch User from Database", "v1.0"),
        (validate_email_format, "Validate Email Format", "v1.0"),
        (encrypt_sensitive_data, "Encrypt Sensitive Data", "v1.0"),
        (save_to_database, "Save User to Database", "v1.0"),
    ])

    # Avoid: Vague names
    pipeline.set_steps([
        (step1, "Step 1", "v1.0"),
        (step2, "Step 2", "v1.0"),
    ])

3. Error Handling Patterns
--------------------------

3.1 Specific Error Codes
~~~~~~~~~~~~~~~~~~~~~~~~~

Use appropriate error codes:

.. code-block:: python

    from wpipe.exception import TaskError, Codes

    def validate_input(data):
        if "email" not in data:
            raise TaskError("Email is required", Codes.VALIDATION_ERROR)
        
        if "@" not in data["email"]:
            raise TaskError("Invalid email format", Codes.VALIDATION_ERROR)
        
        return data

3.2 Graceful Degradation
~~~~~~~~~~~~~~~~~~~~~~~~

Handle failures gracefully:

.. code-block:: python

    def fetch_with_fallback(data):
        """Fetch with fallback on failure."""
        try:
            return {"data": fetch_from_primary()}
        except Exception:
            # Fallback to cache
            try:
                return {"data": get_from_cache()}
            except Exception:
                # Last resort - return empty
                return {"data": [], "source": "none"}

3.3 Error Context
~~~~~~~~~~~~~~~~~

Include helpful error information:

.. code-block:: python

    import traceback

    def step_with_context(data):
        try:
            return process(data)
        except Exception as e:
            raise TaskError(
                f"Step failed: {e}",
                Codes.TASK_FAILED
            ) from e

4. Configuration Management
---------------------------

4.1 Use Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import os

    def get_config():
        return {
            "api_url": os.environ.get("API_URL", "http://localhost:8418"),
            "api_token": os.environ["API_TOKEN"],  # Required
            "debug": os.environ.get("DEBUG", "false").lower() == "true",
            "timeout": int(os.environ.get("TIMEOUT", "30")),
        }

4.2 YAML Configuration
~~~~~~~~~~~~~~~~~~~~~

Separate configuration from code:

.. code-block:: yaml

    # config/production.yaml
    pipeline:
      name: "data_processor"
      version: "1.0.0"
      verbose: true
      max_retries: 3
      retry_delay: 2.0

    api:
      base_url: ${API_BASE_URL}
      token: ${API_TOKEN}

    database:
      path: ${DB_PATH:-data.db}

5. Performance Optimization
---------------------------

5.1 Lazy Evaluation
~~~~~~~~~~~~~~~~~~~

Don't do unnecessary work:

.. code-block:: python

    def optimized_step(data):
        # Only process if needed
        if not data.get("process"):
            return {"skipped": True}
        
        # Actual processing
        return process(data)

5.2 Batch Processing
~~~~~~~~~~~~~~~~~~~~

Process data in batches when possible:

.. code-block:: python

    def batch_process(data):
        items = data.get("items", [])
        
        # Process in batches of 100
        batch_size = 100
        results = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            results.extend(process_batch(batch))
        
        return {"results": results}

6. Testing Best Practices
-------------------------

6.1 Test Each Step
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def test_step():
        # Arrange
        data = {"value": 10}
        
        # Act
        result = double_value(data)
        
        # Assert
        assert result == {"value": 20}

6.2 Integration Tests
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def test_pipeline():
        pipeline = Pipeline()
        pipeline.set_steps([
            (lambda d: {"x": 5}, "Init", "v1.0"),
            (lambda d: {"y": d["x"] * 2}, "Double", "v1.0"),
        ])
        
        result = pipeline.run({})
        
        assert result["x"] == 5
        assert result["y"] == 10

7. Logging Strategy
-------------------

7.1 Structured Logging
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import logging

    logger = logging.getLogger(__name__)

    def logged_step(data):
        logger.info(f"Processing request", extra={
            "user_id": data.get("user_id"),
            "step": "process_data"
        })
        
        try:
            result = process(data)
            logger.info(f"Success", extra={"result": result})
            return result
        except Exception as e:
            logger.error(f"Failed: {e}", extra={"error": str(e)})
            raise

8. Security Considerations
--------------------------

8.1 Never Log Secrets
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def safe_logging(data):
        # Good: Don't log sensitive data
        logger.info(f"Processing user: {user_id}")
        
        # Bad: Never do this
        logger.info(f"Token: {api_token}")  # Security risk!

8.2 Validate Input
~~~~~~~~~~~~~~~~~~

Always validate external input:

.. code-block:: python

    def validate_external_data(data):
        # Sanitize and validate all external input
        if "amount" in data:
            amount = float(data["amount"])
            if amount < 0 or amount > 1000000:
                raise ValueError("Amount out of valid range")
        
        return data

9. Code Organization
-------------------

9.1 Project Structure
~~~~~~~~~~~~~~~~~~~~~

::

    my_pipeline/
    ├── pipeline.py           # Main pipeline definition
    ├── steps/
    │   ├── __init__.py
    │   ├── fetch.py         # Data fetching steps
    │   ├── transform.py     # Transformation steps
    │   └── save.py          # Storage steps
    ├── config/
    │   ├── __init__.py
    │   └── settings.py      # Configuration
    ├── tests/
    │   ├── test_steps.py
    │   └── test_pipeline.py
    └── requirements.txt

9.2 Reusable Step Library
~~~~~~~~~~~~~~~~~~~~~~~~~

Create a library of reusable steps:

.. code-block:: python

    # steps/base.py
    class BaseStep:
        """Base class for pipeline steps."""
        
        def __init__(self, config: dict = None):
            self.config = config or {}
        
        def __call__(self, data: dict) -> dict:
            raise NotImplementedError

    # steps/validators.py
    class ValidateEmail(BaseStep):
        def __call__(self, data: dict) -> dict:
            email = data.get(self.config.get("field", "email"))
            if "@" not in email:
                raise ValueError("Invalid email")
            return data

10. Production Checklist
------------------------

Before deploying to production:

- [ ] All steps have type hints
- [ ] Error handling is comprehensive
- [ ] Logging is configured appropriately
- [ ] Configuration uses environment variables
- [ ] Tests cover all critical paths
- [ ] Retry logic is configured for transient failures
- [ ] Timeouts are set on external calls
- [ ] No secrets are logged or hardcoded

11. Common Pitfalls
------------------

11.1 Mutable Default Arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Bad: Mutable default argument
    def step(data, items=[]):
        items.append(data.get("item", ""))
        return {"items": items}

    # Good: Default to None
    def step(data, items=None):
        items = items or []
        items.append(data.get("item", ""))
        return {"items": items}

11.2 Forgetting Return Type
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Bad: Forgot to return dict
    def step(data):
        result = data["value"] * 2
        # Forgot return!

    # Good: Always return dict
    def step(data):
        result = data["value"] * 2
        return {"result": result}

11.3 Not Checking Keys
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Bad: Will raise KeyError
    def step(data):
        return {"value": data["missing_key"]}

    # Good: Safe access
    def step(data):
        return {"value": data.get("missing_key", "default")}