#!/bin/bash
# Ejecutar tests dentro de un contenedor Docker
# Nota: Se asume que las dependencias necesarias están disponibles o se pueden instalar.

IMAGE_NAME="python:3.10-slim"

docker run --rm \
    -v "$(pwd)":/app \
    -w /app \
    $IMAGE_NAME \
    /bin/bash -c "pip install wpipe pytest pytest-cov && pytest tests/"
