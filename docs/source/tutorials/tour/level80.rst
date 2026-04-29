Nivel 80: demo_level80.py
=========================

Este es el nivel 80 del tour de aprendizaje.


.. thebe-button:: ACTIVAR MODO INTERACTIVO


Código Fuente
------------
.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level80.py
   :language: python
   :class: thebe


Resultado de Ejecución
----------------------
.. code-block:: text


   
   >>> Lambda con lógica condicional...
   
   🔍 Verificando sistema...
   🌡️ ALERTA: Sobrecalentamiento!
   viaje_l80_lambdacomplex ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00

.. raw:: html

    <div class="certificate-zone" style="margin-top: 60px; border-top: 2px solid #ef4444; padding: 40px; background: rgba(255,255,255,0.02); border-radius: 15px;">
        <div style="text-align: center; margin-bottom: 40px;">
            <h2 style="color: #ef4444; margin-bottom: 10px;">¡RECLAMA TU LOGRO!</h2>
            <p style="color: #94a3b8;">Introduce tu nombre para desbloquear tu certificado oficial.</p>
            <input type="text" id="cert-name-input" placeholder="ESCRIBE TU NOMBRE COMPLETO AQUÍ" 
                   style="background: #0f172a; border: 2px solid #334155; color: white; padding: 15px 25px; border-radius: 12px; margin-top: 15px; width: 80%; max-width: 500px; text-align: center; font-size: 1.2em; font-weight: bold; outline: none; border-color: #ef4444; box-shadow: 0 0 20px rgba(0,0,0,0.5);">
        </div>

        <div id="cert-container-80" style="width: 1000px; height: 700px; margin: 0 auto; border-radius: 25px; padding: 60px; color: white; position: relative; box-sizing: border-box; overflow: hidden; text-align: center; background: linear-gradient(135deg, #020617 0%, #7f1d1d 100%); border: 15px solid #ef4444; box-shadow: 0 40px 80px rgba(0,0,0,0.9);">
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; opacity: 0.15; background-image: radial-gradient(#ffffff 1px, transparent 1px); background-size: 35px 30px;"></div>
            <div style="position: relative; z-index: 1; height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h1 style="color: #ef4444; margin: 0; font-size: 3.2em; text-transform: uppercase; font-weight: 900; letter-spacing: 3px; text-shadow: 0 5px 15px rgba(0,0,0,0.5);">Certificado de Misión</h1>
                    <p style="font-size: 1.3em; margin-top: 10px; opacity: 0.8; letter-spacing: 1px;">WPipe Engine Certification • Misión 3</p>
                </div>
                
                <div style="margin: 10px 0;">
                    <p style="font-size: 1.4em; margin-bottom: 5px; color: #94a3b8;">Se otorga con honor a:</p>
                    <h2 class="cert-name-display" style="font-size: 4.2em; border-bottom: 4px solid #ef4444; min-width: 500px; display: inline-block; font-family: 'Times New Roman', serif; text-shadow: 0 0 20px rgba(255,255,255,0.3); margin: 10px 0; color: #fff;">---</h2>
                </div>

                <div style="margin-bottom: 10px;">
                    <p style="font-size: 1.5em; color: #fff; margin-bottom: 5px; opacity: 0.9;">Con el rango oficial de:</p>
                    <h3 style="color: #ef4444; font-size: 2.8em; margin: 0; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; text-shadow: 0 0 10px #ef444444;">Arquitecto WPipe Silver</h3>
                </div>

                <div style="display: flex; justify-content: space-between; align-items: flex-end; padding: 15px 30px; border-top: 1px solid rgba(255,255,255,0.1); margin-top: 10px;">
                    <div style="text-align: left; opacity: 0.9; font-family: 'Courier New', monospace; line-height: 1.4;">
                        <p style="margin: 0; color: #ef4444; font-weight: bold; font-size: 1.1em; letter-spacing: 1px;">EMITIDO EL: <span class="cert-date-display" style="color: #fff;">--/--/----</span></p>
                        <p style="margin: 0; color: #64748b; font-size: 0.8em; margin-bottom: 8px;">ID: WP-80-ARQ-LVER</p>
                        <p style="margin: 0; font-weight: 900; color: #fff; font-size: 1.2em; letter-spacing: 1px;">WISROVI SUITE • <span style="color: #ef4444;">WISROVI.DEV</span></p>
                        <p style="margin: 0; margin-top: 3px; font-size: 0.85em; color: #94a3b8;">Oficial Product: <span style="font-weight: bold; color: #cbd5e0;">wpipe.wisrovi.dev</span></p>
                    </div>
                    <div style="width: 100px; height: 100px; background: #ef4444; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 3.5em; box-shadow: 0 0 30px #ef444466; border: 4px solid rgba(255,255,255,0.1);">🛡️</div>
                </div>
            </div>
        </div>

        <div style="text-align: center; margin-top: 40px; display: flex; justify-content: center; gap: 20px;">
            <button id="btn-download" onclick="downloadCert(80)" disabled 
                    style="background: #475569; color: #94a3b8; padding: 12px 35px; border-radius: 12px; font-weight: bold; cursor: not-allowed; border: none; transition: all 0.3s; font-size: 1em;">⬇️ DESCARGAR PNG</button>
            <button id="btn-share" onclick="shareLinkedIn(80)" disabled 
                    style="background: #475569; color: #94a3b8; padding: 12px 35px; border-radius: 12px; font-weight: bold; cursor: not-allowed; border: none; transition: all 0.3s; font-size: 1em;">🔗 COMPARTIR LOGRO</button>
            <a href="level81.html" style="background: #ef4444; color: #020617; padding: 12px 35px; border-radius: 12px; font-weight: bold; text-decoration: none; display: flex; align-items: center; font-size: 1em;">CONTINUAR ➡️</a>
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
            const rank = "Arquitecto WPipe Silver";
            const text = `🚀 ¡Certificación alcanzada! Acabo de obtener mi rango de ${rank} en el WPipe Learning Tour. Agradezco a @wisrovi por crear este potente motor de orquestación industrial. #wpipe #python #dataengineering #backend #wisrovidev`;
            
            downloadCert(level);
            navigator.clipboard.writeText(text);
            const linkedInUrl = `https://www.linkedin.com/feed/?shareActive=true&text=${encodeURIComponent(text)}`;
            
            setTimeout(() => {
                window.open(linkedInUrl, '_blank');
            }, 1000);
        }
    </script>
