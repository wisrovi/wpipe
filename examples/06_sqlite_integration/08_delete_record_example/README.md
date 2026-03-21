# Delete Records Example

## Overview

Demonstrates deleting specific records from a SQLite database using the delete_record method.

## What It Does

1. Creates a SQLite database
2. Writes two records (one to keep, one to delete)
3. Deletes the second record by its ID
4. Counts remaining records to verify deletion

## Example

```python
from wpipe.sqlite import SQLite

db = SQLite(db_name="delete_test.db")
id1 = db.write(input_data={"name": "keep"}, output={"value": 1})
id2 = db.write(input_data={"name": "delete"}, output={"value": 2})

db.delete_record(id2)

count = db.count_records()
print(f"Remaining records: {count}")
```

## Data Flow

```mermaid
graph LR
    A[Write keep] --> B[(SQLite DB)]
    C[Write delete] --> B
    B --> D[db.delete_record id2]
    D --> B
    B --> E[count_records]
    E --> F[1 record remaining]
```

## Database Operations

```mermaid
sequenceDiagram
    participant App as Application
    participant DB as SQLite Database
    App->>DB: db.write(name=keep, value=1)
    DB-->>App: id1
    App->>DB: db.write(name=delete, value=2)
    DB-->>App: id2
    App->>DB: db.delete_record(id2)
    DB-->>App: Success
    App->>DB: count_records()
    DB-->>App: 1
```

## Query Structure

```mermaid
graph TB
    subgraph Write_Operations
        W1[Write 1] --> W2[id1: keep]
        W3[Write 2] --> W4[id2: delete]
    end
    subgraph Delete_Operation
        D1[delete_record id2] --> D2[DELETE FROM table]
        D2 --> D3[WHERE id = id2]
    end
    subgraph Count_Operation
        C1[count_records] --> C2[SELECT COUNT(*)]
        C2 --> C3[Result: 1]
    end
```

## Operation States

```mermaid
stateDiagram-v2
    [*] --> CreateDB: SQLite()
    CreateDB --> Write1: db.write keep
    Write1 --> Write2: db.write delete
    Write2 --> Delete: db.delete_record(id2)
    Delete --> Count: count_records()
    Count --> Cleanup: db.__exit__()
    Cleanup --> [*]
```

## CRUD Operations

```mermaid
flowchart LR
    subgraph Create
        W[db.write records]
    end
    subgraph Read
        C[count_records]
    end
    subgraph Update
        N/A[No update]
    end
    subgraph Delete
        D[db.delete_record id2]
    end
    W --> D --> C
```
