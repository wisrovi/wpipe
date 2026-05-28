import pytest
import os
import shutil
from test_extension import pipeline

def test_pipeline_execution():
    """
    Valida que el pipeline principal se ejecute completamente sin errores.
    Este test elimina las bases de datos previas para asegurar un entorno limpio.
    """
    # Limpiar entorno
    if os.path.exists("output"):
        shutil.rmtree("output")
    os.makedirs("output")
    
    # Ejecutar pipeline
    try:
        result = pipeline.run({})
        # Si no lanza excepción, consideramos que pasó
        assert True
    except Exception as e:
        pytest.fail(f"El pipeline falló con el error: {e}")

if __name__ == "__main__":
    pytest.main([__file__])
