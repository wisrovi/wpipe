# Running Pipelines on a Raspberry Pi? Yes, you can. 🥧🐍

Most orchestrators crash a Raspberry Pi. WPipe loves it.

- **< 50MB RAM:** Leaving plenty of room for your actual processing.
- **SQLite Persistence:** Perfect for SD-card based systems.
- **Reliable:** Handles power cuts with automatic checkpoints.

The ultimate tool for Edge Computing and IoT.

```mermaid
graph TD
    R[Raspberry Pi] --> W[WPipe]
    W --> S1[Sensor Read]
    S1 --> C[Checkpoint]
    C --> S2[Data Upload]
```

#RaspberryPi #IoT #EdgeComputing #WPipe #Python
