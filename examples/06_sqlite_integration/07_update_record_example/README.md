# Update Records Example

## Overview

Demonstrates updating existing records in a SQLite database using the update_record method.

## What It Does

1. Creates a SQLite database
2. Writes a new record with initial value of 0
3. Updates the record's output data with a new value of 100
4. Reads the updated record to verify the change

## Example

```python
from wpipe.sqlite import SQLite

db = SQLite(db_name="update_test.db")
record_id = db.write(input_data={"name": "original"}, output={"value": 0})
db.update_record(record_id, output={"value": 100})
record = db.read_by_id(record_id)
print(f"Updated record: {record}")
```

## Data Flow

```mermaid
graph LR
    A[db.write initial] --> B[SQLite DB]
    B --> C[db.update_record]
    C --> D[SQLite DB updated]
    D --> E[db.read_by_id]
    E --> F[Updated record]
```

## Database Operations

```mermaid
sequenceDiagram
    participant App as Application
    participant DB as SQLite Database
    App->>DB: db.write(name=original, value=0)
    DB-->>App: record_id
    App->>DB: db.update_record(id, output={value: 100})
    DB-->>App: Success
    App->>DB: db.read_by_id(record_id)
    DB-->>App: Updated record dict
```

## Query Structure

```mermaid
graph TB
    subgraph Write_Step
        W1[write] --> W2[input: {name: original}]
        W2 --> W3[output: {value: 0}]
        W3 --> W4[record_id]
    end
    subgraph Update_Step
        U1[update_record] --> U2[SET output]
        U2 --> U3[WHERE id=record_id]
        U3 --> U4[New output: {value: 100}]
    end
    subgraph Read_Step
        R1[read_by_id] --> R2[SELECT * WHERE id]
        R2 --> R3[Updated record]
    end
```

## Operation States

```mermaid
stateDiagram-v2
    [*] --> CreateDB: SQLite()
    CreateDB --> Write: db.write initial
    Write --> Update: db.update_record
    Update --> Read: db.read_by_id
    Read --> Verify: Check updated value
    Verify --> Cleanup: db.__exit__()
    Cleanup --> [*]
```

## CRUD Operations

```mermaid
flowchart LR
    subgraph Create
        W[db.write initial record]
    end
    subgraph Read
        R[db.read_by_id]
    end
    subgraph Update
        U[db.update_record]
    end
    subgraph Delete
        C[db.__exit__]
    end
    W --> U --> R --> C
```
