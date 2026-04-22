import os
import re
import subprocess

def sort_key(filename):
    # Extract the number from demo_levelX.py
    match = re.search(r'demo_level(\d+)\.py', filename)
    if match:
        return int(match.group(1))
    return 0

def generate():
    examples_dir = 'examples/00_honey_pot/03_yield'
    output_dir = 'docs/source/tutorials/tour'
    os.makedirs(output_dir, exist_ok=True)

    files = [f for f in os.listdir(examples_dir) if f.startswith('demo_level') and f.endswith('.py')]
    files.sort(key=sort_key)

    index_content = """Tour de Aprendizaje (130 Niveles)
=================================

Bienvenido al Tour de Aprendizaje de WPipe. Este recorrido guiado te llevará desde los conceptos más básicos hasta las orquestaciones más complejas a través de 130 niveles prácticos.

.. toctree::
   :maxdepth: 1
   :numbered:

"""

    for i, filename in enumerate(files):
        level_num = sort_key(filename)
        rst_filename = f'level{level_num}.rst'
        
        # Capture output
        print(f"Ejecutando {filename} para capturar salida...")
        try:
            result = subprocess.run(['python3', filename], cwd=examples_dir, capture_output=True, text=True, timeout=30)
            output = result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            output = "Error: Timeout al ejecutar el ejemplo."
        except Exception as e:
            output = f"Error al ejecutar el ejemplo: {str(e)}"

        # Create individual rst for each level
        with open(os.path.join(output_dir, rst_filename), 'w') as f:
            title = f"Nivel {level_num}: {filename}"
            f.write(f"{title}\n" + "=" * len(title) + "\n\n")
            f.write(f"Este es el nivel {level_num} del tour de aprendizaje.\n\n")
            
            f.write("Código Fuente\n------------\n\n")
            f.write(f".. literalinclude:: ../../../../{examples_dir}/{filename}\n")
            f.write("   :language: python\n")
            f.write("   :linenos:\n\n")
            
            f.write("Resultado de Ejecución\n----------------------\n\n")
            f.write(".. code-block:: text\n\n")
            for line in output.splitlines():
                f.write(f"   {line}\n")
            f.write("\n")

        index_content += f"   {rst_filename[:-4]}\n"

    with open(os.path.join(output_dir, 'index.rst'), 'w') as f:
        f.write(index_content)

    print(f"Generados {len(files)} niveles con resultados en {output_dir}")

if __name__ == "__main__":
    generate()
