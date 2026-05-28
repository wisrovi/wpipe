#!/bin/bash
# Ejecutar tests con cálculo de cobertura
conda run -n cv pytest --cov=. --cov-report=term-missing tests/
