import pytest
import os
from test_extension import pipeline

def test_pipeline_execution():
    """
    Valida que el pipeline principal se ejecute completamente sin errores.
    """
    # Asegurar que el directorio de salida existe
    if not os.path.exists("output"):
        os.makedirs("output")
    
    # Ejecutar pipeline con datos de prueba
    try:
        # Usamos un tracking_db diferente para el test para evitar conflictos
        pipeline.tracker.db_path = "output/tracking_test.db"
        result = pipeline.run({"valor": 150})
        assert True
    except Exception as e:
        pytest.fail(f"El pipeline falló con el error: {e}")

if __name__ == "__main__":
    pytest.main([__file__])
