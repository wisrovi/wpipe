# Query Specific Records Example

## Overview

Demonstrates querying specific database records by their unique record ID.

## What It Does

1. Creates a SQLite database
2. Writes two records with different names and values
3. Retrieves the first record by its ID
4. Prints the queried record data

## Example

```python
from wpipe.sqlite import SQLite

db = SQLite(db_name="query_test.db")
id1 = db.write(input_data={"name": "test1"}, output={"value": 1})
id2 = db.write(input_data={"name": "test2"}, output={"value": 2})

record = db.read_by_id(id1)
print(f"Record 1: {record}")
```

## Data Flow

```mermaid
graph LR
    A[Write Record 1] --> B[db.write]
    B --> C[(SQLite DB)]
    C --> D[Write Record 2]
    D --> E[db.write]
    E --> C
    C --> F[db.read_by_id id1]
    F --> G[Record Data]
```

## Database Operations

```mermaid
sequenceDiagram
    participant App as Application
    participant DB as SQLite Database
    App->>DB: db.write(name=test1, value=1)
    DB-->>App: id1 (int)
    App->>DB: db.write(name=test2, value=2)
    DB-->>App: id2 (int)
    App->>DB: db.read_by_id(id1)
    DB-->>App: Record dict with id1 data
```

## Query Structure

```mermaid
graph TB
    subgraph Write_Records
        W1[Write 1] --> W2[input: {name: test1}]
        W2 --> W3[output: {value: 1}]
        W3 --> W4[id1 returned]
    end
    subgraph Write_Records2
        W5[Write 2] --> W6[input: {name: test2}]
        W6 --> W7[output: {value: 2}]
        W7 --> W8[id2 returned]
    end
    subgraph Read_By_ID
        R1[read_by_id id1] --> R2[SELECT WHERE id=id1]
        R2 --> R3[Record dict]
    end
```

## Operation States

```mermaid
stateDiagram-v2
    [*] --> CreateDB: SQLite()
    CreateDB --> Write1: db.write record 1
    Write1 --> Write2: db.write record 2
    Write2 --> ReadById: db.read_by_id(id1)
    ReadById --> Print: Print record
    Print --> Cleanup: db.__exit__()
    Cleanup --> [*]
```

## CRUD Operations

```mermaid
flowchart LR
    subgraph Create
        W1[Write test1]
        W2[Write test2]
    end
    subgraph Read
        R[read_by_id id1]
    end
    subgraph Update
        N/A[No update]
    end
    subgraph Delete
        C[db.__exit__]
    end
    W1 --> W2 --> R --> C
```
