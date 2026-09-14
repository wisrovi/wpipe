# 171: Reddit (r/DevOps) | Celery is overkill for your side project. Use this instead.

Stop setting up Redis/RabbitMQ for simple background tasks.

**wpipe** gives you:
- <50MB RAM.
- No external broker.
- SQLite persistence.
- Auto-Mermaid diagrams.

### Battle Card
| Requirement | wpipe | Celery |
|-------------|-------|--------|
| Broker | None | Redis/Rabbit |
| Complexity | Low | High |

```mermaid
graph LR
    App --> wpipe
    wpipe --> SQLite[Local WAL]
    SQLite --> Done
```

+117k downloads and counting.

#DevOps #Python #SoftwareEngineering
