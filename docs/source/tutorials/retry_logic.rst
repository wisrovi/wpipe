Retry Logic Tutorial
====================

This tutorial covers implementing automatic retry logic for failed pipeline steps.

.. contents::
   :local:
   :depth: 2

1. Introduction
---------------

Retry logic is essential for handling transient failures like network timeouts, temporary service unavailability, or temporary resource constraints.

2. Built-in Retry Support
--------------------------

2.1 Configuring Retries
~~~~~~~~~~~~~~~~~~~~~~~

wpipe has built-in support for retries:

.. code-block:: python

    from wpipe import Pipeline

    pipeline = Pipeline(
        verbose=True,
        max_retries=3,           # Number of retry attempts
        retry_delay=1.0,         # Seconds between retries
        retry_on_exceptions=(Exception,)  # Which exceptions to retry on
    )

2.2 How It Works
~~~~~~~~~~~~~~~~

When a step fails:
1. Pipeline catches the exception
2. Waits for ``retry_delay`` seconds
3. Attempts the step again
4. Repeats up to ``max_retries`` times
5. If all attempts fail, raises the final exception

3. Custom Retry Decorators
---------------------------

3.1 Basic Retry Decorator
~~~~~~~~~~~~~~~~~~~~~~~~~

Create a reusable retry decorator:

.. code-block:: python

    import time
    from functools import wraps

    def retry(max_attempts=3, delay=1.0, backoff=1.0):
        """Retry decorator with exponential backoff.
        
        Args:
            max_attempts: Maximum number of attempts
            delay: Initial delay between retries (seconds)
            backoff: Multiplier for delay after each retry
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                current_delay = delay
                last_exception = None
                
                for attempt in range(max_attempts):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        last_exception = e
                        if attempt < max_attempts - 1:
                            time.sleep(current_delay)
                            current_delay *= backoff
                        else:
                            raise
                
                raise last_exception
            
            return wrapper
        return decorator

3.2 Using the Decorator
~~~~~~~~~~~~~~~~~~~~~~~

Apply the decorator to your step functions:

.. code-block:: python

    @retry(max_attempts=3, delay=1.0, backoff=2.0)
    def unreliable_api_call(data):
        """Call that might fail occasionally."""
        import random
        if random.random() < 0.7:  # 70% chance of failure
            raise ConnectionError("Connection failed")
        return {"result": "success"}

4. Advanced Retry Patterns
---------------------------

4.1 Retry with Custom Logic
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def conditional_retry(max_attempts=3, delay=1.0):
        """Retry only on specific exceptions."""
        
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                retryable_exceptions = (
                    ConnectionError,
                    TimeoutError,
                    ConnectionResetError,
                )
                
                for attempt in range(max_attempts):
                    try:
                        return func(*args, **kwargs)
                    except retryable_exceptions as e:
                        if attempt < max_attempts - 1:
                            time.sleep(delay * (attempt + 1))
                        else:
                            raise
                    except Exception as e:
                        # Don't retry on other exceptions
                        raise
                        
            return wrapper
        return decorator

4.2 Retry with Logging
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import logging

    logger = logging.getLogger(__name__)

    def retry_with_logging(max_attempts=3, delay=1.0):
        """Retry with detailed logging."""
        
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(max_attempts):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_attempts} failed: {e}"
                        )
                        if attempt < max_attempts - 1:
                            logger.info(f"Retrying in {delay} seconds...")
                            time.sleep(delay)
                        else:
                            logger.error(
                                f"All {max_attempts} attempts failed"
                            )
                            raise
                            
            return wrapper
        return decorator

5. Step-Level Retries
---------------------

5.1 Independent Retry Config
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configure retries per-step:

.. code-block:: python

    class RetryableStep:
        """Step with its own retry logic."""
        
        def __init__(self, max_retries: int = 3):
            self.max_retries = max_retries
        
        def __call__(self, data: dict) -> dict:
            last_error = None
            
            for attempt in range(self.max_retries):
                try:
                    return self._execute(data)
                except Exception as e:
                    last_error = e
                    if attempt < self.max_retries - 1:
                        time.sleep(1 * (attempt + 1))
            
            raise last_error
        
        def _execute(self, data: dict) -> dict:
            # Actual implementation
            return {"result": "success"}

6. Handling Different Failure Types
------------------------------------

6.1 Network Failures
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import requests

    @retry(max_attempts=3, delay=2.0)
    def fetch_with_retry(url: str) -> dict:
        """Fetch data with retry on network failure."""
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()

6.2 Database Failures
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    @retry(max_attempts=3, delay=1.0)
    def save_to_database(data: dict) -> dict:
        """Save with retry on database errors."""
        # Connection errors, deadlocks, etc. can be retried
        connection = get_db_connection()
        try:
            connection.save(data)
            return {"saved": True}
        finally:
            connection.close()

7. Timeout Handling
------------------

7.1 Combined Retry and Timeout
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import signal
    from functools import wraps

    class TimeoutError(Exception):
        pass

    def timeout_handler(signum, frame):
        raise TimeoutError("Operation timed out")

    def retry_with_timeout(max_attempts=3, delay=1.0, timeout_seconds=5):
        """Retry with timeout for each attempt."""
        
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(max_attempts):
                    # Set timeout
                    signal.signal(signal.SIGALRM, timeout_handler)
                    signal.alarm(timeout_seconds)
                    
                    try:
                        result = func(*args, **kwargs)
                        signal.alarm(0)  # Cancel alarm
                        return result
                    except TimeoutError:
                        if attempt < max_attempts - 1:
                            signal.alarm(0)
                            time.sleep(delay)
                        else:
                            raise
                    finally:
                        signal.alarm(0)
                        
            return wrapper
        return decorator

8. Complete Example
------------------

Here's a complete example with comprehensive retry logic:

.. code-block:: python

    import time
    import logging
    from functools import wraps

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


    def smart_retry(
        max_attempts=3,
        delay=1.0,
        backoff=2.0,
        retry_on=(Exception,)
    ):
        """Smart retry decorator with exponential backoff."""
        
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                current_delay = delay
                
                for attempt in range(max_attempts):
                    try:
                        result = func(*args, **kwargs)
                        if attempt > 0:
                            logger.info(
                                f"{func.__name__} succeeded after {attempt + 1} attempts"
                            )
                        return result
                        
                    except retry_on as e:
                        last_error = e
                        if attempt < max_attempts - 1:
                            logger.warning(
                                f"{func.__name__} attempt {attempt + 1} failed: {e}. "
                                f"Retrying in {current_delay}s..."
                            )
                            time.sleep(current_delay)
                            current_delay *= backoff
                        else:
                            logger.error(
                                f"{func.__name__} failed after {max_attempts} attempts"
                            )
                            raise last_error
                    
                    except Exception as e:
                        # Don't retry on non-retryable exceptions
                        logger.error(f"Non-retryable error in {func.__name__}: {e}")
                        raise
                
                raise last_error
                
            return wrapper
        return decorator


    # Apply to step functions
    @smart_retry(max_attempts=3, delay=1.0, backoff=2.0)
    def fetch_from_api(data):
        """Fetch data from external API."""
        import random
        
        # Simulate occasional failures
        if random.random() < 0.5:
            raise ConnectionError("API temporarily unavailable")
        
        return {"data": ["item1", "item2", "item3"]}


    @smart_retry(max_attempts=2, delay=0.5)
    def process_data(data):
        """Process the fetched data."""
        if not data.get("data"):
            raise ValueError("No data to process")
        return {"processed": True, "count": len(data["data"])}


    @smart_retry(max_attempts=3, delay=1.0, retry_on=(ConnectionError, TimeoutError))
    def save_results(data):
        """Save results to database."""
        import random
        
        if random.random() < 0.3:
            raise ConnectionError("Database connection failed")
        
        return {"saved": True}


    # Create pipeline
    from wpipe import Pipeline

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (fetch_from_api, "Fetch from API", "v1.0"),
        (process_data, "Process Data", "v1.0"),
        (save_results, "Save Results", "v1.0"),
    ])

    # Run pipeline
    result = pipeline.run({})
    print(f"Pipeline completed: {result}")

9. Best Practices
-----------------

1. **Retry only transient failures** - Network, timeouts, not logic errors
2. **Use exponential backoff** - Don't hammer the failing service
3. **Set reasonable limits** - Don't retry forever
4. **Log retry attempts** - Helps with debugging
5. **Distinguish recoverable vs non-recoverable** - Don't retry validation errors
6. **Consider circuit breaker** - Stop retrying if service is down

10. Next Steps
-------------

- :doc:`nested_pipelines` - Combine pipelines together
- :doc:`production_deployment` - Deploy to production
- :doc:`best_practices` - More best practices