# wpipe

La clase `Pipeline` es una herramienta que facilita la ejecución de un pipeline de tareas y la interacción con una API externa. La librería proporciona la capacidad de registrar workers, procesos y tareas, permitiendo reportar el estado de cada paso en tiempo real.



## Descripción

La clase Pipeline permite gestionar y ejecutar un pipeline de tareas con integración a una API externa. El objetivo de esta librería es facilitar la ejecución ordenada de varias funciones (tareas) que componen un pipeline, reportando su progreso y estado a un servidor externo. Entre sus principales características se encuentran:

    Registro de workers (trabajadores) y procesos.
    Ejecución y monitoreo de tareas.
    Decoradores para reportar automáticamente el estado de cada tarea.
    Integración con una API para seguimiento de procesos.
    Manejo de errores durante la ejecución del pipeline.

Esta librería es útil cuando se tiene un conjunto de pasos que deben ejecutarse en secuencia, y se quiere tener un control y reporte detallado sobre cada uno de estos pasos.
## Instalación

Puedes instalar la librería mediante pip, siempre que se haya registrado en PyPI:

```python
pip install wpipe
```

tambien puedes desde la fuente


```sh
git clone https://github.com/wisrovi/wpipe
cd wpipe
pip install .
```

Esto instalará las dependencias necesarias y permitirá que puedas importar Pipeline en tu proyecto.


## Configuración

La librería Pipeline puede ser utilizada de dos maneras:

- 1. Localmente, sin enviar datos a una API externa.
- 2. Con un servicio de API, usando un contenedor Docker para registrar y reportar los procesos y tareas ejecutados por el pipeline.





A continuación, se detallan ejemplos de configuración para cada caso:

### 1. Uso local (sin API)

En este modo, puedes usar la clase Pipeline sin necesidad de conectarte a un servidor externo o API. No se requiere un api_config en el constructor, y todos los procesos se ejecutan de forma local.

```python
from wpipe.pipe import Pipeline

# Crear el pipeline sin pasar configuración de API (modo local)
pipeline = Pipeline()

# Definir pasos del pipeline
def step1(data: dict):
    return {"resultado1": "Paso 1 completado"}

def step2(data: dict):
    return {"resultado2": "Paso 2 completado"}

class Demo:
    def __call__(self, data: dict):
        return {"resultado3": "Paso 3 completado"}

pipeline.set_steps([
    (step1, "Paso 1", "v1.0"),
    (step2, "Paso 2", "v1.0"),
    (Demo(), "Paso 3", "v1.0"),
])

# Ejecutar el pipeline con los datos de entrada
input_data = {"input": "datos_iniciales"}
resultado = pipeline.run(input_data)
print("Resultado final:", resultado)
```

### 2. Uso con servicio de API (Docker)

En esta modalidad, la librería se conectará a un servidor API externo para reportar el estado de las tareas y los procesos del pipeline. Para usar este modo, debes tener un contenedor Docker con el servicio de API corriendo.

Pasos para configurar el servicio de API con Docker:

- Clona el repositorio de la API desde GitHub:

```sh 
git clone https://github.com/wisrovi/wpipe-api
```

- Construye y ejecuta el contenedor Docker:

```sh 
cd wpipe-api
docker-compose up -d
```

Este comando levantará el backend en http://localhost:8418
 y el dashboard en http://localhost:8050


```sh 
    También crea una base de datos con la siguiente estructura:

    worker_1
    |____Process_1
    |         |_____Task1 (step)
    |         |_____Task2 (step)
    |         |_____Task3 (step)
    |____Process_2
    |          ...
    worker_2
    |    ...
```

   1. Los worker identifican al script en si (con un id de registro en DB en la api), es un autoregistro con:
```python 
worker_id = pipeline.worker_register(name=NAME, version=VERSION)
```

   - La idea es que este id se almacene en disco y se actualice cuando cambie la version del script.
   - Seguidamente en las siguientes ejecuciones se lea este id almacenado








2. Los Process se crean con cada ejecucion de un `run`
```python 
resultado = pipeline.run(input_data)  # input_data = dict  # son datos en un dict
```
   - Pueden haber varios procesos ejecutados para el `Pipeline` de esta manera se podrá contabilizar cuantas veces se ha ejecutado el script, cuantas veces sin fallos, cuantas con fallos, tiempo promedio de ejecucion, entre otras




3. Los Tasks con los `steps` del pipeline, esto:
   - Muestra en que proceso o avance va la ejecución
   - El tiempo de ejecucion de cada step, etc
   - el registro de esto esta automatizado en el uso del `run`


Un ejemplo es:

```python
from wpipe.pipe import Pipeline


NAME = "microservicio_1
VERSION = "v1.0

# Configuración de la API externa
api_config = {
    "base_url": "http://localhost:8418",  # URL del servicio API
    "token": "mysecrettoken",     # Token de autenticación, debe ser el mismo con la API
}

# Crear el pipeline con configuración de API (modo conectado a API)
pipeline = Pipeline(api_config=api_config)

# Definir pasos del pipeline
def step1(data):
    return {"resultado1": "Paso 1 completado"}

def step2(data):
    return {"resultado2": "Paso 2 completado"}

class Demo:
    def __call__(self, data: dict):
        return {"resultado3": "Paso 3 completado"}

pipeline.set_steps([
    (step1, "Paso 1", "v1.0"),
    (step2, "Paso 2", "v1.0"),
    (Demo(), "Paso 3", "v1.0"),
])


# es necesario registrar el proceso como un worker
worker_id = pipeline.worker_register(name=NAME, version=VERSION) # el registro solo se puede hacer despues de 'set_steps'
pipeline.set_worker_id(worker_id)
# aunque el worker_id (string) en este codigo no se guarda, se recomienda guardarlo en un archivo para no registrarlo en cada inicio sino aprovechar el id, dado que este identifica al script


# ************************************************
#          opcional pero recomendado
# ************************************************
import threading
import time
stop_event = threading.Event()  # por default es False
def worker_healthchecker():
    stop = False
    while not stop:
        pipeline.healthcheck_worker(worker_id)

        for _ in range(20):
            stop = stop_event.is_set()
            time.sleep(1)

healthchecker_thread = threading.Thread(target=worker_healthchecker)
healthchecker_thread.start()
# ************************************************


def worker(input_data: dict = {}):
    # Ejecutar el pipeline con los datos de entrada
    resultado = pipeline.run(input_data)
    # esto crea un nuevo proceso atado al worker

    print("Resultado final:", resultado)

    # se detiene el 'healthcheck'
    stop_event.set()  # pongo el evento en True [Solo si uso el healthchecker]


worker(input_data={"input": "datos_iniciales"})

healthchecker_thread.join()  # [Solo si uso el healthchecker]
```



## Uso

Una vez que tienes configurado tu Pipeline, necesitas definir los pasos que este ejecutará. Cada paso del pipeline se define como una tupla que contiene:

1. Una función que ejecutará la tarea.
2. Un nombre en formato de string para identificar la tarea.
3. La versión de la tarea.



Ejemplo de definición de pasos:

```python
# funciones cuyos datos de entrada y return sean un dict
def step1(data):
    return {"resultado1": "Paso 1 completado"}

# clases cuyo __call__ tenga de entrada y return un dict
class Demo: # puede tener o no herencia a otra clase

    # puede tener un constructor
    def __init__(self, a:int):
        self.a = a

    def __call__(self, data: dict):
        return {"resultado2": f"Paso {self.a} completado"}

pipeline.set_steps([
    (step1, "Paso 1", "v1.0"),
    (Demo(a=2), "Paso 2", "v1.0"),
])
```

Ejemplo de ejecución:

Una vez definidos los pasos, puedes ejecutar el pipeline llamando al método run:
```python
input_data = {"input": "datos_iniciales"}
resultado = pipeline.run(input_data)
print("Resultado final:", resultado)
```

El pipeline pasará los datos de salida de cada paso como entrada al siguiente, y reportará el estado de cada tarea.

Los datos se iran acumulando durante la ejecución, pudiendo los steps siguientes ver todos los return de los steps anteriores
## Ejemplos

### Ejemplo 1: Ejecución local básica (sin conexión a API)

Este ejemplo muestra cómo usar la clase Pipeline en modo local, sin necesidad de conectarse a una API externa. El pipeline ejecuta dos tareas sencillas.

```python
from wpipe.pipe import Pipeline

# Definir las funciones del pipeline
def tarea1(data):
    print("Ejecutando tarea 1...")
    return {"resultado1": "Tarea 1 completada"}

def tarea2(data):
    print("Ejecutando tarea 2...")
    return {"resultado2": "Tarea 2 completada"}

# Crear pipeline sin conexión a API
pipeline = Pipeline(verbose=True)

# Establecer las tareas (función, nombre, versión)
pipeline.set_steps([
    (tarea1, "Tarea 1", "v1.0"),
    (tarea2, "Tarea 2", "v1.0"),
])

# Ejecutar el pipeline
input_data = {"dato_inicial": "valor"}
resultado = pipeline.run(input_data)

print("Resultado final:", resultado)
```

### Ejemplo 2: Uso con API externa para registrar el estado de las tareas

En este caso, el pipeline se conecta a una API externa utilizando un contenedor Docker, y reporta el estado de cada tarea a la API.

```python
from wpipe.pipe import Pipeline

# Definir las funciones del pipeline
def tarea1(data):
    return {"resultado1": "Tarea 1 completada"}

def tarea2(data):
    return {"resultado2": "Tarea 2 completada"}


# Configuración para conectar con la API externa
api_config = {
    "base_url": "http://localhost:8418",  # URL del servicio API
    "token": "mysecrettoken",     # Token de autenticación, debe ser el mismo con la API
}

# Crear pipeline conectado a la API
pipeline = Pipeline(api_config)



# Establecer las tareas
pipeline.set_steps([
    (tarea1, "Tarea 1", "v1.0"),
    (tarea2, "Tarea 2", "v1.0"),
])



# se debe registrar para obtener el worker_id, si ya se tiene uno se omite el registro
worker_id = pipeline.worker_register(name=NAME, version=VERSION) # el registro solo se puede hacer despues de 'set_steps'

# se configura el worker_id a usar
pipeline.set_worker_id(worker_id)



# Ejecutar el pipeline
input_data = {"dato_inicial": "valor"}
resultado = pipeline.run(input_data)

print("Resultado final reportado a la API:", resultado)
```






### Ejemplo 3: Pipeline con manejo de errores en las tareas

Este ejemplo incluye una tarea que falla para mostrar cómo el pipeline maneja los errores y detiene la ejecución.

```python
from wpipe.pipe import Pipeline

# Definir las funciones del pipeline
def tarea1(data):
    print("Ejecutando tarea 1...")
    return {"resultado1": "Tarea 1 completada"}

def tarea_falla(data):
    print("Ejecutando tarea con error...")
    raise Exception("Error en la tarea")

# Crear pipeline en modo local
pipeline = Pipeline(verbose=True)

# Establecer las tareas
pipeline.set_steps([
    (tarea1, "Tarea 1", "v1.0"),
    (tarea_falla, "Tarea con error", "v1.0"),
])

# Ejecutar el pipeline
try:
    input_data = {"dato_inicial": "valor"}
    resultado = pipeline.run(input_data)
    print("Resultado final:", resultado)
except Exception as e:
    print(f"Pipeline fallido: {str(e)}")
```













### Ejemplo 4: Reutilización del pipeline con diferentes funciones


Este ejemplo muestra cómo reutilizar el mismo pipeline con diferentes conjuntos de funciones (tareas).

```python
from wpipe.pipe import Pipeline

# Definir funciones para dos pipelines diferentes
def tareaA(data):
    return {"resultadoA": "Tarea A completada"}

def tareaB(data):
    return {"resultadoB": "Tarea B completada"}

def tareaX(data):
    return {"resultadoX": "Tarea X completada"}

def tareaY(data):
    return {"resultadoY": "Tarea Y completada"}

# Crear pipeline en modo local
pipeline = Pipeline(verbose=True)

# Primer conjunto de tareas
pipeline.set_steps([
    (tareaA, "Tarea A", "v1.0"),
    (tareaB, "Tarea B", "v1.0"),
])

# Ejecutar el primer pipeline
input_data1 = {"dato_inicial": "valor1"}
resultado1 = pipeline.run(input_data1)
print("Resultado pipeline 1:", resultado1)

# Segundo conjunto de tareas
pipeline.set_steps([
    (tareaX, "Tarea X", "v1.0"),
    (tareaY, "Tarea Y", "v1.0"),
])

# Ejecutar el segundo pipeline
input_data2 = {"dato_inicial": "valor2"}
resultado2 = pipeline.run(input_data2)
print("Resultado pipeline 2:", resultado2)
```


















### Ejemplo 5: Uso avanzado del pipeline con conexión a API y varias versiones de tareas

Este ejemplo muestra cómo se puede ejecutar un pipeline con diferentes versiones de las mismas tareas y reportar a la API.






```python
from wpipe.pipe import Pipeline

# Definir las funciones del pipeline
def tarea1_v1(data):
    return {"resultado1": "Tarea 1 completada (v1.0)"}

def tarea1_v2(data):
    return {"resultado1": "Tarea 1 completada (v2.0)"}

def tarea2(data):
    return {"resultado2": "Tarea 2 completada"}

# Configuración de la API externa
api_config = {
    "base_url": "http://localhost:8000/api",  # URL de la API
    "token": "mi_token_de_autenticacion",
}

# Crear pipeline conectado a la API
pipeline = Pipeline(worker_id="worker_67890", api_config=api_config, verbose=True)

# Definir tareas con versiones diferentes
pipeline.set_steps([
    (tarea1_v1, "Tarea 1", "v1.0"),
    (tarea1_v2, "Tarea 1", "v2.0"),
    (tarea2, "Tarea 2", "v1.0"),
])

# Ejecutar el pipeline
input_data = {"dato_inicial": "valor"}
resultado = pipeline.run(input_data)

print("Resultado final reportado a la API:", resultado)
```




### Ejemplo 6: Uso del pipeline con funciones asincrónicas

Este ejemplo muestra cómo usar tareas asincrónicas en el pipeline.


```python
from wpipe.pipe import Pipeline
import asyncio

# Definir funciones asincrónicas
async def tarea1_async(data):
    await asyncio.sleep(1)
    return {"resultado1": "Tarea 1 completada (async)"}

async def tarea2_async(data):
    await asyncio.sleep(1)
    return {"resultado2": "Tarea 2 completada (async)"}

# Crear pipeline en modo local
pipeline = Pipeline(verbose=True)

# Establecer las tareas
pipeline.set_steps([
    (tarea1_async, "Tarea 1 (async)", "v1.0"),
    (tarea2_async, "Tarea 2 (async)", "v1.0"),
])

# Ejecutar el pipeline en un loop de asyncio
async def run_pipeline():
    input_data = {"dato_inicial": "valor"}
    resultado = await pipeline.run(input_data)
    print("Resultado final (async):", resultado)

asyncio.run(run_pipeline())
```


### Ejemplo 7: Pipeline con tareas dependientes del resultado anterior

Este ejemplo ilustra cómo una tarea puede depender del resultado de la tarea anterior.


```python
from wpipe.pipe import Pipeline

# Definir las funciones del pipeline
def tarea1(data):
    print("Ejecutando tarea 1...")
    return {"valor_intermedio": 10}

def tarea2(data):
    valor = data.get("valor_intermedio", 0)
    return {"resultado2": f"Tarea 2 completada, multiplicando: {valor * 2}"}

# Crear pipeline en modo local
pipeline = Pipeline(verbose=True)

# Establecer las tareas
pipeline.set_steps([
    (tarea1, "Tarea 1", "v1.0"),
    (tarea2, "Tarea 2", "v1.0"),
])

# Ejecutar el pipeline
input_data = {"dato_inicial": "valor"}
resultado = pipeline.run(input_data)

print("Resultado final:", resultado)
```


### Ejemplo 8: Uso de pipeline para tareas de limpieza y procesamiento de datos

Este ejemplo ilustra un pipeline usado para una cadena de procesamiento de datos.


```python
from wpipe.pipe import Pipeline

# Definir funciones para procesar datos
def limpiar_datos(data):
    datos_limpios = data["raw_data"].strip()
    return {"datos_limpios": datos_limpios}

def procesar_datos(data):
    datos_procesados = data["datos_limpios"].upper()
    return {"datos_procesados": datos_procesados}

# Crear pipeline en modo local
pipeline = Pipeline(verbose=True)

# Establecer las tareas
pipeline.set_steps([
    (limpiar_datos, "Limpiar Datos", "v1.0"),
    (procesar_datos, "Procesar Datos", "v1.0"),
])

# Ejecutar el pipeline
input_data = {"raw_data": "   datos en crudo   "}
resultado = pipeline.run(input_data)

print("Resultado final:", resultado)
```



### Ejemplo 9: Pipeline con logs personalizados

Este ejemplo muestra cómo agregar un sistema de logging personalizado dentro del pipeline.


```python
from wpipe.pipe import Pipeline
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Definir funciones con logs
def tarea1(data):
    logging.info("Ejecutando tarea 1...")
    return {"resultado1": "Tarea 1 completada"}

def tarea2(data):
    logging.info("Ejecutando tarea 2...")
    return {"resultado2": "Tarea 2 completada"}

# Crear pipeline en modo local
pipeline = Pipeline(verbose=True)

# Establecer las tareas
pipeline.set_steps([
    (tarea1, "Tarea 1", "v1.0"),
    (tarea2, "Tarea 2", "v1.0"),
])

# Ejecutar el pipeline
input_data = {"dato_inicial": "valor"}
resultado = pipeline.run(input_data)

logging.info(f"Resultado final: {resultado}")
```



### Ejemplo 10: Pipeline con validación de entrada

Este ejemplo valida los datos de entrada antes de ejecutar las tareas.

```python
from wpipe.pipe import Pipeline

# Definir funciones del pipeline
def validar_entrada(data):
    if "dato_inicial" not in data:
        raise ValueError("Falta 'dato_inicial' en los datos de entrada")
    return data

def tarea1(data):
    return {"resultado1": "Tarea 1 completada"}

# Crear pipeline en modo local
pipeline = Pipeline(verbose=True)

# Establecer las tareas
pipeline.set_steps([
    (validar_entrada, "Validación de Entrada", "v1.0"),
    (tarea1, "Tarea 1", "v1.0"),
])

# Ejecutar el pipeline
input_data = {"dato_inicial": "valor"}
resultado = pipeline.run(input_data)

print("Resultado final:", resultado)
```



## Manejo de Errores

La clase Pipeline tiene una gestión robusta de errores durante la ejecución. Si una tarea genera una excepción, el pipeline captura ese error y lo registra en la API (si está configurada). Además:

   - Si una tarea falla, el pipeline se detiene inmediatamente, registrando el motivo del error en la API.
   - El error se añade al resultado final de la tarea fallida, permitiendo que puedas gestionar la falla.

Ejemplo de manejo de error:

Si una tarea falla, la excepción se mostrará en el log y se enviará a la API:


```python
def step_fails(data):
    raise Exception("Error en la tarea")

pipeline.set_steps([
    (step_fails, "Tarea fallida", "v1.0"),
])

try:
    resultado = pipeline.run({"input": "datos_iniciales"})
except Exception as e:
    print(f"Pipeline fallido: {str(e)}")
```






## Requisitos

Para que la librería funcione correctamente, necesitas las siguientes dependencias, que se instalan automáticamente cuando instalas el paquete:

    - requests: Para hacer peticiones HTTP a la API externa.
    - loguru: Para gestionar los logs.
    - pandas: Para el manejo de datos en formato tabular.
    - pyyaml: Para la manipulación de archivos en formato YAML.





## Contribuyendo

1. Haz un fork del proyecto.
2. Crea una rama con tu nueva funcionalidad: git checkout -b mi-nueva-funcionalidad.
3. Haz commit de tus cambios: git commit -m 'Agregar nueva funcionalidad'.
4. Haz push de la rama: git push origin mi-nueva-funcionalidad.
5. Crea un Pull Request.





## Licencia

Este proyecto está bajo la licencia MIT, lo que significa que puedes usarlo, modificarlo y distribuirlo libremente, siempre que mantengas la atribución al autor original. Ver el archivo LICENSE para más detalles.


[MIT](https://choosealicense.com/licenses/mit/)