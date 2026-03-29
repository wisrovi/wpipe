# Example 14: API Sending

Send pipeline results to external APIs, webhooks, and notification systems.

## API Integration Flow

```mermaid
flowchart TD
    P[Pipeline] --> E[Execute Steps]
    E --> R[Results]
    R --> W[Webhook]
    R --> S[Slack]
    R --> E2[Email]
    
    W --> API[(External APIs)]
    S --> API
    E2 --> API
```

## Sending Methods

```mermaid
classDiagram
    class APIClient {
        +str base_url
        +dict headers
        +send_post(endpoint, data)
        +send_get(endpoint)
    }
    
    class SendingMethods {
        +POST to webhook
        +GET from API
        +Slack notification
        +Email notification
    }
```

## Data Flow

```mermaid
sequenceDiagram
    participant P as Pipeline
    participant A as APIClient
    participant W as Webhook
    participant DB as SQLite
    
    P->>A: execute step
    A->>W: POST /webhook
    W-->>A: 200 OK
    A-->>P: response
    P->>DB: store result
```

## Run

```bash
cd examples/10_dashboard/14_api_sending
python example.py
```
