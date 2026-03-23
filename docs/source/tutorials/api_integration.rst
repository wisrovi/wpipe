API Integration Tutorial
=======================

This tutorial covers integrating your pipeline with external APIs for tracking, monitoring, and orchestration.

.. contents::
   :local:
   :depth: 2

1. Introduction
--------------

wpipe's API integration allows you to:

- Register workers with an API server
- Track pipeline execution progress
- Report task status in real-time
- Monitor health and performance

2. Understanding the API Client
--------------------------------

The APIClient class provides methods for interacting with external APIs:

.. code-block:: python

    from wpipe import Pipeline
    
    api_config = {
        "base_url": "http://localhost:8418",
        "token": "your-auth-token"
    }
    
    pipeline = Pipeline(api_config=api_config)

3. Worker Registration
----------------------

3.1 Basic Registration
~~~~~~~~~~~~~~~~~~~~~~

Register your pipeline as a worker:

.. code-block:: python

    from wpipe import Pipeline

    api_config = {
        "base_url": "http://localhost:8418",
        "token": "your-auth-token"
    }

    pipeline = Pipeline(api_config=api_config, verbose=True)

    # Register the worker
    worker_info = pipeline.worker_register(
        name="data_processor",
        version="1.0.0"
    )

    print(f"Worker registered: {worker_info}")
    # Expected: {'id': 'worker_abc123', 'name': 'data_processor', ...}

3.2 Setting Worker ID
~~~~~~~~~~~~~~~~~~~~~

After registration, set the worker ID:

.. code-block:: python

    if worker_info and "id" in worker_info:
        worker_id = worker_info["id"]
        pipeline.set_worker_id(worker_id)
        print(f"Worker ID set: {worker_id}")

4. Process Tracking
------------------

4.1 Starting a Process
~~~~~~~~~~~~~~~~~~~~~~

When you run a pipeline with API configured, it automatically registers the process:

.. code-block:: python

    # Define some steps
    def fetch_data(data):
        return {"users": [{"name": "Alice"}, {"name": "Bob"}]}

    def process_data(data):
        return {"count": len(data["users"])}

    # Configure pipeline
    pipeline = Pipeline(api_config=api_config, verbose=True)
    pipeline.set_steps([
        (fetch_data, "Fetch Data", "v1.0"),
        (process_data, "Process Data", "v1.0"),
    ])

    # Run the pipeline - this will register the process with the API
    result = pipeline.run({"request_id": "req_123"})

4.2 Process Flow
~~~~~~~~~~~~~~~~

Here's what happens when you run a pipeline with API:

1. Pipeline starts → API receives process start notification
2. Each step begins → API receives task start notification
3. Each step completes → API receives task completion notification
4. Pipeline finishes → API receives process completion notification

5. API Methods Reference
------------------------

5.1 Worker Methods
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Register worker
    worker_info = pipeline.register_worker({
        "name": "processor",
        "version": "1.0.0",
        "tasks": [{"name": "process", "version": "1.0.0"}]
    })

    # Health check
    health = pipeline.healthcheck_worker({
        "worker_id": "worker_123",
        "status": "healthy"
    })

5.2 Process Methods
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Start process
    process_info = pipeline.register_process({
        "id": "worker_123",
        "steps": ["step1", "step2", "step3"]
    })

    # End process
    pipeline.end_process({
        "id": "process_456",
        "status": "completed"
    })

5.3 Task Methods
~~~~~~~~~~~~~~~~

.. code-block:: python

    # Update task status
    pipeline.update_task({
        "task_id": "task_789",
        "status": "completed",
        "result": {"output": "success"}
    })

6. Custom API Implementation
-----------------------------

6.1 Extending APIClient
~~~~~~~~~~~~~~~~~~~~~~~

Create a custom API client for your specific needs:

.. code-block:: python

    from wpipe import APIClient

    class CustomAPIClient(APIClient):
        """Custom API client with additional methods."""
        
        def __init__(self, base_url: str, token: str, team_id: str):
            super().__init__(base_url, token)
            self.team_id = team_id
        
        def report_metrics(self, metrics: dict) -> dict:
            """Report custom metrics to the API."""
            data = {
                "team_id": self.team_id,
                "metrics": metrics,
                "timestamp": self._get_timestamp()
            }
            return self.send_post("/metrics", data)
        
        def _get_timestamp(self) -> str:
            from datetime import datetime
            return datetime.utcnow().isoformat()

7. Error Handling with API
--------------------------

7.1 Graceful Degradation
~~~~~~~~~~~~~~~~~~~~~~~~

Handle API failures gracefully:

.. code-block:: python

    from wpipe import Pipeline

    class FallbackPipeline(Pipeline):
        """Pipeline that works offline if API is unavailable."""
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.api_available = True
        
        def _api_task_update(self, msg: dict):
            try:
                super()._api_task_update(msg)
            except Exception as e:
                print(f"API update failed: {e}")
                # Continue without API - graceful degradation

8. Complete Example
------------------

Here's a complete example with full API integration:

.. code-block:: python

    from wpipe import Pipeline
    import logging

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


    class TrackedPipeline(Pipeline):
        """Pipeline with comprehensive API tracking."""
        
        def __init__(self, api_config: dict, worker_name: str):
            super().__init__(api_config=api_config, verbose=True)
            self.worker_name = worker_name
        
        def run(self, *args, **kwargs):
            logger.info(f"Starting pipeline: {self.worker_name}")
            try:
                result = super().run(*args, **kwargs)
                logger.info(f"Pipeline completed successfully")
                return result
            except Exception as e:
                logger.error(f"Pipeline failed: {e}")
                raise


    # Define steps
    def fetch_data(data):
        logger.info("Fetching data...")
        return {"records": [{"id": 1}, {"id": 2}, {"id": 3}]}


    def transform_data(data):
        logger.info("Transforming data...")
        records = data["records"]
        transformed = [{"id": r["id"] * 2, "processed": True} for r in records]
        return {"transformed_records": transformed}


    def save_data(data):
        logger.info("Saving data...")
        return {"saved": True, "count": len(data["transformed_records"])}


    # Configure and run
    api_config = {
        "base_url": "http://localhost:8418",
        "token": "your-auth-token"
    }

    pipeline = TrackedPipeline(api_config, "data_pipeline")
    pipeline.set_steps([
        (fetch_data, "Fetch Data", "v1.0"),
        (transform_data, "Transform Data", "v1.0"),
        (save_data, "Save Data", "v1.0"),
    ])

    # Register worker
    worker_info = pipeline.worker_register(
        name="data_pipeline",
        version="1.0.0"
    )

    if worker_info:
        pipeline.set_worker_id(worker_info.get("id"))

    # Run pipeline
    result = pipeline.run({})
    print(f"Result: {result}")

9. Testing API Integration
--------------------------

9.1 Mock Server
~~~~~~~~~~~~~~~

Use a mock server for testing:

.. code-block:: python

    import responses
    from wpipe import Pipeline

    @responses.activate
    def test_pipeline_with_mock_api():
        """Test pipeline with mocked API responses."""
        
        # Mock the worker registration endpoint
        responses.add(
            responses.POST,
            "http://localhost:8418/matricula",
            json={"id": "worker_test_123", "name": "test_worker"},
            status=200
        )
        
        # Mock the process registration endpoint
        responses.add(
            responses.POST,
            "http://localhost:8418/newprocess",
            json={"father": "process_123", "sons": []},
            status=200
        )
        
        # Run pipeline
        pipeline = Pipeline(
            api_config={"base_url": "http://localhost:8418", "token": "test"}
        )
        pipeline.set_steps([
            (lambda d: {"result": "ok"}, "Test Step", "v1.0"),
        ])
        
        result = pipeline.run({})
        assert result["result"] == "ok"

10. Security Best Practices
---------------------------

10.1 Token Management
~~~~~~~~~~~~~~~~~~~~~

- Never hardcode tokens in source code
- Use environment variables or secure vaults
- Rotate tokens regularly

.. code-block:: python

    import os

    api_config = {
        "base_url": os.environ["API_BASE_URL"],
        "token": os.environ["API_TOKEN"]  # Set in environment
    }

10.2 HTTPS Only
~~~~~~~~~~~~~~~

Always use HTTPS in production:

.. code-block:: python

    # Development (HTTP OK)
    api_config = {"base_url": "http://localhost:8418", "token": "..."}

    # Production (HTTPS required)
    api_config = {"base_url": "https://api.production.com", "token": "..."}

11. Troubleshooting
------------------

11.1 Common Issues
~~~~~~~~~~~~~~~~~

- **Connection refused**: Check API server is running
- **401 Unauthorized**: Verify token is correct
- **Timeout**: Check network connectivity

11.2 Debug Mode
~~~~~~~~~~~~~~

Enable debug output:

.. code-block:: python

    import logging
    logging.getLogger("wpipe").setLevel(logging.DEBUG)

12. Next Steps
--------------

Now you understand API integration:

- :doc:`error_handling` - Handle errors gracefully
- :doc:`retry_logic` - Add automatic retries
- :doc:`production_deployment` - Deploy to production