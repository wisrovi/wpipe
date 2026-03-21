# Wsqlite Context Manager Example

## Overview

Demonstrates using Wsqlite as a context manager for convenient database operations with automatic resource cleanup.

## What It Does

1. Opens a SQLite database using the Wsqlite context manager
2. Sets input data on a new record
3. Sets output data on the same record
4. Counts total records in the database
5. Automatically closes the database on exit

## Example

```python
from wpipe.sqlite import Wsqlite

with Wsqlite(db_name="test.db") as db:
    db.input = {"name": "pipeline_run", "id": 123}
    db.output = {"result": "completed", "value": 42}
    print(f"Total records: {db.count()}")
```

## Data Flow

```mermaid
graph LR
    A[App] --> B[with Wsqlite]
    B --> C[db.input]
    C --> D[(Database)]
    D --> E[db.output]
    E --> F[db.count]
    F --> G[Auto Cleanup]
```

## Database Operations

```mermaid
sequenceDiagram
    participant App as Application
    participant DB as Wsqlite Context
    participant Storage as SQLite Storage
    App->>DB: with Wsqlite(db_name)
    DB->>Storage: Open database
    App->>DB: db.input = data
    DB->>Storage: Create record, set input
    Storage-->>DB: record_id
    DB-->>App: db.id
    App->>DB: db.output = data
    DB->>Storage: Update record with output
    App->>DB: db.count()
    Storage-->>DB: record count
    DB-->>App: count
    App->>DB: Exit context
    DB->>Storage: Close database
```

## Query Structure

```mermaid
graph TB
    subgraph Context_Manager
        C1[with Wsqlite] --> C2[Open DB]
        C2 --> C3[Auto __enter__]
    end
    subgraph Input_Operation
        I1[db.input = dict] --> I2[Create Record]
        I2 --> I3[db.id returned]
    end
    subgraph Output_Operation
        O1[db.output = dict] --> O2[Update Record]
    end
    subgraph Cleanup
        CL1[Exit context] --> CL2[Auto __exit__]
        CL2 --> CL3[Close DB]
    end
```

## Operation States

```mermaid
stateDiagram-v2
    [*] --> Open: with Wsqlite()
    Open --> SetInput: db.input = data
    SetInput --> SetOutput: db.output = data
    SetOutput --> Count: db.count()
    Count --> Close: Exit context
    Close --> [*]
```

## CRUD Operations

```mermaid
flowchart LR
    subgraph Create
        IN[db.input sets input]
    end
    subgraph Read
        ID[db.id returns record_id]
    end
    subgraph Update
        OUT[db.output updates record]
    end
    subgraph Delete
        CONTEXT[Auto cleanup on exit]
    end
    IN --> ID --> OUT --> CONTEXT
```
