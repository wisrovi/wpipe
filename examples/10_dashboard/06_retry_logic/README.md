# Example 06: Retry Logic

Shows automatic retry functionality with tracking of retry attempts.

## Retry Flow

```mermaid
flowchart TD
    A[Start] --> B{Execute Step}
    B -->|Success| C[Continue]
    B -->|Fail| D{Retry Count < Max?}
    D -->|Yes| E[Wait Delay]
    E --> B
    D -->|No| F[Mark Failed]
    
    B -.->|Attempt 1| T[Tracker]
    B -.->|Attempt 2| T
    B -.->|Attempt 3| T
```

## Retry Configuration

```mermaid
classDiagram
    class RetryConfig {
        +int max_retries
        +float retry_delay
        +tuple retry_on_exceptions
        +bool exponential_backoff
    }
    
    RetryConfig --> Pipeline
```

## Tracking Retries

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant T as Tracker
    
    P->>T: start_step(attempt=1)
    T->>DB: INSERT step
    P->>P: Execute - FAILS
    P->>P: Wait 0.5s
    P->>T: start_step(attempt=2)
    T->>DB: INSERT step
    P->>P: Execute - FAILS
    P->>P: Wait 0.5s
    P->>T: start_step(attempt=3)
    P->>P: Execute - SUCCESS
```

## Run

```bash
cd examples/10_dashboard/06_retry_logic
python example.py
```
