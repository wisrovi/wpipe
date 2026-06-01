#!/bin/bash
# Ejecutar tests dentro de un contenedor Docker

IMAGE_NAME="python:3.10-slim"

docker run --rm \
    -v "$(pwd)":/app \
    -w /app \
    $IMAGE_NAME \
    /bin/bash -c "
        pip install wpipe==2.4.0 wpipe-steps==0.105.0 wredis==0.9.6 psutil pytest pytest-cov && \
        # Aplicar parche para wpipe-steps
        CORE_PATH=\$(python -c 'import wpipe_steps.core as c; print(c.__path__[0])') && \
        echo 'from wpipe.decorators.step import step' > \$CORE_PATH/decorators.py && \
        echo 'from wpipe.util.transform import to_obj' >> \$CORE_PATH/decorators.py && \
        sed -i 's/@abstractmethod//g' \$CORE_PATH/base.py && \
        sed -i 's/from abc import ABC, abstractmethod/from abc import ABC/g' \$CORE_PATH/base.py && \
        # Vaciar __init__ de database para evitar errores
        DB_INIT_PATH=\$(python -c 'import wpipe_steps.database as d; print(d.__path__[0])')/__init__.py && \
        echo '' > \$DB_INIT_PATH && \
        pytest tests/
    "
