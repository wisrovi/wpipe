# Medium | De Frágil a A Prueba de Balas: Scraping Resiliente con wpipe

## La Fragilidad del Scraping
El scraping es inherentemente inestable: timeouts, cambios de estructura HTML, IP bloqueadas, antiguas sesiones que expiran. Un scraper sin estado pierde todo a la primera caída.

## wpipe: El Paradigma del Scraping con Checkpoints
- **Reanudación exacta**: 4 horas de crawl, se cae en la página 999 → retomas en la 999.
- **Retries inteligentes**: `retry_count` y `retry_delay` absorben los fallos transitorios.
- **Estado persistente**: SQLite WAL guarda cada resultado procesado.

```python
from wpipe import Pipeline, step

@step(name="crawl", retry_count=3, retry_delay=2)
def crawl(data):
    return {"page": data["n"], "ok": True}

pipe = Pipeline(pipeline_name="scraper", tracking_db="crawl.db")
pipe.set_steps([crawl])
pipe.run({"n": 1})
```

## Conclusión
Un scraper de producción no es un script: es un pipeline con estado. Con wpipe, tu crawler sobrevive a la realidad.

#WebScraping #Python #wpipe #DataEngineering #Reliability