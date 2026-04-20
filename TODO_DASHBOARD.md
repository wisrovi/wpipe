# TODO: Mejoras Críticas del Dashboard

## 🔴 Alta Prioridad
- **Fix: Renderizado de Grafo**: El grafo no se visualiza a pesar de que la API devuelve datos. Investigar el algoritmo de layout en `dashboard.js` y la consistencia de los IDs de los nodos.
- **Soporte de Esquema Mixto**: Asegurar que registros antiguos (sin `parent_step_id`) no rompan el cálculo de niveles en el frontend.
- **Estadísticas en Cero**: Revisar por qué el `success_rate` y `avg_duration` no se calculan correctamente incluso cuando hay datos en la BD.

## 🟡 Media Prioridad
- **Unificación de Tablas**: Estandarizar el nombre de la tabla de pasos (`steps` vs `stepmodel`) en todo el sistema para evitar migraciones manuales.
- **Feedback de Carga**: Añadir estados de carga más claros en el frontend para diagnosticar fallos de red vs fallos de renderizado.

## 🟢 Baja Prioridad
- **Auto-refresco**: Implementar WebSockets o polling para actualizar el dashboard en tiempo real sin F5.
- **Limpieza de DB**: Script para purgar registros antiguos y mantener el rendimiento de `WSQLite`.
