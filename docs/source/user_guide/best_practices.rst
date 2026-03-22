Best Practices
==============

This guide outlines best practices for building robust, maintainable, and efficient pipelines with wpipe.

1. Pipeline Design
------------------

1.1 Single Responsibility Principle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each step should do one thing well:

**Good:**

.. code-block:: python

    def fetch_user(data):
        return {"user": database.get_user(data["user_id"])}

    def validate_user(data):
        user = data["user"]
        return {"valid": user is not None and user.is_active}

    def send_notification(data):
        if data["valid"]:
            email.send(data["user"].email, "Welcome!")
        return {"notified": data["valid"]}

**Bad:**

.. code-block:: python

    def everything(data):
        user = database.get_user(data["user_id"])  # Fetch
        if user and user.is_active:  # Validation
            email.send(user.email, "Welcome!")  # Send
        return {"done": True}  # Done

1.2 Keep Steps Small and Testable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Smaller steps are easier to:

- Test in isolation
- Debug when errors occur
- Reuse in different pipelines
- Understand and maintain

**Good - Testable step:**

.. code-block:: python

    def calculate_discount(price: float, discount_percent: float) -> float:
        """Calculate discounted price."""
        return price * (1 - discount_percent / 100)

    def apply_discount(data):
        price = data["original_price"]
        discount = data["discount_percent"]
        return {"final_price": calculate_discount(price, discount)}

1.3 Order Steps Logically
~~~~~~~~~~~~~~~~~~~~~~~~

Steps should follow a natural workflow:

::

    Fetch Data → Validate Input → Process Data → Save Results
    
    NOT:
    
    Process Data → Fetch Data → Save Results → Validate Input

2. Error Handling
-----------------

2.1 Always Return Dictionaries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Never return None from a step:

.. code-block:: python

    # Good
    def good_step(data):
        return {"result": data["x"] * 2}

    # Bad - returns None on error
    def bad_step(data):
        if "x" not in data:
            return  # ERROR!
        return {"result": data["x"] * 2}

2.2 Use .get() with Defaults
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Handle missing keys gracefully:

.. code-block:: python

    def robust_step(data):
        value = data.get("value", 0)  # Default to 0
        multiplier = data.get("multiplier", 1)  # Default to 1
        optional = data.get("optional", None)  # Default to None
        return {"result": value * multiplier}

2.3 Raise TaskError for Failures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the appropriate exception type:

.. code-block:: python

    from wpipe.exception import TaskError, Codes

    def validate_input(data):
        if "email" not in data:
            raise TaskError(
                "Email is required",
                step_name="Validate Input",
                code=Codes.VALIDATION_ERROR
            )

        if not is_valid_email(data["email"]):
            raise TaskError(
                "Invalid email format",
                step_name="Validate Email",
                code=Codes.VALIDATION_ERROR
            )

        return {"validated": True}

2.4 Distinguish Recoverable Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Mark errors that can be retried:

.. code-block:: python

    from wpipe.exception import TaskError, Codes

    def call_api(data):
        try:
            result = api.get(data["endpoint"])
            return {"api_result": result}
        except NetworkTimeout:
            raise TaskError(
                "API timeout - may succeed on retry",
                code=Codes.RETRYABLE_ERROR
            )
        except InvalidApiKey:
            raise TaskError(
                "Invalid API key - won't succeed on retry",
                code=Codes.API_ERROR
            )

3. Data Management
------------------

3.1 Don't Mutate Input Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create new dictionaries instead of modifying:

.. code-block:: python

    # Good - creates new dict
    def transform_good(data):
        return {
            **data,
            "transformed": True,
            "value": data["value"] * 2,
        }

    # Bad - mutates input
    def transform_bad(data):
        data["transformed"] = True
        data["value"] = data["value"] * 2
        return data  # Same object, mutated!

3.2 Use Clear Key Names
~~~~~~~~~~~~~~~~~~~~~~~

Avoid generic names:

.. code-block:: python

    # Good - descriptive keys
    return {
        "user_email": user.email,
        "user_id": user.id,
        "email_validated": True,
    }

    # Bad - generic keys
    return {
        "a": user.email,
        "b": user.id,
        "c": True,
    }

3.3 Document Data Schema
~~~~~~~~~~~~~~~~~~~~~~~

Comment expected input/output:

.. code-block:: python

    def process_payment(data):
        """Process a payment transaction.

        Input:
            data (dict):
                - amount (float): Payment amount in USD
                - currency (str): Currency code (e.g., 'USD')
                - card_token (str): Tokenized card from payment provider

        Output:
            data (dict):
                - transaction_id (str): Unique transaction ID
                - status (str): 'success' or 'failed'
                - receipt_url (str): URL to receipt

        Raises:
            TaskError: If payment processing fails
        """
        ...

4. Performance
-------------

4.1 Lazy Loading
~~~~~~~~~~~~~~~

Only load data when needed:

.. code-block:: python

    def fetch_if_needed(data):
        if "cached_data" not in data:
            return {"cached_data": expensive_fetch()}
        return {"cached_data": data["cached_data"]}

4.2 Avoid Redundant Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cache results when safe:

.. code-block:: python

    class CachedTransformer:
        def __init__(self):
            self.cache = {}

        def __call__(self, data):
            cache_key = data.get("id")
            if cache_key in self.cache:
                return self.cache[cache_key]

            result = expensive_transform(data)
            self.cache[cache_key] = result
            return result

4.3 Batch Operations
~~~~~~~~~~~~~~~~~~~

Process multiple items together:

.. code-block:: python

    # Bad - individual calls
    def process_slow(data):
        for item in data["items"]:
            api.save(item)  # N API calls
        return {"saved": len(data["items"])}

    # Good - batch call
    def process_fast(data):
        api.batch_save(data["items"])  # 1 API call
        return {"saved": len(data["items"])}

5. Testing
----------

5.1 Test Steps in Isolation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each step should be independently testable:

.. code-block:: python

    # my_module.py
    def calculate_total(items):
        return {"total": sum(item["price"] for item in items)}

    # test_my_module.py
    def test_calculate_total():
        data = {"items": [
            {"name": "A", "price": 10},
            {"name": "B", "price": 20},
        ]}
        result = calculate_total(data)
        assert result["total"] == 30

5.2 Mock External Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Isolate from external services:

.. code-block:: python

    from unittest.mock import patch

    def test_pipeline_with_api():
        with patch("my_module.api_call") as mock_api:
            mock_api.return_value = {"success": True}

            pipeline = Pipeline()
            pipeline.set_steps([
                (call_api, "Call API", "v1.0"),
            ])
            result = pipeline.run({"endpoint": "/test"})

            assert result["success"] is True
            mock_api.assert_called_once()

5.3 Test Error Handling
~~~~~~~~~~~~~~~~~~~~~~~

Verify error behavior:

.. code-block:: python

    from wpipe.exception import TaskError

    def test_validation_error():
        pipeline = Pipeline()
        pipeline.set_steps([
            (validate_email, "Validate", "v1.0"),
        ])

        with pytest.raises(TaskError) as exc_info:
            pipeline.run({"email": "invalid"})

        assert exc_info.value.code == Codes.VALIDATION_ERROR

6. Logging and Debugging
------------------------

6.1 Use Descriptive Step Names
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Helpful for debugging:

.. code-block:: python

    # Good
    (fetch_user_by_id, "Fetch User by ID from Database", "v1.0")

    # Bad
    (fetch_user, "Step 1", "v1.0")

6.2 Add Debug Output in Development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use verbose mode for debugging:

.. code-block:: python

    # Development
    pipeline = Pipeline(verbose=True)

    # Production
    pipeline = Pipeline(verbose=False)

6.3 Preserve Error Context
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Include useful information in errors:

.. code-block:: python

    def risky_operation(data):
        try:
            return do_operation(data)
        except Exception as e:
            raise TaskError(
                f"Operation failed: {e}",
                step_name="Risky Operation",
                original_error=e
            )

7. Security
-----------

7.1 Don't Log Sensitive Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Protect sensitive information:

.. code-block:: python

    # Bad - logs password
    def bad_step(data):
        logger.info(f"Login attempt for user: {data['username']}, password: {data['password']}")

    # Good - sanitizes
    def good_step(data):
        logger.info(f"Login attempt for user: {data['username']}")
        return {"login_success": authenticate(data)}

7.2 Validate External Input
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Never trust external data:

.. code-block:: python

    def process_user_input(data):
        # Validate all external input
        user_id = data.get("user_id")
        if not isinstance(user_id, int) or user_id <= 0:
            raise TaskError("Invalid user_id", code=Codes.VALIDATION_ERROR)

        return {"validated": True}

8. Configuration
----------------

8.1 Use Configuration Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Externalize configuration:

.. code-block:: yaml

    # config.yaml
    pipeline:
      verbose: false
      timeout: 300

    api:
      base_url: "https://api.example.com"
      timeout: 30

    database:
      host: "localhost"
      port: 5432

.. code-block:: python

    from wpipe.util import leer_yaml

    config = leer_yaml("config.yaml")
    pipeline = Pipeline(
        verbose=config["pipeline"]["verbose"],
        timeout=config["pipeline"]["timeout"]
    )

8.2 Use Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For deployment:

.. code-block:: yaml

    # config.yaml with env vars
    api:
      token: ${API_TOKEN}
      base_url: ${API_BASE_URL:-https://default.example.com}

8.3 Version Control Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. code-block:: text

    # .gitignore
    config.yaml  # Don't commit secrets
    *.db  # Don't commit databases

    # Commit template instead
    config.yaml.template

9. Code Organization
---------------------

9.1 Group Related Steps
~~~~~~~~~~~~~~~~~~~~~~~

::

    my_pipeline/
    ├── __init__.py
    ├── steps/
    │   ├── __init__.py
    │   ├── fetch.py      # Data fetching steps
    │   ├── process.py    # Processing steps
    │   └── save.py       # Storage steps
    ├── pipeline.py       # Pipeline configuration
    └── main.py           # Entry point

9.2 Create Reusable Step Libraries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # my_steps/__init__.py
    from .validation import validate_email, validate_phone
    from .transform import normalize_text, format_date
    from .storage import save_to_db, save_to_s3

    __all__ = [
        "validate_email",
        "validate_phone",
        "normalize_text",
        "format_date",
        "save_to_db",
        "save_to_s3",
    ]

10. Deployment
-------------

10.1 Use Virtual Environments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

10.2 Pin Dependencies
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    # requirements.txt
    wpipe==1.0.0
    requests==2.31.0
    pyyaml==6.0.1

10.3 Monitor Pipeline Health
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Track execution metrics:

.. code-block:: python

    from wpipe import Pipeline
    from wpipe.sqlite import Wsqlite

    pipeline = Pipeline(verbose=False)

    with Wsqlite("metrics.db") as db:
        db.input = {"run_id": generate_run_id()}

        result = pipeline.run({"data": process()})

        db.output = {
            "status": "success",
            "duration": measure_duration(),
            "result_size": len(str(result)),
        }
