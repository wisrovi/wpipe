<img width="1682" height="943" alt="image" src="https://github.com/user-attachments/assets/9618bcca-4253-43b1-a483-7941a1130edf" />

<p align="center">
  <a href="https://pypi.org/project/wpipe/"><img src="https://img.shields.io/pypi/v/wpipe?style=for-the-badge&logo=pypi&color=3b82f6" alt="PyPI version" /></a>
  <a href="https://pypi.org/project/wpipe/"><img src="https://img.shields.io/pypi/dm/wpipe?style=for-the-badge&color=10b981" alt="PyPI Downloads" /></a>
  <a href="https://pypi.org/project/wpipe/"><img src="https://img.shields.io/pypi/pyversions/wpipe?style=for-the-badge&logo=python&color=ffd343&logoColor=black" alt="Python Versions" /></a>
  <a href="https://linkedin.com/in/wisrovi-rodriguez"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
  <a href="https://wisrovi.dev"><img src="https://img.shields.io/badge/Author-wisrovi.dev-111827?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Portal" /></a>
  <a href="https://orcid.org/0009-0005-0710-1861"><img src="https://img.shields.io/badge/ORCID-0009--0005--0710--1861-A6CE39?style=for-the-badge&logo=orcid&logoColor=white" alt="ORCID" /></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="License" /></a>
</p>

# 🚀 WPipe: Enterprise Pipeline & Directed Acyclic Graph (DAG) Orchestrator

**The fastest, most resilient, and purest pipeline orchestration engine for Python.**

WPipe is an enterprise-grade framework designed to automate complex, high-throughput computational workflows. It guarantees zero data loss, ultra-low execution latency, and deterministic post-mortem diagnosis. Featuring **native sync & async runtime parity**, **transparent GIL-bypass multiprocessing**, **forensic error capture**, and an interactive **Live Real-time Web Dashboard**.

---

## 📑 Table of Contents

- [🏛️ Architectural Overview](#️-architectural-overview)
- [💎 Why WPipe?](#-why-wpipe)
- [📦 Installation](#-installation)
- [🛠️ Key Technologies and Libraries](#️-key-technologies-and-libraries)
- [🧩 VS Code Official Extension (WPipe Tools)](#-vs-code-official-extension-wpipe-tools)
- [🚀 5-Minute Quick Start](#-5-minute-quick-start)
- [🧩 Core Composition Blocks](#-core-composition-blocks)
  - [1. Sequential Pipeline (`Pipeline` / `PipelineAsync`)](#1-sequential-pipeline-pipeline--pipelineasync)
  - [2. Parallel Execution (`Parallel`)](#2-parallel-execution-parallel)
  - [3. Conditional Routing (`Condition`)](#3-conditional-routing-condition)
  - [4. Iterative Execution (`For`)](#4-iterative-execution-for)
  - [5. Background Fire & Forget Tasks (`Background`)](#5-background-fire--forget-tasks-background)
- [🔍 Forensic Error Capture & Telemetry](#-forensic-error-capture--telemetry)
- [📊 Real-time Visual Web Dashboard](#-real-time-visual-web-dashboard)
- [⚙️ Configuration & Database Tracking](#️-configuration--database-tracking)
- [🧪 Unit Testing & Quality Assurance](#-unit-testing--quality-assurance)
- [👤 Author & Official Affiliation](#-author--official-affiliation)
- [📜 License](#-license)

---

## 🏛️ Architectural Overview

```
+========================================================================================+
|                                    WPIPE ECOSYSTEM                                     |
+========================================================================================+
|                                                                                        |
|   🔌 DECLARATIVE ORCHESTRATION ENGINE (`Pipeline` / `PipelineAsync`)                   |
|   +--------------------------------------------------------------------------------+   |
|   |  • Dual Runtime: Synchronous and Asynchronous (`asyncio`) complete parity       |   |
|   |  • Composition Blocks: Parallel (Processes/Threads), Condition, For, Background |   |
|   |  • Step Decorator: Inline `@step` with strict type hints & auto-DTO reflection |   |
|   +--------------------------------------------------------------------------------+   |
|                                          |                                             |
|                                          v                                             |
|   🛡️ RESILIENCE, INTEGRITY & RECOVERY LAYER                                           |
|   +--------------------------------------------------------------------------------+   |
|   |  • Forensic Error Capture: Line-accurate exception traces and context dumps    |   |
|   |  • Automatic Checkpointing: Resume execution from latest committed state        |   |
|   |  • Lightning Database Engine: High-concurrency WAL mode via `wsqlite`           |   |
|   +--------------------------------------------------------------------------------+   |
|                                          |                                             |
|                                          v                                             |
|   📊 TELEMETRY, METRICS & VISUAL OBSERVABILITY                                         |
|   +--------------------------------------------------------------------------------+   |
|   |  • Real-time Web Dashboard: Interactive DAG graphs, metrics, and event alerts  |   |
|   |  • Resource Monitoring: Non-intrusive CPU & RAM consumption tracking           |   |
|   |  • VS Code WPipe Tools: Live DAG visualization, snippets, and step catalog      |   |
|   +--------------------------------------------------------------------------------+   |
+========================================================================================+
```

---

## 💎 Why WPipe?

Traditional linear scripts and ad-hoc pipelines lack resilience, observability, and structured error handling.

| Capability | Impact & Engineering Benefit |
| :--- | :--- |
| ⚡ **Lightning Storage Engine** | Uses `wsqlite` with WAL mode and thread-safe connection pooling for sub-millisecond tracking persistence. |
| 🧵 **Native Multiprocessing & Multithreading** | Transparently runs CPU-heavy steps across isolated processes to bypass the Python GIL or lightweight I/O threads. |
| 🛡️ **Intelligent Checkpointing** | Resilient against non-serializable objects and circular references. Recovers cleanly after system halts. |
| 🔍 **Forensic Error Capturing** | Pinpoints the exact file, line number, and execution context that caused failures, preventing silent dropouts. |
| ⚡ **Background Tasks (`Background`)** | Fire-and-forget asynchronous tasks that execute without blocking the critical DAG execution path. |
| 🔄 **Sync / Async Parity** | 100% architectural parity between synchronous `Pipeline` and coroutine-driven `PipelineAsync`. |

---

## 📦 Installation

```bash
# Standard installation from PyPI
pip install wpipe

# Using poetry
poetry add wpipe
```

---

## 🛠️ Key Technologies and Libraries

WPipe is built on top of high-performance modern Python standards:

- **Python (3.9 - 3.14)**: Modern typed runtime with strict type annotations.
- **WSQLite (`wsqlite`)**: Optimized SQLite persistence engine operating in high-concurrency WAL (Write-Ahead Logging) mode.
- **Pydantic (v1 / v2)**: Strict data contract validation and automatic DTO model serialization.
- **FastAPI & Uvicorn**: Underlying REST server powering the real-time interactive web dashboard.
- **Loguru**: Structured, asynchronous diagnostic logging.
- **PSUtil**: Real-time system telemetry tracking per-step CPU and RAM utilization.
- **Pytest**: Comprehensive test suite ensuring zero-regression execution across all modules.

---

## 🧩 VS Code Official Extension (WPipe Tools)

WPipe features an official **VS Code extension** (`WPipe Tools`) to accelerate development, debugging, and live visual inspection:

- **Installation:** Search for `WPipe Tools` in the VS Code Marketplace or run:
  ```bash
  ext install wpipe.wpipe-vscode
  ```
- **Live DAG Visualizer:** Open the Command Palette (`Ctrl+Shift+P`) and select `WPipe: Preview Pipeline DAG`.

### 🧠 Developer Snippets
Type `wp` in any Python file to trigger productive scaffolding:

| Snippet | Keyword | Description |
| :--- | :--- | :--- |
| **WPipe Complete** | `wppipecomplete` | Complete enterprise pipeline with error capture, break-on-error, checkpoints, and resource metrics. |
| **WPipe Advanced** | `wppipeadv` | Resilient pipeline with retries, configuration handling, and alerts. |
| **WPipe Basic** | `wppipe` | Clean standard pipeline with database tracking. |
| **WPipe Step Func** | `wpstep` | Lightweight functional step. |
| **WPipe Step Class** | `wpstepadv` | Class-based step with retries, timeouts, and Pydantic DTO typing. |
| **WPipe Error Capture** | `wperrorcapture` | Registers forensic error handler. |

---

## 🚀 5-Minute Quick Start

### Basic Pipeline with Step Decorators
```python
from wpipe import Pipeline, step

# 1. Define modular pipeline steps
@step(name="IngestData", version="1.0.0")
def ingest_data(context: dict) -> dict:
    context["raw_records"] = [10, 20, 30, 40]
    return context

@step(name="ProcessData", version="1.0.0")
def process_data(context: dict) -> dict:
    context["sum_total"] = sum(context["raw_records"])
    return context

# 2. Instantiate and run pipeline
pipe = Pipeline(pipeline_name="quickstart_pipeline")
pipe.set_steps([ingest_data, process_data])

result = pipe.run({"status": "INIT"})
print(f"Pipeline Result: {result['sum_total']}")  # 100
```

---

## 🧩 Core Composition Blocks

WPipe allows flexible workflow assembly using 5 native orchestration blocks:

```python
from wpipe import Pipeline, PipelineAsync, Background, Condition, For, Parallel, step
```

### 1. Sequential Pipeline (`Pipeline` / `PipelineAsync`)
Executes a linear sequence of steps, validating outputs and recording telemetry.

```python
pipe = Pipeline(pipeline_name="order_processing")
pipe.set_steps([validate_order, charge_payment, notify_customer])
pipe.run(order_payload)
```

### 2. Parallel Execution (`Parallel`)
Executes multiple steps simultaneously using either threads (I/O bound) or isolated processes (CPU bound):

```python
pipe.set_steps([
    Parallel([
        generate_pdf_report,
        generate_excel_summary,
        broadcast_webhook,
    ], mode="threads", max_workers=3)
])
```

### 3. Conditional Routing (`Condition`)
Branches execution paths dynamically based on data inside the context:

```python
pipe.set_steps([
    Condition(
        condition=lambda ctx: ctx.get("is_vip", False),
        if_true=[apply_vip_discount, priority_dispatch],
        if_false=[apply_standard_discount]
    )
])
```

### 4. Iterative Execution (`For`)
Iterates over a list in the context, processing items with configurable merge policies (`accumulate`, `last_wins`):

```python
pipe.set_steps([
    For(
        items="image_urls",
        step=download_and_resize_image,
        merge_policy="accumulate"
    )
])
```

### 5. Background Fire & Forget Tasks (`Background`)
Offloads non-critical, slow operations (e.g. audit logs, cleanup, telemetry pushes) to daemon threads without blocking pipeline throughput:

```python
pipe.set_steps([
    process_transaction,
    Background(send_audit_telemetry),  # Runs in daemon thread; does not block pipeline!
    return_response_to_client
])
```

---

## 🔍 Forensic Error Capture & Telemetry

Configure fail-fast guarantees and pinpoint exact exception origins:

```python
def on_pipeline_failure(error_info: dict) -> None:
    print(f"🚨 Failed at Step: {error_info['step_name']}")
    print(f"   Exception: {error_info['error_message']}")
    print(f"   Origin: {error_info['file_name']}:{error_info['line_number']}")

pipe = Pipeline(pipeline_name="critical_billing")
pipe.add_error_capture(on_pipeline_failure, break_on_error=True)
```

---

## 📊 Real-time Visual Web Dashboard

Launch the embedded real-time web dashboard with a single command to inspect DAG execution, latency waterfalls, and database checkpoints:

```python
from wpipe import start_dashboard

# Starts dashboard on http://localhost:8080
start_dashboard(db_path="wpipe_tracking.db", port=8080)
```

---

## ⚙️ Configuration & Database Tracking

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `pipeline_name` | `str` | `"Pipeline"` | Human-readable pipeline identifier. |
| `tracking_db` | `str` | `None` | Path to SQLite tracking database (WAL mode). |
| `collect_system_metrics` | `bool` | `False` | Enables real-time CPU and RAM percentage tracking. |
| `show_progress` | `bool` | `True` | Displays rich console progress indicators in terminal. |
| `max_retries` | `int` | `0` | Number of automated step retries on failure. |
| `retry_delay` | `float` | `0.0` | Delay in seconds between retries. |

---

## 🧪 Unit Testing & Quality Assurance

WPipe maintains an exhaustive test suite verifying sync/async pipelines, parallel execution, loop iterations, and database integrity:

```bash
# Run all unit tests
pytest test/ -v
```

---

## 👤 Author & Official Affiliation

* **William Steve Rodriguez Villamizar (Wisrovi)**
* **Role:** AI Leader & Solutions Architect at eCaptureDtech | Principal AI Engineer
* 📧 **Email:** [wisrovi.rodriguez@gmail.com](mailto:wisrovi.rodriguez@gmail.com)
* 🌐 **Official Portal:** [wisrovi.dev](https://wisrovi.dev)
* 💼 **LinkedIn:** [wisrovi-rodriguez](https://www.linkedin.com/in/wisrovi-rodriguez/)
* 🆔 **ORCID:** [0009-0005-0710-1861](https://orcid.org/0009-0005-0710-1861)
* 📦 **PyPI:** [pypi.org/user/wisrovi/](https://pypi.org/user/wisrovi/)
* 🐙 **GitHub:** [@wisrovi](https://github.com/wisrovi)

---

## 📜 License

Distributed under the **MIT License**. Free for commercial, enterprise, and academic research use.
