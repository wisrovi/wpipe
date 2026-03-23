API Reference
=============

Complete reference for all wpipe classes, methods, and functions.

.. contents::
   :local:
   :depth: 3

1. Core Classes
---------------

1.1 Pipeline
~~~~~~~~~~~~

The main pipeline orchestration class.

.. class:: Pipeline

    **Usage:**

    .. code-block:: python

        from wpipe import Pipeline

        pipeline = Pipeline(
            worker_id=None,
            worker_name="worker",
            api_config=None,
            verbose=False,
            max_retries=0,
            retry_delay=1.0,
            retry_on_exceptions=(Exception,)
        )

    **Parameters:**

    .. py:attribute:: worker_id : Optional[str]

        Unique identifier for this worker. If provided and longer than 5 characters, enables API tracking.

        **Default:** ``None``

    .. py:attribute:: worker_name : str

        Human-readable name for the worker.

        **Default:** ``"worker"``

    .. py:attribute:: api_config : Optional[dict]

        Configuration for API integration. Should contain:

        - ``base_url``: Base URL for the API server
        - ``token``: Authentication token

        **Default:** ``None``

    .. py:attribute:: verbose : bool

        Enable verbose output with progress information.

        **Default:** ``False``

    .. py:attribute:: max_retries : int

        Maximum number of retry attempts for failed steps.

        **Default:** ``0`` (no retries)

    .. py:attribute:: retry_delay : float

        Delay in seconds between retry attempts.

        **Default:** ``1.0``

    .. py:attribute:: retry_on_exceptions : tuple

        Tuple of exception types that should trigger retries.

        **Default:** ``(Exception,)``

    .. method:: set_steps(steps: list) -> None

        Configure the pipeline steps.

        :param steps: List of step tuples (function, name, version) or Condition objects
        :type steps: list
        :raises ValueError: If step format is invalid

        **Example:**

        .. code-block:: python

            pipeline.set_steps([
                (fetch_data, "Fetch Data", "v1.0"),
                (process_data, "Process Data", "v1.0"),
                (save_data, "Save Data", "v1.0"),
            ])

    .. method:: run(*args: Any, **kwargs: Any) -> dict

        Execute the pipeline.

        :param args: Initial data dictionary
        :param kwargs: Additional keyword arguments
        :return: Dictionary containing all accumulated results from steps
        :rtype: dict
        :raises TaskError: If a step fails

        **Example:**

        .. code-block:: python

            result = pipeline.run({"initial": "data"})
            print(result)

    .. method:: set_worker_id(worker_id: str) -> None

        Set the worker ID.

        :param worker_id: Unique identifier for the worker
        :type worker_id: str
        :raises TypeError: If worker_id is not a string
        :raises ValueError: If worker_id is too short (must be > 5 chars)

    .. method:: worker_register(name: str, version: str) -> Optional[dict]

        Register the worker with the API server.

        :param name: Worker name
        :type name: str
        :param version: Worker version
        :type version: str
        :return: Worker registration data if successful, None otherwise
        :rtype: Optional[dict]

        **Example:**

        .. code-block:: python

            worker_data = pipeline.worker_register(
                name="data_processor",
                version="1.0.0"
            )

1.2 Condition
~~~~~~~~~~~~~

Represents a conditional branch in the pipeline.

.. class:: Condition

    **Usage:**

    .. code-block:: python

        from wpipe import Pipeline, Condition

        condition = Condition(
            expression="status == 'success'",
            branch_true=[(handle_success, "Handle Success", "v1.0")],
            branch_false=[(handle_failure, "Handle Failure", "v1.0")]
        )

    **Parameters:**

    .. py:attribute:: expression : str

        Python expression to evaluate. The expression has access to all data in the pipeline.

    .. py:attribute:: branch_true : list

        List of steps to execute if the condition is True.

    .. py:attribute:: branch_false : Optional[list]

        List of steps to execute if the condition is False.

    .. method:: evaluate(data: dict) -> bool

        Evaluate the condition against the data.

    .. method:: get_branch(data: dict) -> list

        Get the appropriate branch based on evaluation.

2. API Client
-------------

2.1 APIClient
~~~~~~~~~~~~~

Client for communicating with the pipeline API server.

.. class:: APIClient

    **Usage:**

    .. code-block:: python

        from wpipe import APIClient

        client = APIClient(
            base_url="http://localhost:8418",
            token="your-auth-token"
        )

    **Parameters:**

    .. py:attribute:: base_url : Optional[str]

        Base URL for the API server.

    .. py:attribute:: headers : dict

        HTTP headers for API requests.

    .. method:: send_post(endpoint: str, data: dict) -> Optional[dict]

        Send a POST request to an endpoint.

    .. method:: send_get(endpoint: str) -> Optional[dict]

        Send a GET request to an endpoint.

    .. method:: register_worker(data: dict) -> Optional[dict]

        Register a worker with the API server.

    .. method:: healthcheck_worker(data: dict) -> Optional[dict]

        Perform worker health check.

    .. method:: register_process(data: dict) -> Optional[dict]

        Register a new process with the API server.

    .. method:: end_process(data: dict) -> Optional[dict]

        End a process on the API server.

    .. method:: update_task(data: dict) -> Optional[dict]

        Update task status on the API server.

    .. method:: get_dashboard_workers() -> Optional[dict]

        Get workers dashboard information.

3. Database
------------

3.1 Wsqlite
~~~~~~~~~~~

Simplified SQLite wrapper for pipeline records.

.. class:: Wsqlite

    **Usage:**

    .. code-block:: python

        from wpipe.sqlite import Wsqlite

        with Wsqlite(db_name="results.db") as db:
            db.input = {"key": "value"}
            result = pipeline.run({"key": "value"})
            db.output = result

    **Parameters:**

    .. py:attribute:: db_name : str

        Path to the SQLite database file.

        **Default:** ``"register.db"``

    .. py:attribute:: id : Optional[str]

        ID of the current record.

    .. py:attribute:: input : dict

        Property to set input data.

    .. py:attribute:: output : dict

        Property to get/set output data.

    .. py:attribute:: details : dict

        Property to get/set details data.

3.2 SQLite
~~~~~~~~~~

Core SQLite database operations.

.. class:: SQLite

    **Usage:**

    .. code-block:: python

        from wpipe.sqlite import Sqlite

        db = Sqlite(db_name="results.db")

    **Parameters:**

    .. py:attribute:: db_name : str

        Path to the SQLite database file.

    .. method:: write(input_data, output, details, record_id)

        Write a record to the database.

    .. method:: async_write(input_data, output, details, record_id)

        Asynchronously write a record to the database.

    .. method:: read_by_id(record_id: int) -> list

        Read a record by ID.

    .. method:: export_to_dataframe(save_csv=False, csv_name="records.csv")

        Export records to a pandas DataFrame.

    .. method:: get_records_by_date_range(start_date: str, end_date: str) -> list

        Get records within a date range.

    .. method:: count_records() -> int

        Count total records in the database.

    .. method:: delete_by_id(record_id: int) -> None

        Delete a record by ID.

4. Exceptions
-------------

4.1 TaskError
~~~~~~~~~~~~~

Exception for task-related errors.

.. class:: TaskError

    **Usage:**

    .. code-block:: python

        from wpipe.exception import TaskError, Codes

        try:
            result = pipeline.run(data)
        except TaskError as e:
            print(f"Error: {e}")
            print(f"Code: {e.error_code}")

    **Attributes:**

    .. py:attribute:: error_code : int

        Error code from the Codes class.

4.2 ApiError
~~~~~~~~~~~~

Exception for API-related errors.

.. class:: ApiError

4.3 ProcessError
~~~~~~~~~~~~~~~~

Exception for process-related errors.

.. class:: ProcessError

4.4 Codes
~~~~~~~~~

Error codes for pipeline exceptions.

.. class:: Codes

    **Error Codes:**

    .. py:attribute:: TASK_FAILED : int = 502

        Task execution failed.

    .. py:attribute:: API_ERROR : int = 501

        API communication error.

    .. py:attribute:: UPDATE_PROCESS_ERROR : int = 504

        Process update failed.

    .. py:attribute:: UPDATE_TASK : int = 505

        Task update failed.

    .. py:attribute:: UPDATE_PROCESS_OK : int = 503

        Process completed successfully.

5. Utilities
------------

5.1 leer_yaml
~~~~~~~~~~~~~

Read a YAML file.

.. function:: leer_yaml(archivo, verbose=False)

    :param archivo: Path to the YAML file
    :param verbose: Enable verbose output
    :return: Dictionary with YAML contents

5.2 escribir_yaml
~~~~~~~~~~~~~~~~~

Write data to a YAML file.

.. function:: escribir_yaml(archivo, datos, verbose=False)

    :param archivo: Path to the output file
    :param datos: Dictionary to write
    :param verbose: Enable verbose output

5.3 new_logger
~~~~~~~~~~~~~~

Create and configure a new logger instance.

.. function:: new_logger(process_name="wpipe", path_file=None, filename_format="{time:YYYY-MM-DD}")

    :param process_name: Name for the logger process
    :param path_file: Directory path for log files
    :param filename_format: Format string for log filename
    :return: Configured logger instance

6. Memory Utilities
-------------------

6.1 memory
~~~~~~~~~~

Decorator to limit memory usage of a function.

.. function:: memory(percentage=0.8)

    :param percentage: Memory limit percentage
    :return: Decorated function

    **Example:**

    .. code-block:: python

        from wpipe.ram import memory

        @memory(percentage=0.8)
        def main():
            print('Memory limited to 80%')

6.2 memory_limit
~~~~~~~~~~~~~~~~

Set memory limit for the current process.

.. function:: memory_limit(percentage)

    :param percentage: Percentage of available memory (0.0 to 1.0)

    **Note:** Only works on Linux.

6.3 get_memory
~~~~~~~~~~~~~~

Get available memory in KB.

.. function:: get_memory() -> int

    :return: Available memory in kilobytes

7. Import Reference
-------------------

All public classes and functions can be imported from the main wpipe package:

.. code-block:: python

    # Main classes
    from wpipe import Pipeline, Condition, APIClient, Wsqlite

    # Exceptions
    from wpipe.exception import TaskError, ApiError, ProcessError, Codes

    # Utilities
    from wpipe.log import new_logger
    from wpipe.ram import memory
    from wpipe.util import leer_yaml, escribir_yaml