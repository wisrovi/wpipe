Nivel 50: Integración Final - El Viaje Completo
===============================================

.. meta::
   :description: Integración de todas las funcionalidades de WPipe en un único flujo complejo.
   :keywords: integration, complex, parallel, for-loop, checkpoints, alerts, wpipe

Objetivo
--------
Consolidar todos los conocimientos adquiridos en los primeros 50 niveles. Crearemos un pipeline de "Viaje en Coche" que utiliza paralelismo, bucles, condiciones, alertas de rendimiento, manejo de errores forense y exportación de datos.

Conceptos Clave
---------------
* **Orquestación Compleja**: Combinación de `Parallel`, `For` y `Condition` en una estructura jerárquica.
* **Alertas de Rendimiento**: Uso de `add_alert_threshold` para detectar cuellos de botella en tiempo real.
* **Resiliencia Extrema**: Captura de errores con notificaciones personalizadas (simulación de Telegram).
* **Observabilidad**: Monitoreo de recursos del sistema (CPU/RAM) y exportación a JSON/CSV.

¿Qué estamos probando?
----------------------
Este nivel es la prueba de fuego para el motor. Validamos:
1. La capacidad de manejar **objetos no serializables** en el contexto sin romper la persistencia.
2. La ejecución de tareas en paralelo mientras se mantiene el registro de logs thread-safe.
3. La activación de **checkpoints inteligentes** basados en expresiones lógicas.
4. La recuperación automática mediante reintentos en pasos específicos (`random_flat_tire`).


.. thebe-button:: ACTIVAR MODO INTERACTIVO


Código Fuente
------------
.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level50.py
   :language: python
   :class: thebe


Resultado de Ejecución
----------------------
.. code-block:: text


   Captured output.

.. raw:: html

    <div class="certificate-zone" style="margin-top: 60px; border-top: 2px solid #f59e0b; padding: 40px; background: rgba(255,255,255,0.02); border-radius: 15px;">
        <div style="text-align: center; margin-bottom: 40px;">
            <h2 style="color: #f59e0b; margin-bottom: 10px;">¡RECLAMA TU LOGRO!</h2>
            <p style="color: #94a3b8;">Introduce tu nombre para desbloquear tu certificado oficial.</p>
            <input type="text" id="cert-name-input" placeholder="ESCRIBE TU NOMBRE COMPLETO AQUÍ" 
                   style="background: #0f172a; border: 2px solid #334155; color: white; padding: 15px 25px; border-radius: 12px; margin-top: 15px; width: 80%; max-width: 500px; text-align: center; font-size: 1.2em; font-weight: bold; outline: none; border-color: #f59e0b; box-shadow: 0 0 20px rgba(0,0,0,0.5);">
        </div>

        <div id="cert-container-50" style="width: 1000px; height: 700px; margin: 0 auto; border-radius: 25px; padding: 60px; color: white; position: relative; box-sizing: border-box; overflow: hidden; text-align: center; background: linear-gradient(135deg, #020617 0%, #78350f 100%); border: 15px solid #f59e0b; box-shadow: 0 40px 80px rgba(0,0,0,0.9);">
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; opacity: 0.15; background-image: radial-gradient(#ffffff 1px, transparent 1px); background-size: 35px 30px;"></div>
            <div style="position: relative; z-index: 1; height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h1 style="color: #f59e0b; margin: 0; font-size: 3.2em; text-transform: uppercase; font-weight: 900; letter-spacing: 3px; text-shadow: 0 5px 15px rgba(0,0,0,0.5);">Certificado de Misión</h1>
                    <p style="font-size: 1.3em; margin-top: 10px; opacity: 0.8; letter-spacing: 1px;">WPipe Engine Certification • Misión 2</p>
                </div>
                
                <div style="margin: 10px 0;">
                    <p style="font-size: 1.4em; margin-bottom: 5px; color: #94a3b8;">Se otorga con honor a:</p>
                    <h2 class="cert-name-display" style="font-size: 4.2em; border-bottom: 4px solid #f59e0b; min-width: 500px; display: inline-block; font-family: 'Times New Roman', serif; text-shadow: 0 0 20px rgba(255,255,255,0.3); margin: 10px 0; color: #fff;">---</h2>
                </div>

                <div style="margin-bottom: 10px;">
                    <p style="font-size: 1.5em; color: #fff; margin-bottom: 5px; opacity: 0.9;">Con el rango oficial de:</p>
                    <h3 style="color: #f59e0b; font-size: 2.8em; margin: 0; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; text-shadow: 0 0 10px #f59e0b44;">Arquitecto WPipe Bronze</h3>
                </div>

                <div style="display: flex; justify-content: space-between; align-items: flex-end; padding: 25px; border-top: 2px solid #f59e0b44; background: rgba(0,0,0,0.3); border-radius: 15px;">
                    <div style="text-align: left; opacity: 1; font-family: 'Courier New', monospace; line-height: 1.7;">
                        <p style="margin: 0; color: #f59e0b; font-weight: bold; font-size: 1.1em; letter-spacing: 1px;">EMITIDO EL: <span class="cert-date-display" style="color: #fff;">--/--/----</span></p>
                        <p style="margin: 0; color: #64748b; font-size: 0.8em; margin-bottom: 12px;">ID: WP-50-ARQ-ONZE</p>
                        <div style="background: #f59e0b; color: #020617; padding: 8px 20px; border-radius: 8px; display: inline-block; font-weight: 900; font-size: 1.1em; letter-spacing: 0.5px; box-shadow: 0 4px 15px rgba(0,0,0,0.4);">
                            WPIPE.WISROVI.DEV • WISROVI SUITE
                        </div>
                        <p style="margin: 0; margin-top: 8px; font-size: 0.85em; color: #94a3b8; font-weight: bold;">Explore the full suite at WISROVI.DEV</p>
                    </div>
                    <div style="width: 120px; height: 120px; background: #f59e0b; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 4.5em; box-shadow: 0 0 50px #f59e0b88; border: 5px solid rgba(255,255,255,0.1);">📐</div>
                </div>
            </div>
        </div>

        <div style="text-align: center; margin-top: 40px; display: flex; justify-content: center; gap: 20px;">
            <button id="btn-download" onclick="downloadCert(50)" disabled 
                    style="background: #475569; color: #94a3b8; padding: 12px 35px; border-radius: 12px; font-weight: bold; cursor: not-allowed; border: none; transition: all 0.3s; font-size: 1em;">⬇️ DESCARGAR PNG</button>
            <button id="btn-share" onclick="shareLinkedIn(50)" disabled 
                    style="background: #475569; color: #94a3b8; padding: 12px 35px; border-radius: 12px; font-weight: bold; cursor: not-allowed; border: none; transition: all 0.3s; font-size: 1em;">🔗 COMPARTIR LOGRO</button>
            <a href="level51.html" style="background: #f59e0b; color: #020617; padding: 12px 35px; border-radius: 12px; font-weight: bold; text-decoration: none; display: flex; align-items: center; font-size: 1em;">CONTINUAR ➡️</a>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const nameInput = document.getElementById('cert-name-input');
            const nameDisplays = document.querySelectorAll('.cert-name-display');
            const btnDownload = document.getElementById('btn-download');
            const btnShare = document.getElementById('btn-share');
            const dateDisplays = document.querySelectorAll('.cert-date-display');
            
            // Inyectar fecha actual inmediatamente
            const now = new Date();
            const dateStr = now.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric' });
            dateDisplays.forEach(el => el.innerText = dateStr);
            
            const updateUI = (val) => {
                const cleanVal = val.trim();
                if (cleanVal.length >= 3) {
                    nameDisplays.forEach(el => el.innerText = cleanVal);
                    btnDownload.disabled = false;
                    btnDownload.style.background = 'white';
                    btnDownload.style.color = '#020617';
                    btnDownload.style.cursor = 'pointer';
                    btnDownload.style.boxShadow = '0 5px 15px rgba(255,255,255,0.2)';
                    btnShare.disabled = false;
                    btnShare.style.background = '#0077b5';
                    btnShare.style.color = 'white';
                    btnShare.style.cursor = 'pointer';
                    btnShare.style.boxShadow = '0 5px 15px rgba(0,119,181,0.3)';
                } else {
                    nameDisplays.forEach(el => el.innerText = '---');
                    btnDownload.disabled = true;
                    btnDownload.style.background = '#475569';
                    btnDownload.style.color = '#94a3b8';
                    btnDownload.style.cursor = 'not-allowed';
                    btnDownload.style.boxShadow = 'none';
                    btnShare.disabled = true;
                    btnShare.style.background = '#475569';
                    btnShare.style.color = '#94a3b8';
                    btnShare.style.cursor = 'not-allowed';
                    btnShare.style.boxShadow = 'none';
                }
            };

            // Recuperar persistencia
            const savedName = localStorage.getItem('wpipe_student_name');
            if (savedName) {
                nameInput.value = savedName;
                updateUI(savedName);
            }

            nameInput.addEventListener('input', (e) => {
                const val = e.target.value;
                localStorage.setItem('wpipe_student_name', val);
                updateUI(val);
            });
        });

        function downloadCert(level) {
            const element = document.getElementById('cert-container-' + level);
            html2canvas(element, { 
                scale: 3, 
                backgroundColor: '#0f172a',
                logging: false,
                useCORS: true
            }).then(canvas => {
                const link = document.createElement('a');
                link.download = 'WPipe_Certification_L' + level + '.png';
                link.href = canvas.toDataURL('image/png');
                link.click();
            });
        }

        function shareLinkedIn(level) {
            const rank = "Arquitecto WPipe Bronze";
            const text = `🚀 ¡Certificación alcanzada! Acabo de obtener mi rango de ${rank} en el WPipe Learning Tour. Agradezco a @wisrovi por crear este potente motor de orquestación industrial. #wpipe #python #dataengineering #backend #wisrovidev`;
            
            downloadCert(level);
            navigator.clipboard.writeText(text);
            const linkedInUrl = `https://www.linkedin.com/feed/?shareActive=true&text=${encodeURIComponent(text)}`;
            
            setTimeout(() => {
                window.open(linkedInUrl, '_blank');
            }, 1000);
        }
    </script>
