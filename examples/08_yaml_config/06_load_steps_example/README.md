# Loading Pipeline Steps from YAML

Shows how to load pipeline step definitions from a YAML configuration file.

## What It Does

This example demonstrates:
- Defining pipeline steps in YAML
- Loading step configurations dynamically
- Mapping function names to actual functions
- Building pipelines from loaded configurations

## Example

```python
from wpipe import Pipeline
from wpipe.util import leer_yaml

config = leer_yaml("steps.yaml")
for step_config in config["steps"]:
    func = functions[step_config["function"]]
    steps.append((func, step_config["name"], step_config["version"]))
```

## Config Flow

```mermaid
graph LR
    A[Steps YAML] --> B[Load Config]
    B --> C[Extract Steps]
    C --> D[Map Functions]
    D --> E[Build Pipeline]
    E --> F[Execute]
```

## Step Loading Sequence

```mermaid
sequenceDiagram
    participant User
    participant YAML as Steps YAML
    participant Config as Loaded Config
    participant Functions as Function Map
    participant Pipeline as Pipeline
    
    User->>YAML: Load steps.yaml
    User->>Config: Read config["steps"]
    loop For each step
        Config->>Functions: Lookup function name
        Functions-->>Config: Return function
        Config->>Config: Create tuple
    end
    User->>Pipeline: set_steps(loaded_steps)
    User->>Pipeline: run({})
```

## Config Structure

```mermaid
graph TB
    subgraph YAML Config
        A[steps]
    end
    subgraph Step Entries
        B[Step 1]
        C[Step 2]
    end
    subgraph Step Properties
        D[name]
        E[function]
        F[version]
    end
    A --> B
    A --> C
    B --> D
    B --> E
    B --> F
    C --> D
    C --> E
    C --> F
```

## Loading States

```mermaid
stateDiagram-v2
    [*] --> LoadYAML
    LoadYAML --> ParseSteps: Parse config
    ParseSteps --> MapFunctions: For each step
    MapFunctions --> Validate: Function exists?
    Validate --> Valid: Yes
    Validate --> Invalid: No
    Valid --> BuildList: Add to steps list
    BuildList --> MoreSteps: More steps?
    MoreSteps --> MapFunctions: Yes
    MoreSteps --> Done: No
    Done --> [*]
```

## Process Flow

```mermaid
flowchart LR
    A[Define Steps<br/>in YAML] --> B[Write YAML File]
    B --> C[Load Config]
    C --> D[Iterate Steps]
    D --> E[Lookup Function]
    E --> F[Create Tuple]
    F --> G[set_steps]
    G --> H[Run Pipeline]
```
