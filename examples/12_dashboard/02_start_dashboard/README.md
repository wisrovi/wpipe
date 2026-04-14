# Example 02: Start Dashboard

Learn how to launch and configure the wpipe dashboard.

## Dashboard Access Methods

```mermaid
flowchart LR
    A[CLI] --> D[Dashboard]
    B[Python Module] --> D
    C[Programmatic] --> D
    
    D --> DB[(SQLite)]
    D --> UI[Web Browser]
```

## Startup Options

```mermaid
graph TB
    subgraph "Options"
        O1[--db path]
        O2[--config-dir path]
        O3[--port number]
        O4[--open auto]
    end
    
    O1 --> C[Dashboard]
    O2 --> C
    O3 --> C
    O4 --> C
```

## Architecture Overview

```mermaid
flowchart TB
    subgraph "wpipe System"
        P[Pipeline] --> T[Tracker]
        T --> DB[(SQLite)]
    end
    
    D[Dashboard] --> DB
    D --> UI[Browser]
    
    subgraph "Dashboard Components"
        D --> S[Stats]
        D --> G[Graph]
        D --> A[Analytics]
        D --> AL[Alerts]
    end
```

## Run Methods

```bash
# Method 1: CLI
python -m wpipe.dashboard --db wpipe_dashboard.db --config-dir configs --open

# Method 2: Python
python -c "from wpipe import start_dashboard; start_dashboard('wpipe_dashboard.db')"

# Method 3: Shell script
./run_dashboard.sh
```

## Key Features

- ✅ Multiple startup methods
- ✅ Configurable port and database
- ✅ Auto browser opening
- ✅ Real-time data refresh
