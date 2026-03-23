Examples Gallery
================

Explore **100+ examples** organized by functionality. Each example includes code, explanation, and is located in the ``examples/`` directory of the repository.

.. contents::
   :local:
   :depth: 2

01 Basic Pipeline (15 Examples)
------------------------------

Simple pipelines with functions, classes, and data flow.

**Location:** `examples/01_basic_pipeline/ <https://github.com/wisrovi/wpipe/tree/main/examples/01_basic_pipeline/>`_

These examples demonstrate the core concepts of wpipe pipelines.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Example
     - Description
   * - `01_simple_function/ <https://github.com/wisrovi/wpipe/tree/main/examples/01_basic_pipeline/01_simple_function>`_
     - Basic pipeline with a single function step
   * - `02_class_steps/ <https://github.com/wisrovi/wpipe/tree/main/examples/01_basic_pipeline/02_class_steps>`_
     - Using class instances with ``__call__`` as pipeline steps
   * - `03_mixed_steps/ <https://github.com/wisrovi/wpipe/tree/main/examples/01_basic_pipeline/03_mixed_steps>`_
     - Combining functions and classes in the same pipeline
   * - `04_default_values/ <https://github.com/wisrovi/wpipe/tree/main/examples/01_basic_pipeline/04_default_values>`_
     - Handling missing data with default values
   * - `05_args_kwargs/ <https://github.com/wisrovi/wpipe/tree/main/examples/01_basic_pipeline/05_args_kwargs>`_
     - Passing additional arguments to steps
   * - `06_dict_processing/ <https://github.com/wisrovi/wpipe/tree/main/examples/01_basic_pipeline/06_dict_processing>`_
     - Advanced dictionary manipulation in steps
   * - `07_multiple_runs/ <https://github.com/wisrovi/wpipe/tree/main/examples/01_basic_pipeline/07_multiple_runs>`_
     - Running the same pipeline with different data
   * - `08_data_aggregation/ <https://github.com/wisrovi/wpipe/tree/main/examples/01_basic_pipeline/08_data_aggregation>`_
     - Aggregating data from multiple sources
   * - `09_empty_data/ <https://github.com/wisrovi/wpipe/tree/main/examples/01_basic_pipeline/09_empty_data>`_
     - Handling empty input data gracefully
   * - `10_lambda_steps/ <https://github.com/wisrovi/wpipe/tree/main/examples/01_basic_pipeline/10_lambda_steps>`_
     - Using lambda functions as simple steps
   * - `11_decorator_steps/ <https://github.com/wisrovi/wpipe/tree/main/examples/01_basic_pipeline/11_decorator_steps>`_
     - Using decorators to modify step behavior
   * - `12_context_manager/ <https://github.com/wisrovi/wpipe/tree/main/examples/01_basic_pipeline/12_context_manager>`_
     - Using context managers with pipelines
   * - `13_async_pipeline/ <https://github.com/wisrovi/wpipe/tree/main/examples/01_basic_pipeline/13_async_pipeline>`_
     - Async pipeline execution patterns
   * - `14_pipeline_chaining/ <https://github.com/wisrovi/wpipe/tree/main/examples/01_basic_pipeline/14_pipeline_chaining>`_
     - Chaining multiple pipelines together
   * - `15_pipeline_clone/ <https://github.com/wisrovi/wpipe/tree/main/examples/01_basic_pipeline/15_pipeline_clone>`_
     - Cloning and modifying pipelines

**Quick Example:**

.. code-block:: python

    from wpipe import Pipeline

    def fetch_data(data):
        return {"data": [1, 2, 3]}

    def process(data):
        return {"sum": sum(data["data"])}

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (fetch_data, "Fetch Data", "v1.0"),
        (process, "Process Data", "v1.0"),
    ])
    result = pipeline.run({})

02 API Pipeline (20 Examples)
-----------------------------

Connect pipelines to external APIs for tracking and monitoring.

**Location:** `examples/02_api_pipeline/ <https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/>`_

These examples show how to integrate with external APIs and track pipeline execution.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Example
     - Description
   * - `01_basic_api/ <https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/01_basic_api>`_
     - Basic API connection and configuration
   * - `02_worker_id/ <https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/02_worker_id>`_
     - Setting and managing worker IDs
   * - `03_no_api/ <https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/03_no_api>`_
     - Running without API (local only)
   * - `04_api_errors/ <https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/04_api_errors>`_
     - Handling API connection errors gracefully
   * - `05_show_errors/ <https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/05_show_errors>`_
     - Displaying detailed error information
   * - `06_api_with_timeout/ <https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/06_api_with_timeout>`_
     - Configuring request timeouts
   * - `06_full_config/ <https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/06_full_config>`_
     - Complete API configuration example
   * - `07_api_retry_config/ <https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/07_api_retry_config>`_
     - Configuring retries for API calls
   * - `08_api_custom_headers/ <https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/08_api_custom_headers>`_
     - Adding custom headers to requests
   * - `09_api_logging/ <https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/09_api_logging>`_
     - Logging API interactions
   * - `10_worker_metadata/ <https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/10_worker_metadata>`_
     - Attaching metadata to workers
   * - `11_rate_limiting/ <https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/11_rate_limiting>`_
     - Handling API rate limits
   * - `12_batch_operations/ <https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/12_batch_operations>`_
     - Processing data in batches via API
   * - `13_authentication/ <https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/13_authentication>`_
     - Different authentication methods
   * - `14_health_checks/ <https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/14_health_checks>`_
     - Implementing health check endpoints
   * - `15_service_discovery/ <https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/15_service_discovery>`_
     - Dynamic service discovery
   * - `16_expired_token/ <https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/16_expired_token>`_
     - Handling expired authentication tokens
   * - `17_network_timeout/ <https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/17_network_timeout>`_
     - Network timeout handling
   * - `18_invalid_url/ <https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/18_invalid_url>`_
     - Handling invalid API URLs
   * - `19_concurrent_workers/ <https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/19_concurrent_workers>`_
     - Multiple workers running concurrently
   * - `20_reconnection/ <https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/20_reconnection>`_
     - Automatic reconnection patterns

**Quick Example:**

.. code-block:: python

    from wpipe import Pipeline

    api_config = {
        "base_url": "https://api.example.com",
        "token": "your-auth-token"
    }

    pipeline = Pipeline(api_config=api_config)
    pipeline.worker_register(name="processor", version="1.0.0")

03 Error Handling (15 Examples)
-----------------------------

Robust error handling patterns and recovery strategies.

**Location:** `examples/03_error_handling/ <https://github.com/wisrovi/wpipe/tree/main/examples/03_error_handling/>`_

Learn how to handle errors gracefully and implement recovery patterns.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Example
     - Description
   * - `01_basic_error_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/03_error_handling/01_basic_error_example>`_
     - Catching and handling basic errors
   * - `02_exception_types_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/03_error_handling/02_exception_types_example>`_
     - Different exception types in wpipe
   * - `03_task_error_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/03_error_handling/03_task_error_example>`_
     - Working with TaskError exceptions
   * - `04_middle_error_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/03_error_handling/04_middle_error_example>`_
     - Errors occurring mid-pipeline
   * - `05_continue_after_error_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/03_error_handling/05_continue_after_error_example>`_
     - Continuing after non-critical errors
   * - `06_exception_chaining_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/03_error_handling/06_exception_chaining_example>`_
     - Exception chaining and context
   * - `07_custom_error_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/03_error_handling/07_custom_error_example>`_
     - Creating custom error types
   * - `08_error_in_recovery_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/03_error_handling/08_error_in_recovery_example>`_
     - Recovery from errors
   * - `09_partial_results_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/03_error_handling/09_partial_results_example>`_
     - Accessing partial results on failure
   * - `10_error_code.py <https://github.com/wisrovi/wpipe/tree/main/examples/03_error_handling/10_error_code.py>`_
     - Working with error codes
   * - `10_error_context.py <https://github.com/wisrovi/wpipe/tree/main/examples/03_error_handling/10_error_context.py>`_
     - Error context and debugging
   * - `10_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/03_error_handling/10_example>`_
     - Complete error handling example
   * - `errors.py <https://github.com/wisrovi/wpipe/tree/main/examples/03_error_handling/errors.py>`_
     - Custom error definitions

**Quick Example:**

.. code-block:: python

    from wpipe import Pipeline
    from wpipe.exception import TaskError, Codes

    def risky_step(data):
        raise ConnectionError("Network unavailable")

    pipeline = Pipeline(verbose=True)

    try:
        result = pipeline.run({})
    except TaskError as e:
        print(f"Error code: {e.error_code}")
        print(f"Message: {str(e)}")

04 Conditional Branching (12 Examples)
--------------------------------------

Execute different paths based on data conditions.

**Location:** `examples/04_condition/ <https://github.com/wisrovi/wpipe/tree/main/examples/04_condition/>`_

Build complex decision trees with conditional execution.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Example
     - Description
   * - `01_basic_condition_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/04_condition/01_basic_condition_example>`_
     - Basic conditional branching
   * - `02_string_condition_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/04_condition/02_string_condition_example>`_
     - String-based conditions
   * - `03_multiple_steps_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/04_condition/03_multiple_steps_example>`_
     - Multiple steps in conditional branches
   * - `04_no_else_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/04_condition/04_no_else_example>`_
     - Condition without else branch
   * - `05_invalid_expression_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/04_condition/05_invalid_expression_example>`_
     - Handling invalid expressions
   * - `06_complex_expression_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/04_condition/06_complex_expression_example>`_
     - Complex boolean expressions
   * - `07_numeric_comparison_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/04_condition/07_numeric_comparison_example>`_
     - Numeric comparisons
   * - `08_equality_check_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/04_condition/08_equality_check_example>`_
     - Equality checks in conditions
   * - `09_chained_conditions_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/04_condition/09_chained_conditions_example>`_
     - Chaining multiple conditions
   * - `10_boolean_logic.py <https://github.com/wisrovi/wpipe/tree/main/examples/04_condition/10_boolean_logic.py>`_
     - Boolean logic in conditions
   * - `10_none_check.py <https://github.com/wisrovi/wpipe/tree/main/examples/04_condition/10_none_check.py>`_
     - Checking for None values

**Quick Example:**

.. code-block:: python

    from wpipe import Pipeline, Condition

    def check_value(data):
        return {"value": 75}

    def process_high(data):
        return {"result": "High value"}

    def process_low(data):
        return {"result": "Low value"}

    condition = Condition(
        expression="value > 50",
        branch_true=[(process_high, "Process High", "v1.0")],
        branch_false=[(process_low, "Process Low", "v1.0")],
    )

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (check_value, "Check Value", "v1.0"),
        condition,
    ])
    result = pipeline.run({})

05 Retry Logic (12 Examples)
----------------------------

Automatic retries for failed operations with backoff strategies.

**Location:** `examples/05_retry/ <https://github.com/wisrovi/wpipe/tree/main/examples/05_retry/>`_

Implement robust retry mechanisms for unreliable operations.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Example
     - Description
   * - `01_basic_retry_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/05_retry/01_basic_retry_example>`_
     - Basic retry configuration
   * - `02_success_after_retry_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/05_retry/02_success_after_retry_example>`_
     - Succeeding after retries
   * - `03_filter_exceptions_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/05_retry/03_filter_exceptions_example>`_
     - Filtering which exceptions trigger retries
   * - `04_multiple_steps_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/05_retry/04_multiple_steps_example>`_
     - Retry across multiple steps
   * - `05_no_retry_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/05_retry/05_no_retry_example>`_
     - Disabling retries
   * - `06_retry_with_backoff_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/05_retry/06_retry_with_backoff_example>`_
     - Exponential backoff between retries
   * - `07_retry_with_custom_exception_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/05_retry/07_retry_with_custom_exception_example>`_
     - Custom exception handling in retries
   * - `08_retry_partial_failure_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/05_retry/08_retry_partial_failure_example>`_
     - Handling partial failures
   * - `09_retry_counter_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/05_retry/09_retry_counter_example>`_
     - Tracking retry attempts
   * - `10_retry_context.py <https://github.com/wisrovi/wpipe/tree/main/examples/05_retry/10_retry_context.py>`_
     - Retry context management
   * - `10_retry_state.py <https://github.com/wisrovi/wpipe/tree/main/examples/05_retry/10_retry_state.py>`_
     - Managing state during retries

**Quick Example:**

.. code-block:: python

    from wpipe import Pipeline

    pipeline = Pipeline(
        verbose=True,
        max_retries=3,
        retry_delay=2.0,
        retry_on_exceptions=(ConnectionError, TimeoutError),
    )

06 SQLite Integration (14 Examples)
-----------------------------------

Persist pipeline results to SQLite databases.

**Location:** `examples/06_sqlite_integration/ <https://github.com/wisrovi/wpipe/tree/main/examples/06_sqlite_integration/>`_

Store and query pipeline execution results.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Example
     - Description
   * - `01_basic_write_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/06_sqlite_integration/01_basic_write_example>`_
     - Writing results to database
   * - `02_wsqlite_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/06_sqlite_integration/02_wsqlite_example>`_
     - Using Wsqlite context manager
   * - `03_export_csv_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/06_sqlite_integration/03_export_csv_example>`_
     - Exporting data to CSV
   * - `04_advanced_queries_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/06_sqlite_integration/04_advanced_queries_example>`_
     - Advanced query patterns
   * - `05_batch_insert_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/06_sqlite_integration/05_batch_insert_example>`_
     - Batch insert operations
   * - `06_query_specific_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/06_sqlite_integration/06_query_specific_example>`_
     - Querying specific records
   * - `07_update_record_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/06_sqlite_integration/07_update_record_example>`_
     - Updating existing records
   * - `08_delete_record_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/06_sqlite_integration/08_delete_record_example>`_
     - Deleting records
   * - `09_complex_query_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/06_sqlite_integration/09_complex_query_example>`_
     - Complex query examples
   * - `10_json_storage.py <https://github.com/wisrovi/wpipe/tree/main/examples/06_sqlite_integration/10_json_storage.py>`_
     - Storing JSON data
   * - `10_transaction.py <https://github.com/wisrovi/wpipe/tree/main/examples/06_sqlite_integration/10_transaction.py>`_
     - Transaction handling
   * - `database.py <https://github.com/wisrovi/wpipe/tree/main/examples/06_sqlite_integration/database.py>`_
     - Database utility functions

**Quick Example:**

.. code-block:: python

    from wpipe import Pipeline
    from wpipe.sqlite import Wsqlite

    with Wsqlite(db_name="results.db") as db:
        db.input = {"x": 10}
        result = pipeline.run({"x": 10})
        db.output = result
        print(f"Record ID: {db.id}")

07 Nested Pipelines (14 Examples)
---------------------------------

Compose complex workflows from smaller, reusable pipelines.

**Location:** `examples/07_nested_pipelines/ <https://github.com/wisrovi/wpipe/tree/main/examples/07_nested_pipelines/>`_

Build modular, maintainable pipeline systems.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Example
     - Description
   * - `01_basic_nested_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/07_nested_pipelines/01_basic_nested_example>`_
     - Basic nested pipeline structure
   * - `02_multiple_nested_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/07_nested_pipelines/02_multiple_nested_example>`_
     - Multiple nested pipelines
   * - `03_data_passing_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/07_nested_pipelines/03_data_passing_example>`_
     - Passing data between nested pipelines
   * - `04_reuse_pipeline_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/07_nested_pipelines/04_reuse_pipeline_example>`_
     - Reusing pipeline definitions
   * - `05_nested_with_data_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/07_nested_pipelines/05_nested_with_data_example>`_
     - Nested pipelines with data
   * - `06_deep_nesting_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/07_nested_pipelines/06_deep_nesting_example>`_
     - Deeply nested pipeline hierarchies
   * - `07_parallel_nested_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/07_nested_pipelines/07_parallel_nested_example>`_
     - Parallel nested execution
   * - `08_conditional_nested_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/07_nested_pipelines/08_conditional_nested_example>`_
     - Conditionals in nested pipelines
   * - `09_nested_state_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/07_nested_pipelines/09_nested_state_example>`_
     - Managing state in nested pipelines
   * - `10_nested_error_handling.py <https://github.com/wisrovi/wpipe/tree/main/examples/07_nested_pipelines/10_nested_error_handling.py>`_
     - Error handling in nested pipelines
   * - `10_recursive_nesting.py <https://github.com/wisrovi/wpipe/tree/main/examples/07_nested_pipelines/10_recursive_nesting.py>`_
     - Recursive pipeline patterns
   * - `nested.py <https://github.com/wisrovi/wpipe/tree/main/examples/07_nested_pipelines/nested.py>`_
     - Nested pipeline utilities

**Quick Example:**

.. code-block:: python

    from wpipe import Pipeline

    sub_pipeline = Pipeline()
    sub_pipeline.set_steps([
        (step_a, "Step A", "v1.0"),
        (step_b, "Step B", "v1.0"),
    ])

    main_pipeline = Pipeline()
    main_pipeline.set_steps([
        (sub_pipeline.run, "Run Sub-pipeline", "v1.0"),
        (step_c, "Step C", "v1.0"),
    ])

08 YAML Configuration (14 Examples)
----------------------------------

Load and manage pipeline configuration from YAML files.

**Location:** `examples/08_yaml_config/ <https://github.com/wisrovi/wpipe/tree/main/examples/08_yaml_config/>`_

Dynamic configuration and environment management.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Example
     - Description
   * - `01_read_yaml_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/08_yaml_config/01_read_yaml_example>`_
     - Reading YAML configuration
   * - `02_write_yaml_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/08_yaml_config/02_write_yaml_example>`_
     - Writing YAML configuration
   * - `03_pipeline_with_config_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/08_yaml_config/03_pipeline_with_config_example>`_
     - Pipeline with YAML config
   * - `04_complex_config_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/08_yaml_config/04_complex_config_example>`_
     - Complex configuration structures
   * - `05_nested_config_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/08_yaml_config/05_nested_config_example>`_
     - Nested configuration options
   * - `06_load_steps_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/08_yaml_config/06_load_steps_example>`_
     - Loading steps from config
   * - `07_dynamic_loading_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/08_yaml_config/07_dynamic_loading_example>`_
     - Dynamic configuration loading
   * - `08_validation_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/08_yaml_config/08_validation_example>`_
     - Validating configuration
   * - `09_environment_vars_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/08_yaml_config/09_environment_vars_example>`_
     - Environment variable integration
   * - `10_multi_file.py <https://github.com/wisrovi/wpipe/tree/main/examples/08_yaml_config/10_multi_file.py>`_
     - Multi-file configuration
   * - `10_nested_env_config.py <https://github.com/wisrovi/wpipe/tree/main/examples/08_yaml_config/10_nested_env_config.py>`_
     - Nested env config
   * - `config_loader.py <https://github.com/wisrovi/wpipe/tree/main/examples/08_yaml_config/config_loader.py>`_
     - Configuration loader utility

**Quick Example:**

.. code-block:: python

    from wpipe import Pipeline
    from wpipe.util import leer_yaml

    config = leer_yaml("config.yaml")
    pipeline = Pipeline(**config["pipeline"])

09 Microservice (11 Examples)
---------------------------

Build microservice workflows with wpipe.

**Location:** `examples/09_microservice/ <https://github.com/wisrovi/wpipe/tree/main/examples/09_microservice/>`_

Production-ready microservice patterns.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Example
     - Description
   * - `01_basic_service_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/09_microservice/01_basic_service_example>`_
     - Basic microservice setup
   * - `02_message_processor_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/09_microservice/02_message_processor_example>`_
     - Message processing patterns
   * - `03_service_with_pipeline_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/09_microservice/03_service_with_pipeline_example>`_
     - Service with integrated pipeline
   * - `05_health_check_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/09_microservice/05_health_check_example>`_
     - Health check implementation
   * - `06_service_state_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/09_microservice/06_service_state_example>`_
     - Service state management
   * - `07_service_validation_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/09_microservice/07_service_validation_example>`_
     - Input validation in services
   * - `08_service_metrics_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/09_microservice/08_service_metrics_example>`_
     - Metrics collection
   * - `09_service_config_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/09_microservice/09_service_config_example>`_
     - Service configuration
   * - `09_service_dependencies_example/ <https://github.com/wisrovi/wpipe/tree/main/examples/09_microservice/09_service_dependencies_example>`_
     - Managing service dependencies
   * - `10_service_graceful_shutdown.py <https://github.com/wisrovi/wpipe/tree/main/examples/09_microservice/10_service_graceful_shutdown.py>`_
     - Graceful shutdown patterns

**Quick Example:**

.. code-block:: python

    from wpipe import Pipeline

    pipeline = Pipeline(verbose=True)
    pipeline.worker_register(name="microservice", version="1.0.0")
    pipeline.set_steps([
        (process_request, "Process Request", "v1.0"),
        (validate_response, "Validate Response", "v1.0"),
    ])

Running Examples
---------------

Clone and run examples locally:

.. code-block:: bash

    git clone https://github.com/wisrovi/wpipe.git
    cd wpipe/examples/01_basic_pipeline/01_simple_function
    python example.py

Each example folder contains:

* ``example.py`` - Runnable example code
* ``README.md`` - Detailed explanation with examples

Example Directory Structure
--------------------------

::

    examples/
    ├── 01_basic_pipeline/      # 15 examples - Core pipeline functionality
    ├── 02_api_pipeline/        # 20 examples - API integration
    ├── 03_error_handling/      # 15 examples - Error handling
    ├── 04_condition/          # 12 examples - Conditional branching
    ├── 05_retry/              # 12 examples - Retry mechanisms
    ├── 06_sqlite_integration/ # 14 examples - Database operations
    ├── 07_nested_pipelines/    # 14 examples - Nested workflows
    ├── 08_yaml_config/        # 14 examples - Configuration
    ├── 09_microservice/       # 11 examples - Microservice patterns
    └── test/                  # Integration tests

Total: 100+ examples
