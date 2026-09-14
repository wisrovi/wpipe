# Medium | Trazabilidad Forense: El Historial que tus Pipelines Necesitan

## No basta con "Funciona"
Para auditarías, comparativas de rendimiento o simplemente para explicar qué pasó, necesitas un historial completo: quién, qué, cuándo y por qué.

## wpipe: Tracking de Grado Industrial
Cada ejecución de wpipe queda registrada en un **tracker SQL** consultable.

- **Quién**: qué pipeline corrió.
- **Qué**: qué pasos se ejecutaron y con qué datos.
- **Cuándo**: línea de tiempo de cada transformación.
- **Por qué**: contexto completo del fallo, si ocurrió.

```python
from wpipe import PipelineExporter

exporter = PipelineExporter("tracking.db")
logs = exporter.export_pipeline_logs(format="json")
stats = exporter.export_statistics(format="json")
```

## Conclusión
La trazabilidad forense separa a los sistemas de juguete de los de producción. Con wpipe, la tienes desde el primer run.

#Observability #wpipe #Python #DataEngineering #Audit