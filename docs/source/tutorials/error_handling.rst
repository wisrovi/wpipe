Error Handling Tutorial
=======================

This tutorial covers implementing robust error handling in your wpipe pipelines.

.. contents::
   :local:
   :depth: 2

1. Introduction
--------------

Proper error handling is crucial for production pipelines. wpipe provides comprehensive error handling through custom exceptions and error codes.

2. Understanding Exceptions
--------------------------

2.1 TaskError
~~~~~~~~~~~~~

The primary exception in wpipe is ``TaskError``:

.. code-block:: python

    from wpipe.exception import TaskError

    try:
        result = pipeline.run(data)
    except TaskError as e:
        print(f"Error: {e}")
        print(f"Code: {e.error_code}")

2.2 Error Codes
~~~~~~~~~~~~~~~

wpipe defines standard error codes:

.. code-block:: python

    from wpipe.exception import Codes

    print(Codes.TASK_FAILED)        # 502
    print(Codes.API_ERROR)          # 501
    print(Codes.UPDATE_PROCESS_ERROR)  # 504
    print(Codes.UPDATE_TASK)        # 505
    print(Codes.UPDATE_PROCESS_OK)  # 503

3. Raising TaskError
--------------------

3.1 Basic Usage
~~~~~~~~~~~~~~~

Raise TaskError from step functions:

.. code-block:: python

    from wpipe.exception import TaskError, Codes

    def validate_input(data):
        """Validate input data."""
        if "email" not in data:
            raise TaskError(
                "Email is required",
                Codes.VALIDATION_ERROR
            )
        
        if "@" not in data["email"]:
            raise TaskError(
                "Invalid email format",
                Codes.VALIDATION_ERROR
            )
        
        return {"validated": True}

3.2 With Step Information
~~~~~~~~~~~~~~~~~~~~~~~~

Include step name in errors:

.. code-block:: python

    def process_data(data):
        try:
            # Processing logic
            return {"result": "success"}
        except ValueError as e:
            raise TaskError(
                f"Processing failed: {e}",
                Codes.TASK_FAILED
            ) from e

4. Catching Errors
------------------

4.1 Basic Catch
~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe import Pipeline
    from wpipe.exception import TaskError

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (validate_input, "Validate", "v1.0"),
        (process_data, "Process", "v1.0"),
    ])

    try:
        result = pipeline.run({"email": "invalid"})
    except TaskError as e:
        print(f"Pipeline failed at step")
        print(f"Error: {e}")
        print(f"Code: {e.error_code}")

4.2 Specific Error Codes
~~~~~~~~~~~~~~~~~~~~~~~~

Handle different error types differently:

.. code-block:: python

    from wpipe.exception import TaskError, Codes

    try:
        result = pipeline.run(data)
    except TaskError as e:
        if e.error_code == Codes.VALIDATION_ERROR:
            print("Validation failed - check input data")
        elif e.error_code == Codes.API_ERROR:
            print("API error - check network/API")
        elif e.error_code == Codes.TASK_FAILED:
            print("Task failed - check logs")
        else:
            print(f"Unknown error: {e}")

5. Error Recovery
-----------------

5.1 Graceful Degradation
~~~~~~~~~~~~~~~~~~~~~~~~

Handle errors and continue:

.. code-block:: python

    def safe_step(data):
        """Step that handles errors gracefully."""
        try:
            result = risky_operation(data)
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "fallback", "error": str(e)}

5.2 Fallback Values
~~~~~~~~~~~~~~~~~~~

Provide default values on failure:

.. code-block:: python

    def fetch_with_fallback(data):
        """Fetch with fallback on failure."""
        try:
            return {"data": fetch_from_api()}
        except Exception:
            return {"data": get_cached_data()}

6. Validation Patterns
----------------------

6.1 Early Validation
~~~~~~~~~~~~~~~~~~~~

Validate at the start of the pipeline:

.. code-block:: python

    def validate_pipeline_input(data):
        """Validate all required fields exist."""
        required = ["email", "name", "age"]
        missing = [f for f in required if f not in data]
        
        if missing:
            raise TaskError(
                f"Missing required fields: {missing}",
                Codes.VALIDATION_ERROR
            )
        
        # Validate types
        if not isinstance(data["age"], int):
            raise TaskError(
                "Age must be an integer",
                Codes.VALIDATION_ERROR
            )
        
        if data["age"] < 0 or data["age"] > 150:
            raise TaskError(
                "Age must be between 0 and 150",
                Codes.VALIDATION_ERROR
            )
        
        return data

6.2 Chain Validation
~~~~~~~~~~~~~~~~~~~~

Validate at each step:

.. code-block:: python

    class ValidatingStep:
        """Step with built-in validation."""
        
        def __init__(self, required_fields: list):
            self.required_fields = required_fields
        
        def __call__(self, data: dict) -> dict:
            # Check required fields exist
            missing = [f for f in self.required_fields if f not in data]
            if missing:
                raise TaskError(
                    f"Missing fields: {missing}",
                    Codes.VALIDATION_ERROR
                )
            
            # Process
            return {"processed": True}

7. API Error Handling
---------------------

7.1 Handle API Failures
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def call_api_with_retry(data):
        """Call API with error handling."""
        from wpipe import APIClient
        
        client = APIClient(base_url="http://api.example.com", token="...")
        
        try:
            result = client.send_post("/process", data)
            if result is None:
                raise TaskError("API returned no result", Codes.API_ERROR)
            return {"api_result": result}
        except Exception as e:
            raise TaskError(f"API call failed: {e}", Codes.API_ERROR) from e

7.2 Timeout Handling
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import requests
    from wpipe.exception import TaskError, Codes

    def call_with_timeout(data, timeout=5):
        """Call with timeout handling."""
        try:
            response = requests.post(
                "http://api.example.com/process",
                json=data,
                timeout=timeout
            )
            return {"response": response.json()}
        except requests.Timeout:
            raise TaskError("API request timed out", Codes.TIMEOUT_ERROR)
        except requests.RequestException as e:
            raise TaskError(f"API request failed: {e}", Codes.API_ERROR)

8. Custom Error Classes
-----------------------

8.1 Define Custom Errors
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe.exception import TaskError

    class ValidationError(TaskError):
        """Custom validation error."""
        pass

    class ProcessingError(TaskError):
        """Custom processing error."""
        pass

8.2 Use Custom Errors
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe.exception import Codes

    class ValidationError(TaskError):
        def __init__(self, message: str):
            super().__init__(message, Codes.VALIDATION_ERROR)

    def validate(data):
        if not data.get("name"):
            raise ValidationError("Name is required")
        return data

9. Error Logging
---------------

9.1 Log Errors
~~~~~~~~~~~~~~

.. code-block:: python

    import logging

    logger = logging.getLogger(__name__)

    def logged_step(data):
        """Step with error logging."""
        try:
            return process(data)
        except Exception as e:
            logger.error(f"Step failed: {e}", exc_info=True)
            raise

9.2 Error Context
~~~~~~~~~~~~~~~~

Add context to errors:

.. code-block:: python

    import traceback

    def step_with_context(data):
        try:
            return risky_operation(data)
        except Exception as e:
            # Add context to error
            error_context = {
                "input_keys": list(data.keys()),
                "error_type": type(e).__name__,
                "traceback": traceback.format_exc()
            }
            raise TaskError(
                f"Step failed: {e}",
                Codes.TASK_FAILED
            ) from e

10. Complete Example
-------------------

Here's a complete error handling example:

.. code-block:: python

    from wpipe import Pipeline
    from wpipe.exception import TaskError, Codes
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


    class ErrorHandlingPipeline(Pipeline):
        """Pipeline with comprehensive error handling."""
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        
        def run(self, *args, **kwargs):
            try:
                return super().run(*args, **kwargs)
            except TaskError as e:
                logger.error(f"Task failed: {e}")
                logger.error(f"Error code: {e.error_code}")
                raise
            except Exception as e:
                logger.critical(f"Unexpected error: {e}")
                raise TaskError(str(e), Codes.UNKNOWN_ERROR) from e


    # Define steps with error handling
    def validate_input(data):
        """Validate input data."""
        if "value" not in data:
            raise TaskError("Missing 'value' in input", Codes.VALIDATION_ERROR)
        
        if not isinstance(data["value"], (int, float)):
            raise TaskError("'value' must be a number", Codes.VALIDATION_ERROR)
        
        if data["value"] < 0:
            raise TaskError("'value' must be non-negative", Codes.VALIDATION_ERROR)
        
        return {"validated": True}


    def process_value(data):
        """Process the validated value."""
        value = data["value"]
        
        if value > 1000:
            raise TaskError("Value too large for processing", Codes.TASK_FAILED)
        
        return {"processed_value": value * 2}


    def format_result(data):
        """Format the result."""
        return {
            "output": f"Processed: {data['processed_value']}",
            "success": True
        }


    # Create and run pipeline
    pipeline = ErrorHandlingPipeline(verbose=True)
    pipeline.set_steps([
        (validate_input, "Validate Input", "v1.0"),
        (process_value, "Process Value", "v1.0"),
        (format_result, "Format Result", "v1.0"),
    ])

    # Test with valid data
    result = pipeline.run({"value": 50})
    print(f"Success: {result}")

    # Test with invalid data
    try:
        result = pipeline.run({"value": -1})
    except TaskError as e:
        print(f"Handled error: {e}")

11. Best Practices
------------------

1. **Validate early** - Check inputs at the start of the pipeline
2. **Fail fast** - Raise errors immediately when problems are detected
3. **Provide context** - Include useful information in error messages
4. **Use specific codes** - Choose the most appropriate error code
5. **Log errors** - Record errors for debugging
6. **Handle gracefully** - Plan for failures and provide fallbacks

12. Next Steps
--------------

- :doc:`retry_logic` - Add automatic retries
- :doc:`conditions` - Handle different error scenarios
- :doc:`production_deployment` - Deploy to production