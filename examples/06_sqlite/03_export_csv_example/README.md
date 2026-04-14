# Export to CSV Example

## Overview

Demonstrates exporting database records to a pandas DataFrame and saving the data as a CSV file.

## What It Does

1. Creates a SQLite database
2. Writes multiple records with index and value data
3. Exports all records to a pandas DataFrame
4. Saves the DataFrame to a CSV file
5. Prints the DataFrame and record count

## Example

```python
from wpipe.sqlite import SQLite

db = SQLite(db_name="test_export.db")
for i in range(5):
    db.write(input={"index": i}, output={"value": i * 10})

df = db.export_to_dataframe(save_csv=True, csv_name="export.csv")
print(df)
```

## Data Flow

```mermaid
graph LR
    A[Write Records] --> B[db.write loop]
    B --> C[(SQLite DB)]
    C --> D[export_to_dataframe]
    D --> E[DataFrame]
    E --> F[save_csv]
    F --> G[export.csv]
```

## Database Operations

```mermaid
sequenceDiagram
    participant App as Application
    participant DB as SQLite Database
    participant CSV as CSV File
    App->>DB: for i in range(5): db.write()
    DB-->>App: record_ids
    App->>DB: export_to_dataframe(save_csv=True)
    DB->>CSV: Write CSV file
    CSV-->>DB: File saved
    DB-->>App: DataFrame
    App->>CSV: Print results
```

## Query Structure

```mermaid
graph TB
    subgraph Write_Loop
        W1[for i in range(5)] --> W2[db.write input, output]
    end
    subgraph Export
        E1[export_to_dataframe] --> E2[DataFrame]
        E2 --> E3[save_csv=True]
        E3 --> E4[CSV file created]
    end
    subgraph Query
        Q1[count_records] --> Q2[Total count]
    end
```

## Operation States

```mermaid
stateDiagram-v2
    [*] --> CreateDB: SQLite(db_name)
    CreateDB --> InsertLoop: for i in range(5)
    InsertLoop --> Write: db.write()
    Write --> Export: export_to_dataframe()
    Export --> SaveCSV: save_csv=True
    SaveCSV --> Cleanup: db.__exit__()
    Cleanup --> [*]
```

## CRUD Operations

```mermaid
flowchart LR
    subgraph Create
        W[db.write records]
    end
    subgraph Read
        DF[export_to_dataframe]
    end
    subgraph Update
        CSV[save to CSV]
    end
    subgraph Delete
        CLEANUP[remove temp files]
    end
    W --> DF --> CSV --> CLEANUP
```
