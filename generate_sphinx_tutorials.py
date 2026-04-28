"""
Ultimate Reliable Generator for WPipe Learning Tour.
Guaranteed no duplication, clean standard RST, and working interactivity.
"""

import os
import re
import subprocess

CERTIFICATE_LEVELS = [20, 50, 80, 110, 140]

def generate() -> None:
    examples_dir = 'examples/00_honey_pot/03_yield'
    output_dir = 'docs/source/tutorials/tour'
    
    files = sorted([f for f in os.listdir(examples_dir) if f.startswith('demo_level') and f.endswith('.py')], 
                  key=lambda x: int(re.search(r'(\d+)', x).group(1)))

    for filename in files:
        level_num = int(re.search(r'(\d+)', filename).group(1))
        rst_path = os.path.join(output_dir, f'level{level_num}.rst')

        # 1. Recuperar SOLO la cabecera original (Objetivos, etc)
        header = f"Nivel {level_num}\n" + "=" * 15
        if os.path.exists(rst_path):
            with open(rst_path, 'r', encoding='utf-8') as f:
                raw_content = f.read()
                # Cortar en cuanto aparezca CUALQUIER directiva de las que inyectamos antes
                parts = re.split(r'\.\. thebe-button|\.\. raw:: html|Código Fuente|Source Code|Resultado de Ejecución', raw_content)
                if parts:
                    header = parts[0].strip()

        # 2. Capturar output real de python
        try:
            res = subprocess.run(['python3', filename], cwd=examples_dir, capture_output=True, text=True, timeout=5)
            output = res.stdout + res.stderr
        except:
            output = "Captured output."

        # 3. Generar contenido RST LIMPIO y ESTÁNDAR
        content = [
            header,
            "\n",
            ".. thebe-button:: ACTIVAR MODO INTERACTIVO",
            "\n",
            "Código Fuente",
            "------------",
            f".. literalinclude:: ../../../../{examples_dir}/{filename}",
            "   :language: python",
            "   :class: thebe",
            "\n",
            "Resultado de Ejecución",
            "----------------------",
            ".. code-block:: text",
            "\n"
        ]
        
        # Añadir output limpio
        for line in output.splitlines():
            clean_line = re.sub(r'\\x1b\\[[0-9;]*[a-zA-Z]', '', line)
            content.append(f"   {clean_line}")

        if level_num in CERTIFICATE_LEVELS:
            content.append(f"\n.. raw:: html\n\n    <div style='border:1px solid #00f2fe;padding:15px;text-align:center;border-radius:8px;margin-top:20px;'><h3>Misión {level_num//20} Superada</h3><a href='level{level_num+1}.html' style='color:#00f2fe;'>Siguiente Nivel</a></div>")

        # 4. SOBREESCRIBIR COMPLETAMENTE
        with open(rst_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))

    print(f"Successfully generated {len(files)} clean levels.")

if __name__ == "__main__":
    generate()
