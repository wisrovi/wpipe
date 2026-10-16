# WPipe — WHEN TO USE (Guía del Agente)

Documento de decisión para agentes: **cuándo** usar WPipe y **cuál** feature usar.

---

## ¿Cuándo usar WPipe?

Usa **WPipe** cuando necesites:

- **Orquestar flujos de trabajo multi-paso** (ETL, MLOps, visión, integraciones) con retries, timeouts y tracking.
- **Reanudar ejecuciones tras fallos** con checkpoints (no repetir todo desde cero).
- **Composición**: `Condition`, `For`, `Parallel` (multi-proceso), `Background`, pipelines anidados.
- **PipelineAsync** para flujos asíncronos con la misma API que el síncrono.
- **Monitoreo en vivo** del pipeline (dashboard web, tracking SQLite, export a JSON/CSV).
- **Pipelines con estado tipado** (Contexts Pydantic) que fluyen entre steps clase (`@step`).

> NO uses WPipe para colas de mensajes distribuidas (usa WKafka), ni para estado
> compartido en tiempo real (usa WRedis), ni para persistencia relacional (usa WSQLite).
> WPipe es el orquestador de lógica, no el transporte de datos.

---

## Tabla de decisión: ¿cuál feature de WPipe usar?

| Necesidad | Feature | API |
|---|---|---|
| Flujo secuencial multi-paso | `Pipeline` | `Pipeline(...).set_steps([...]).run(init_data)` |
| Flujo asíncrono | `PipelineAsync` | mismo API con `await pipeline.run(...)` |
| Decisión por condición | `Condition` | `Condition(expression, branch_true, branch_false)` |
| Repetir pasos N veces | `For` | `For(iterations, steps)` |
| Ejecución concurrente | `Parallel` | `Parallel(steps, use_processes=True, merge_policy=...)` |
| Step en background | `Background` | `Background(step)` |
| Steps como función o clase | `@step` | `@step(name=..., version=..., timeout=..., retry_count=...)` |
| Contexto tipado entre steps | `@to_obj` | `@to_obj(MyPydanticContext)` sobre `__call__` |
| Timeout en steps | `timeout_sync` / `TaskTimer` | `@timeout_sync(seconds=N)`; `with TaskTimer(...)` |
| Reanudar tras fallo | `CheckpointManager` | guarda/reanuda ejecuciones |
| Tracking + métricas | `PipelineTracker` | SQLite de ejecuciones, `Metric`, `Severity` |
| RAM/CPU en vivo | `ResourceMonitor` | `with ResourceMonitor("m") as m: ...` → `m.get_summary()` |
| Export de resultados | `PipelineExporter` | logs/métricas/estadísticas → JSON/CSV |
| Dashboard en vivo | `wpipe dashboard` | CLI: `wpipe dashboard --port ...` |
| Pipelines anidados | `composition` | `NestedPipelineStep`, `PipelineAsStep` |
| Serialización robusta | `util` | `object_to_dict`, `to_obj`, `auto_dict_input` |
| Medir tiempos | `wdecorators.time_execution` | `@time_execution` |

---

## Patrón arquitectónico estándar (obligatorio)

```
dto/        Contexts Pydantic (1 archivo por contexto)
states/     Steps clase @step (1 archivo por step) — __call__ acepta el Context, lo modifica, lo retorna
main.py     Pipeline(...).set_steps([...]) → pipeline.run({...campos iniciales...})
```

Reglas:
1. **DTOs** (`dto/`) — Contexts Pydantic con tipado fuerte.
2. **Steps** (`states/`) — clases `@step`; `__call__(self, context)` retorna el contexto modificado.
3. **`tracking_db="path/to.db"`** para forensics y métricas.
4. **`ResourceMonitor` + `TaskTimer`** alrededor de la ejecución.
5. **`max_retries` + `retry_delay`** a nivel Step y Pipeline.
6. **Checkpoints** para pipelines largos que deben reanudarse.
7. **Merge determinista** en `Parallel`: `merge_policy="accumulate"` (default), `"last_wins"` o callable.

---

## Instalación

```bash
pip install wpipe
```

---

*Generado por WPipe MCP by wisrovi.*
