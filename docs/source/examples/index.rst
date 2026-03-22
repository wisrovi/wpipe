Examples Gallery
==============

Explore 100+ examples organized by functionality. Each example includes code, explanation, and Mermaid diagrams.

::::{note}
All examples are located in the `examples/` directory of the repository.
::::

.. _basic-pipeline:

Basic Pipeline (01)
------------------

Simple pipelines with functions, classes, and data flow.

::::{grid} 1 1 2 3
:gutter: 2

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/01_basic_pipeline/01_simple_function
:link-type: url

### Simple Function

Basic pipeline with a single function step.

```{image} https://img.shields.io/badge/01-Simple%20Function-blue
```
:::

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/01_basic_pipeline/02_class_steps
:link-type: url

### Class Steps

Using class instances as pipeline steps.

```{image} https://img.shields.io/badge/02-Class%20Steps-blue
```
:::

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/01_basic_pipeline/03_mixed_steps
:link-type: url

### Mixed Steps

Combining functions and classes.

```{image} https://img.shields.io/badge/03-Mixed%20Steps-blue
```
:::
::::

**View all 15 basic examples:** [examples/01_basic_pipeline/](https://github.com/wisrovi/wpipe/tree/main/examples/01_basic_pipeline/)

.. _api-pipeline:

API Pipeline (02)
-----------------

Connect pipelines to external APIs for tracking and monitoring.

::::{grid} 1 1 2 3
:gutter: 2

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/01_basic_api
:link-type: url

### Basic API

Connect to external API server.

```{image} https://img.shields.io/badge/API-Basic-green
```
:::

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/04_api_errors
:link-type: url

### API Errors

Handle API connection errors.

```{image} https://img.shields.io/badge/API-Errors-green
```
:::

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/06_full_config
:link-type: url

### Full Config

Complete API configuration example.

```{image} https://img.shields.io/badge/API-Full%20Config-green
```
:::
::::

**View all 21 API examples:** [examples/02_api_pipeline/](https://github.com/wisrovi/wpipe/tree/main/examples/02_api_pipeline/)

.. _error-handling:

Error Handling (03)
------------------

Robust error handling patterns and recovery.

::::{grid} 1 1 2 3
:gutter: 2

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/03_error_handling/01_basic_error_example
:link-type: url

### Basic Errors

Simple error catching and handling.

```{image} https://img.shields.io/badge/Errors-Basic-orange
```
:::

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/03_error_handling/04_middle_error_example
:link-type: url

### Middle Errors

Errors in the middle of pipelines.

```{image} https://img.shields.io/badge/Errors-Middle-orange
```
:::

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/03_error_handling/09_partial_results_example
:link-type: url

### Partial Results

Accessing partial results on failure.

```{image} https://img.shields.io/badge/Errors-Partial-orange
```
:::
::::

**View all 10 error handling examples:** [examples/03_error_handling/](https://github.com/wisrovi/wpipe/tree/main/examples/03_error_handling/)

.. _condition:

Conditional Branching (04)
--------------------------

Execute different paths based on data conditions.

::::{grid} 1 1 2 3
:gutter: 2

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/04_condition/01_basic_condition
:link-type: url

### Basic Condition

Simple conditional branching.

```{image} https://img.shields.io/badge/Condition-Basic-purple
```
:::

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/04_condition/02_string_condition
:link-type: url

### String Condition

String-based conditions.

```{image} https://img.shields.io/badge/Condition-String-purple
```
:::

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/04_condition/05_invalid_expression
:link-type: url

### Invalid Expression

Handling invalid conditions.

```{image} https://img.shields.io/badge/Condition-Invalid-purple
```
:::
::::

**View all 9 condition examples:** [examples/04_condition/](https://github.com/wisrovi/wpipe/tree/main/examples/04_condition/)

.. _retry:

Retry Logic (05)
----------------

Automatic retries for failed operations.

::::{grid} 1 1 2 3
:gutter: 2

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/05_retry/01_basic_retry
:link-type: url

### Basic Retry

Simple retry configuration.

```{image} https://img.shields.io/badge/Retry-Basic-red
```
:::

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/05_retry/03_retry_with_wait
:link-type: url

### Retry with Wait

Retry with wait between attempts.

```{image} https://img.shields.io/badge/Retry-Wait-red
```
:::

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/05_retry/05_exponential_backoff
:link-type: url

### Exponential Backoff

Increasing wait time between retries.

```{image} https://img.shields.io/badge/Retry-Backoff-red
```
:::
::::

**View all 9 retry examples:** [examples/05_retry/](https://github.com/wisrovi/wpipe/tree/main/examples/05_retry/)

.. _sqlite:

SQLite Integration (06)
-----------------------

Persist pipeline results to SQLite databases.

::::{grid} 1 1 2 3
:gutter: 2

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/06_sqlite_integration/01_basic_write
:link-type: url

### Basic Write

Write pipeline results to SQLite.

```{image} https://img.shields.io/badge/SQLite-Write-cyan
```
:::

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/06_sqlite_integration/03_read_query
:link-type: url

### Read & Query

Read and query stored results.

```{image} https://img.shields.io/badge/SQLite-Query-cyan
```
:::

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/06_sqlite_integration/07_json_storage
:link-type: url

### JSON Storage

Store complex data as JSON.

```{image} https://img.shields.io/badge/SQLite-JSON-cyan
```
:::
::::

**View all 9 SQLite examples:** [examples/06_sqlite_integration/](https://github.com/wisrovi/wpipe/tree/main/examples/06_sqlite_integration/)

.. _nested:

Nested Pipelines (07)
---------------------

Compose complex workflows with nested pipelines.

::::{grid} 1 1 2 3
:gutter: 2

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/07_nested_pipelines/01_basic_nested
:link-type: url

### Basic Nested

Simple nested pipeline structure.

```{image} https://img.shields.io/badge/Nested-Basic-pink
```
:::

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/07_nested_pipelines/03_data_flow
:link-type: url

### Data Flow

Data flow through nested pipelines.

```{image} https://img.shields.io/badge/Nested-Flow-pink
```
:::

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/07_nested_pipelines/07_multiple_levels
:link-type: url

### Multiple Levels

Deeply nested pipelines.

```{image} https://img.shields.io/badge/Nested-Deep-pink
```
:::
::::

**View all 9 nested examples:** [examples/07_nested_pipelines/](https://github.com/wisrovi/wpipe/tree/main/examples/07_nested_pipelines/)

.. _yaml-config:

YAML Configuration (08)
-----------------------

Load and manage pipeline configuration from YAML files.

::::{grid} 1 1 2 3
:gutter: 2

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/08_yaml_config/01_basic_yaml
:link-type: url

### Basic YAML

Load configuration from YAML.

```{image} https://img.shields.io/badge/YAML-Basic-yellow
```
:::

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/08_yaml_config/03_save_load
:link-type: url

### Save & Load

Save and load pipeline state.

```{image} https://img.shields.io/badge/YAML-Save-yellow
```
:::

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/08_yaml_config/07_nested_config
:link-type: url

### Nested Config

Complex nested configuration.

```{image} https://img.shields.io/badge/YAML-Nested-yellow
```
:::
::::

**View all 9 YAML examples:** [examples/08_yaml_config/](https://github.com/wisrovi/wpipe/tree/main/examples/08_yaml_config/)

.. _microservice:

Microservice (09)
------------------

Build microservice workflows with wpipe.

::::{grid} 1 1 2 3
:gutter: 2

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/09_microservice/01_basic_service
:link-type: url

### Basic Service

Simple microservice setup.

```{image} https://img.shields.io/badge/Service-Basic-teal
```
:::

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/09_microservice/03_api_integration
:link-type: url

### API Integration

Microservice with API tracking.

```{image} https://img.shields.io/badge/Service-API-teal
```
:::

:::{grid-item-card}
:link: https://github.com/wisrovi/wpipe/tree/main/examples/09_microservice/05_health_check
:link-type: url

### Health Check

Health check endpoint implementation.

```{image} https://img.shields.io/badge/Service-Health-teal
```
:::
::::

**View all 9 microservice examples:** [examples/09_microservice/](https://github.com/wisrovi/wpipe/tree/main/examples/09_microservice/)

Running Examples
----------------

Clone and run examples locally:

.. code-block:: bash

    git clone https://github.com/wisrovi/wpipe.git
    cd wpipe/examples/01_basic_pipeline/01_simple_function
    python example.py

Each example folder contains:
- ``example.py`` - Runnable example code
- ``README.md`` - Detailed explanation with Mermaid diagrams

Contributing Examples
--------------------

We welcome new examples! See the repository for contribution guidelines.
