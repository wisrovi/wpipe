Retry Logic
===========

Automatically retry failed steps with configurable parameters.

Overview
--------

The ``Retry`` class wraps steps with automatic retry logic for handling transient failures.

Basic Usage
-----------

.. code-block:: python

   from wpipe import Pipeline
   from wpipe.pipe import Retry

   def unstable_api_call(data):
       import random
       if random.random() < 0.5:
           raise ConnectionError("API timeout")
       return {"api_result": "success"}

   retry_step = Retry(
       func=unstable_api_call,
       name="API Call",
       version="v1.0",
       attempts=3,
       wait=1.0,
   )

   pipeline = Pipeline(verbose=True)
   pipeline.set_steps([retry_step])

   result = pipeline.run({})

Parameters
----------

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Parameter
     - Type
     - Description
   * - ``func``
     - callable
     - Function to execute
   * - ``name``
     - str
     - Step name for logging
   * - ``version``
     - str
     - Step version
   * - ``attempts``
     - int
     - Maximum retry attempts (default: 3)
   * - ``wait``
     - float
     - Wait time between retries in seconds (default: 1.0)
   * - ``backoff``
     - float
     - Backoff multiplier for wait time (default: 1.0)

Retry Strategies
----------------

**Fixed Wait:** Same wait time between retries

.. code-block:: python

   Retry(func=my_func, name="Step", version="v1.0", attempts=3, wait=2.0)

**Exponential Backoff:** Wait time increases exponentially

.. code-block:: python

   Retry(
       func=my_func,
       name="Step",
       version="v1.0",
       attempts=5,
       wait=1.0,
       backoff=2.0,  # 1s, 2s, 4s, 8s, 16s
   )

Complete Example
----------------

.. code-block:: python

   from wpipe import Pipeline
   from wpipe.pipe import Retry

   def fetch_data(data):
       import requests
       response = requests.get("https://api.example.com/data")
       response.raise_for_status()
       return {"data": response.json()}

   def process_data(data):
       return {"processed": True, "items": len(data["data"])}

   retry_fetch = Retry(
       func=fetch_data,
       name="Fetch Data",
       version="v1.0",
       attempts=5,
       wait=2.0,
       backoff=1.5,
   )

   pipeline = Pipeline(verbose=True)
   pipeline.set_steps([
       retry_fetch,
       (process_data, "Process", "v1.0"),
   ])

   result = pipeline.run({})

Best Practices
-------------

1. **Set reasonable attempts**: Don't retry indefinitely
2. **Use exponential backoff**: Prevents overwhelming services
3. **Log failures**: Monitor retry patterns
4. **Handle idempotency**: Ensure retry is safe for your operation

Next Steps
---------

* Learn about :doc:`api_integration` for API tracking
* Explore :doc:`error_handling` for error recovery
