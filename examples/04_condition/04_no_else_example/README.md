# No Else Branch

Demonstrates using a condition with only a true branch, no false branch.

## What It Does

This example shows how to create a condition with an empty `branch_false` list. When the condition evaluates to false, the pipeline simply continues without executing any additional steps. This is useful for optional processing that only applies when a certain condition is met.

## Flow

```mermaid
graph LR
    A[Get Tier] --> B{tier == 'premium'?}
    B -->|True| C[Premium Process]
    B -->|False| D[Continue]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant G as Get Tier
    participant C as Condition
    participant P2 as Premium Process

    P->>G: Run get_tier
    G-->>P: {tier: 'premium'}
    P->>C: Evaluate tier == 'premium'
    C-->>P: True
    P->>P2: Run premium_process
    P2-->>P: {processed: 'premium'}
```

```mermaid
graph TB
    subgraph Pipeline
        A1[get_tier<br/>returns: tier, name]
        A2[Condition<br/>tier == 'premium']
        A3[premium_process<br/>processed, discount]
    end
    A1 --> A2
    A2 -->|True| A3
    A2 -->|False| D[Continue<br/>No-op]
```

```mermaid
stateDiagram-v2
    [*] --> GetTier
    GetTier --> CheckTier: tier received
    CheckTier --> ProcessPremium: tier == 'premium'
    CheckTier --> Continue: tier != 'premium'
    ProcessPremium --> [*]
    Continue --> [*]
```

```mermaid
flowchart LR
    subgraph Scenarios
        S1["tier = 'premium'"]
        S2["tier = 'standard'"]
    end
    subgraph Actions
        A1["Run premium_process"]
        A2["Continue (no-op)"]
    end
    S1 --> C{tier == 'premium'?}
    S2 --> C
    C -->|True| A1
    C -->|False| A2
```
