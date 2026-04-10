# WPIPE Dashboard - Start Options

This document shows different ways to start the wpipe Dashboard.

## Prerequisites

Install dashboard dependencies:
```bash
pip install -e ".[dashboard]"
```

## Option 1: CLI Command

```bash
wpipe --dashboard --db pipeline_data.db --port 8000 --open
```

## Option 2: Python Module

```bash
python -m wpipe.dashboard --db pipeline_data.db --port 8000 --open
```

## Option 3: Python Code

### Option A: Using start_dashboard function
```python
from wpipe import start_dashboard

start_dashboard(
    db_path="pipeline_data.db",
    host="127.0.0.1",
    port=8000,
    open_browser=True
)
```

### Option B: Using uvicorn directly
```python
import uvicorn
from wpipe.dashboard.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `--host` | Host to bind | `127.0.0.1` |
| `--port` | Port to bind | `8000` |
| `--db` | SQLite database path | `register.db` |
| `--open` | Automatically open browser | `False` |
| `--reload` | Enable auto-reload for development | `False` |

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Dashboard HTML |
| `GET /api/health` | Health check |
| `GET /api/records` | List records (supports `?limit`, `?offset`, `?search`) |
| `GET /api/records/<id>` | Get specific record |
| `GET /api/stats` | Get statistics |
| `GET /api/config` | Get current configuration |
| `POST /api/config` | Update configuration |
