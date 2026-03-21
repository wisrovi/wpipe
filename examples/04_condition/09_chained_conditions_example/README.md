# Chained Conditions

Demonstrates chaining/nesting multiple conditions for hierarchical decision making.

## What It Does

This example shows how to nest conditions within other conditions to create hierarchical decision trees. The outer condition checks `tier == 'premium'`, and if true, an inner condition further categorizes based on `amount > 500`. This allows for complex routing logic without duplicating code.

## Flow

```mermaid
graph LR
    A[Get Data] --> B{tier == 'premium'?}
    B -->|True| C{amount > 500?}
    B -->|False| D[Standard]
    C -->|True| E[Premium High]
    C -->|False| F[Premium Low]
```

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant G as Get Data
    participant C1 as Condition 1
    participant C2 as Condition 2
    participant PH as Premium High

    P->>G: Run get_data
    G-->>P: {tier: 'premium', amount: 1000}
    P->>C1: Evaluate tier == 'premium'
    C1-->>P: True
    P->>C2: Evaluate amount > 500
    Note over C2: 1000 > 500 = True
    C2-->>P: True
    P->>PH: Run premium_high
    PH-->>P: {category: 'premium_high'}
```

```mermaid
graph TB
    subgraph Input
        A1[get_data<br/>tier: premium<br/>amount: 1000]
    end
    subgraph Outer Condition
        C1[tier == 'premium'<br/>True]
    end
    subgraph Inner Condition
        C2[amount > 500<br/>True]
    end
    subgraph Results
        R1[premium_high<br/>category: premium_high]
        R2[premium_low<br/>category: premium_low]
        R3[standard<br/>category: standard]
    end
    A1 --> C1
    C1 -->|True| C2
    C1 -->|False| R3
    C2 -->|True| R1
    C2 -->|False| R2
```

```mermaid
stateDiagram-v2
    [*] --> GetData
    GetData --> CheckTier: data received
    CheckTier --> Premium: tier == 'premium'
    CheckTier --> Standard: tier != 'premium'
    Premium --> CheckAmount: amount = 1000
    CheckAmount --> PremiumHigh: amount > 500
    CheckAmount --> PremiumLow: amount <= 500
    Standard --> [*]: {category: 'standard'}
    PremiumHigh --> [*]: {category: 'premium_high'}
    PremiumLow --> [*]: {category: 'premium_low'}
```

```mermaid
flowchart LR
    subgraph Decision Tree
        D1{tier?}
        D2{amount?}
    end
    subgraph Categories
        C1["Premium High"]
        C2["Premium Low"]
        C3["Standard"]
    end
    D1 -->|"'premium'"| D2
    D1 -->|"other"| C3
    D2 -->|"> 500"| C1
    D2 -->|"<= 500"| C2
```
