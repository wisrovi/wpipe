# 03 Mixed Steps

Functions and classes working together in pipeline.

```mermaid
flowchart LR
    A[Start] --> B[extract_numbers]
    B --> C[SumNumbers class]
    C --> D[calculate_average]
    D --> E[Result]
```
