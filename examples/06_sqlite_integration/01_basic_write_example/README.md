# Basic Write and Read Example

## Overview

Demonstrates the simplest SQLite integration: writing a record to the database and reading it back by ID.

## What It Does

1. Creates a SQLite database file
2. Writes a record with input and output data
3. Reads the record back using its ID
4. Counts total records in the database

## Example

```python
from wpipe.sqlite import SQLite

db = SQLite(db_name="test_basic.db")
record_id = db.write(input_data={"name": "test", "value": 100}, output={"result": "success"})
records = db.read_by_id(record_id)
count = db.count_records()
```

## Data Flow

```mermaid
graph LR
    A[App] --> B[SQLite.write]
    B --> C[(Database)]
    C --> D[SQLite.read_by_id]
    D --> E[Record Data]
```

## Database Operations

```mermaid
sequenceDiagram
    participant App as Application
    participant DB as SQLite Database
    App->>DB: write(input_data, output)
    DB-->>App: record_id (int)
    App->>DB: read_by_id(record_id)
    DB-->>App: record dict
    App->>DB: count_records()
    DB-->>App: count (int)
```

## Query Structure

```mermaid
graph TB
    subgraph Write_Operation
        W1[input_data: dict] --> W2[output: dict]
        W2 --> W3[SQLite.write]
    end
    subgraph Read_Operation
        R1[record_id: int] --> R2[SQLite.read_by_id]
        R2 --> R3[record: dict]
    end
    subgraph Count_Operation
        C1[SQLite.count_records] --> C2[count: int]
    end
```

## Operation States

```mermaid
stateDiagram-v2
    [*] --> Init: Create SQLite instance
    Init --> Write: db.write()
    Write --> Read: db.read_by_id()
    Read --> Count: db.count_records()
    Count --> Cleanup: db.__exit__()
    Cleanup --> [*]
```

## CRUD Operations

```mermaid
flowchart LR
    subgraph Create
        W[write input_data, output]
    end
    subgraph Read
        R[read_by_id record_id]
    end
    subgraph Update
        U[update_record]
    end
    subgraph Delete
        D[delete_record]
    end
    W --> R --> U --> D
```
