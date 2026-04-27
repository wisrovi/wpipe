Nivel 2: Metadatos y Decorador @step
====================================

.. meta::
   :description: Introducción al decorador @step para trazabilidad y versionado.
   :keywords: decorator, step, metadata, traceability, wpipe

Objetivo
--------
Aprender a enriquecer las tareas del pipeline utilizando el decorador `@step` para proporcionar nombres legibles, versionado y trazabilidad mejorada.

Conceptos Clave
---------------
* **Decorador @step**: Cómo usar metadatos para identificar tareas en el Dashboard y logs.
* **Trazabilidad**: Identificación única de versiones de cada paso.
* **Flujo de Datos II**: Cómo el diccionario de salida de un paso se inyecta como entrada en el siguiente.

¿Qué estamos probando?
----------------------
En este nivel probamos la capacidad del motor para extraer metadatos de las funciones decoradas. Validamos que el orquestador respete el nombre y la versión definidos en el decorador, y que mantenga la integridad del flujo de datos entre un paso simple y un paso decorado.

Código Fuente
------------

.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level2.py
   :language: python
   :linenos:

Análisis de la Ejecución
------------------------

Al ejecutar este código, observarás:
1. `start_engine`: Un paso simple que inicializa el contexto con `engine: ON`.
2. `check_brakes`: Un paso decorado que recibe el contexto anterior y añade la validación de frenos.
3. La barra de progreso ahora muestra los nombres configurados en lugar de los nombres técnicos de las funciones si así se prefiere.

Resultado de Ejecución
----------------------

.. code-block:: text

   🔑 Turning key: Engine started. Input data: {}
   👟 Testing pedals: Brakes verified. Input data: {'engine': 'ON', 'fuel': 100}
   Trip_L2 - Processing pipeline tasks ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00

.. raw:: html

    <div style="margin-top: 50px; padding: 30px; border: 2px dashed #4facfe; border-radius: 15px; background: rgba(79, 172, 254, 0.05); text-align: center;">
        <h3 style="color: #4facfe;">🎨 Personaliza tu Senda</h3>
        <p style="color: #94a3b8;">Estás iniciando un gran viaje. Para que tus futuros certificados sean válidos, ¿cómo debemos llamarte?</p>
        <div style="display: flex; gap: 10px; justify-content: center; margin-top: 20px; flex-wrap: wrap;">
            <input type="text" id="user-name-input" placeholder="Tu nombre completo" style="padding: 10px 15px; border-radius: 8px; border: 1px solid #334155; background: #1e293b; color: white; min-width: 250px;">
            <button onclick="saveName()" style="padding: 10px 25px; border-radius: 8px; border: none; background: #4facfe; color: #020617; font-weight: bold; cursor: pointer;">Guardar nombre</button>
        </div>
        <p id="save-status" style="margin-top: 15px; color: #10b981; display: none;">¡Nombre guardado correctamente! 🚀</p>
    </div>

    <script>
        function saveName() {
            const name = document.getElementById('user-name-input').value;
            if (name.trim()) {
                localStorage.setItem('wpipe_user_name', name);
                document.getElementById('save-status').style.display = 'block';
                setTimeout(() => {
                    document.getElementById('save-status').style.display = 'none';
                }, 3000);
            }
        }
        
        // Load existing name if any
        window.addEventListener('DOMContentLoaded', () => {
            const savedName = localStorage.getItem('wpipe_user_name');
            if (savedName) {
                document.getElementById('user-name-input').value = savedName;
            }
        });
    </script>

