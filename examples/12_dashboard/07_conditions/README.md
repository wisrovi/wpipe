# Example 07: Conditional Branching

Demonstrates conditional logic with branches tracked in the dashboard.

## Conditional Flow

```mermaid
graph TD
    I[Input: temp] --> C{temp > 30?}
    C -->|TRUE| CO[Cooling On]
    C -->|FALSE| F{temp < 10?}
    F -->|TRUE| HO[Heating On]
    F -->|FALSE| NO[Normal Op]
    
    CO --> L[Log]
    HO --> L
    NO --> L
    
    C -.-> D[(Database)]
    CO -.-> D
    HO -.-> D
    NO -.-> D
```

## Branch Visualization

```mermaid
flowchart LR
    subgraph "Hot Day (temp=35)"
        N1[read_temp] --> C1{?}
        C1 -->|"✓ TRUE"| A1[cooling_on]
        C1 -->|"✗ FALSE"| A2[heating_on]
    end
    
    subgraph "Cold Day (temp=5)"
        N2[read_temp] --> C2{?}
        C2 -->|"✗ FALSE"| B1[cooling_on]
        C2 -->|"✓ TRUE"| B2[heating_on]
    end
```

## What Dashboard Shows

- ✅ Diamond nodes for conditions
- ✅ TRUE/FALSE branch indicators
- ✅ Skipped steps in gray
- ✅ Both branches listed in tooltip

## Run

```bash
cd examples/10_dashboard/07_conditions
python example.py
```
