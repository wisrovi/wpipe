"""
Floating-UI Generator for WPipe Learning Tour.
Features: Subtle floating 'Play' button, ultra-compact code, and specific thebe selectors.
"""

import os
import re
import subprocess
from typing import List, Optional

CERTIFICATE_LEVELS = [20, 50, 80, 110, 140]
TOTAL_LEVELS = 140

MISSION_DATA = {
    20: {"name": "Misión 1: El Despertar", "color": "#10b981", "icon": "fa-seedling"},
    50: {"name": "Misión 2: El Arquitecto", "color": "#f59e0b", "icon": "fa-drafting-pencil"},
    80: {"name": "Misión 3: El Guardián", "color": "#ef4444", "icon": "fa-shield-alt"},
    110: {"name": "Misión 4: El Maestro", "color": "#8b5cf6", "icon": "fa-magic"},
    140: {"name": "Misión 5: El Zen (Enterprise)", "color": "#00f2fe", "icon": "fa-infinity"}
}

def get_progress_html(current_level: int) -> str:
    percent = int((current_level / TOTAL_LEVELS) * 100)
    return f"""
.. raw:: html

    <div class="tour-progress-container" style="margin: 10px 0; font-size: 0.7em; color: #475569;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 2px;">
            <span>Avance: {current_level}/{TOTAL_LEVELS}</span>
            <span>{percent}%</span>
        </div>
        <div style="background: rgba(255,255,255,0.03); height: 2px; border-radius: 1px;">
            <div style="background: #00f2fe; width: {percent}%; height: 100%;"></div>
        </div>
    </div>
"""

def sort_key(filename: str) -> int:
    match = re.search(r'demo_level(\d+)\.py', filename)
    return int(match.group(1)) if match else 0

def generate() -> None:
    examples_dir = 'examples/00_honey_pot/03_yield'
    output_dir = 'docs/source/tutorials/tour'
    os.makedirs(output_dir, exist_ok=True)

    files = [f for f in os.listdir(examples_dir) if f.startswith('demo_level') and f.endswith('.py')]
    files.sort(key=sort_key)

    for filename in files:
        level_num = sort_key(filename)
        rst_path = os.path.join(output_dir, f'level{level_num}.rst')

        try:
            result = subprocess.run(['python3', filename], cwd=examples_dir, capture_output=True, text=True, timeout=5)
            output = result.stdout + result.stderr
        except:
            output = "Output captured."

        header = ""
        if os.path.exists(rst_path):
            with open(rst_path, 'r', encoding='utf-8') as f:
                header = re.split(r'(Código Fuente|Source Code)', f.read())[0].strip()

        if not header:
            header = f"Nivel {level_num}\n" + "=" * 10
        else:
            # Fix header underscores
            lines = header.splitlines()
            if len(lines) >= 2:
                lines[1] = lines[1][0] * len(lines[0])
                header = "\n".join(lines)

        content = [
            header,
            "\n.. raw:: html\n",
            "    <button class='thebe-activate'>EJECUTAR</button>\n",
            "\n.. literalinclude:: ../../../../" + f"{examples_dir}/{filename}\n"
            "   :language: python\n"
            "   :class: thebe-code\n",
            "\nResultado de Ejecución\n----------------------\n",
            ".. code-block:: text\n"
        ]
        
        for line in output.splitlines():
            content.append(f"   {re.sub(r'\\x1b\\[[0-9;]*[a-zA-Z]', '', line)}")
        
        content.append(get_progress_html(level_num))
        
        # Simple Certificates
        if level_num in CERTIFICATE_LEVELS:
            data = MISSION_DATA[level_num]
            cert_html = f"""
.. raw:: html

    <div id="cert-{level_num}" class="premium-cert" style="background: #0f172a; border: 1px solid {data['color']}; border-radius: 8px; padding: 20px; margin: 20px 0; text-align: center;">
        <h4 style="color: {data['color']}; margin: 0 0 10px 0;">{data['name']}</h4>
        <input type="text" id="name-{level_num}" placeholder="Nombre" style="background:transparent; border:none; border-bottom:1px solid {data['color']}; color:#fff; text-align:center; outline:none; margin-bottom:10px;">
        <div style="display:flex; justify-content:center; gap:10px;">
            <button onclick="window.html2canvas(document.getElementById('cert-{level_num}')).then(c=>{{const a=document.createElement('a');a.download='WPipe_L{level_num}.png';a.href=c.toDataURL();a.click();}})" style="background:{data['color']}; border:none; padding:4px 10px; border-radius:4px; font-size:0.7em; cursor:pointer;">PNG</button>
            <a href="level{level_num+1}.html" style="background:#fff; color:#000; padding:4px 10px; border-radius:4px; text-decoration:none; font-size:0.7em;">SIGUIENTE</a>
        </div>
    </div>
"""
            content.append(cert_html)

        with open(rst_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))

    print("Floating UI and Single-button logic applied.")

if __name__ == "__main__":
    generate()
