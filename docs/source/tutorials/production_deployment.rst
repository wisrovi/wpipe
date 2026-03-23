Production Deployment Tutorial
================================

Learn how to deploy wpipe pipelines to production environments.

.. contents::
   :local:
   :depth: 2

1. Environment Setup
---------------------

1.1 Production Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    pip install wpipe
    pip install -e ".[dev]"  # For testing

2. Configuration Management
----------------------------

2.1 Environment-Based Config
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import os

    config = {
        "base_url": os.environ.get("API_URL", "http://localhost:8418"),
        "token": os.environ["API_TOKEN"],
        "verbose": os.environ.get("VERBOSE", "false").lower() == "true"
    }

3. Logging and Monitoring
-------------------------

3.1 Structured Logging
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    logger = logging.getLogger(__name__)

    def monitored_step(data):
        logger.info(f"Processing {data}")
        try:
            result = process(data)
            logger.info(f"Success: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed: {e}")
            raise

4. Error Handling in Production
--------------------------------

4.1 Graceful Degradation
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wpipe import Pipeline
    from wpipe.exception import TaskError

    class ProductionPipeline(Pipeline):
        def run(self, *args, **kwargs):
            try:
                return super().run(*args, **kwargs)
            except TaskError as e:
                logger.error(f"Pipeline failed: {e}")
                # Send alert
                send_alert(str(e))
                raise

5. Health Checks
----------------

5.1 Health Check Endpoint
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def health_check():
        """Check pipeline health."""
        try:
            # Test imports
            from wpipe import Pipeline
            
            # Test basic pipeline
            p = Pipeline()
            p.set_steps([(lambda d: {}, "Test", "v1.0")])
            p.run({})
            
            return {"status": "healthy"}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

6. CI/CD Integration
--------------------

6.1 GitHub Actions Example
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    name: Test Pipeline
    
    on: [push]
    
    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v2
          - run: pip install -e ".[dev]"
          - run: pytest
          - run: ruff check wpipe/
          - run: mypy wpipe/

7. Docker Deployment
--------------------

7.1 Dockerfile Example
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: dockerfile

    FROM python:3.11-slim
    
    WORKDIR /app
    COPY . .
    RUN pip install wpipe
    
    CMD ["python", "main.py"]

8. Complete Example
------------------

.. code-block:: python

    import os
    import logging
    from wpipe import Pipeline
    from wpipe.exception import TaskError

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)


    class ProductionPipeline(Pipeline):
        """Production-ready pipeline with monitoring."""
        
        def __init__(self):
            api_config = {
                "base_url": os.environ.get("API_URL"),
                "token": os.environ.get("API_TOKEN")
            }
            super().__init__(
                api_config=api_config if os.environ.get("API_URL") else None,
                verbose=os.environ.get("DEBUG", "").lower() == "true",
                max_retries=3,
                retry_delay=2.0
            )
        
        def run(self, *args, **kwargs):
            logger.info("Starting pipeline execution")
            try:
                result = super().run(*args, **kwargs)
                logger.info("Pipeline completed successfully")
                return result
            except TaskError as e:
                logger.error(f"Pipeline failed: {e}")
                raise


    # Entry point
    if __name__ == "__main__":
        pipeline = ProductionPipeline()
        pipeline.set_steps([
            (lambda d: {"data": "processed"}, "Process", "v1.0"),
        ])
        result = pipeline.run({})
        print(result)

9. Best Practices
-----------------

1. Use environment variables for configuration
2. Implement comprehensive logging
3. Set up monitoring and alerting
4. Use retry logic for resilience
5. Test in staging before production

10. Next Steps
-------------

- Review :doc:`architecture` for design details
- Check :doc:`api_reference` for complete API