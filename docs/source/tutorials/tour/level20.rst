Nivel 20: demo_level20.py
=========================

Este es el nivel 20 del tour de aprendizaje.

Código Fuente
------------

.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level20.py
   :language: python
   :linenos:

Resultado de Ejecución
----------------------

.. code-block:: text

   
   [CONDITION] Evaluating: obstaculo == True and distancia < 10
   🚨 ABS: ¡Frenando bruscamente para evitar colisión!
   Viaje_L20_EmergencyLogic - Processing pipeline tasks ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00

.. raw:: html

    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    
    <div id="cert-m1-container" style="margin-top: 50px; text-align: center;">
        <div id="certificate-m1" style="width: 800px; height: 500px; margin: 0 auto; background: linear-gradient(135deg, #020617 0%, #064e3b 100%); border: 10px solid #10b981; border-radius: 20px; padding: 40px; color: white; position: relative; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; box-sizing: border-box;">
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; opacity: 0.1; background-image: radial-gradient(#ffffff 1px, transparent 1px); background-size: 20px 20px;"></div>
            
            <div style="position: relative; z-index: 1;">
                <h1 style="color: #10b981; margin: 0; font-size: 3em; text-transform: uppercase; font-weight: 800;">Certificado de Misión</h1>
                <p style="font-size: 1.2em; margin-top: 10px; opacity: 0.8;">WPipe Learning Tour: Misión 1 Completada</p>
                
                <div style="margin: 40px 0;">
                    <p style="font-size: 1.5em; margin-bottom: 5px;">Se otorga a:</p>
                    <h2 id="cert-name-m1" style="font-size: 3.5em; color: white; border-bottom: 2px solid #10b981; display: inline-block; padding: 0 40px; margin: 0; font-family: serif;">Arquitecto WPipe</h2>
                </div>
                
                <div style="margin-top: 30px;">
                    <h3 style="color: #10b981; font-size: 1.8em; margin: 0;">Iniciado del Motor WPipe</h3>
                    <p style="max-width: 600px; margin: 15px auto; font-size: 1.1em; color: #cbd5e0;">Por demostrar dominio en la instanciación de motores, gestión del Warehouse y orquestación de tareas atómicas.</p>
                </div>
                
                <div style="margin-top: 40px; display: flex; justify-content: space-between; align-items: flex-end; padding: 0 40px;">
                    <div style="text-align: left;">
                        <p style="margin: 0; font-weight: bold;">WPipe v2.3.0 LTS</p>
                        <p style="margin: 0; font-size: 0.9em; opacity: 0.7;">Wisrovi Ecosystem</p>
                    </div>
                    <div style="width: 80px; height: 80px; background: #10b981; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2.5em; box-shadow: 0 0 20px rgba(16, 185, 129, 0.5);">🎖️</div>
                </div>
            </div>
        </div>
        
        <div style="margin-top: 30px; display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;">
            <button onclick="downloadCert('certificate-m1', 'Certificado_WPipe_M1.png')" style="padding: 12px 30px; border-radius: 50px; border: none; background: #10b981; color: #020617; font-weight: 800; cursor: pointer; display: flex; align-items: center; gap: 10px; transition: transform 0.2s;">
                ⬇️ Descargar Diploma (PNG)
            </button>
            <button onclick="shareLinkedIn('Misión 1: El Despertar del Motor', '20')" style="padding: 12px 30px; border-radius: 50px; border: 2px solid #10b981; background: transparent; color: #10b981; font-weight: 800; cursor: pointer; display: flex; align-items: center; gap: 10px; transition: transform 0.2s;">
                🔗 Compartir en LinkedIn
            </button>
        </div>
    </div>

    <script>
        function updateCertName() {
            const name = localStorage.getItem('wpipe_user_name') || 'Arquitecto WPipe';
            const nameEl = document.getElementById('cert-name-m1');
            if (nameEl) nameEl.innerText = name;
        }

        function downloadCert(divId, filename) {
            const element = document.getElementById(divId);
            html2canvas(element, {
                scale: 2,
                backgroundColor: null,
                logging: false,
                useCORS: true
            }).then(canvas => {
                const link = document.createElement('a');
                link.download = filename;
                link.href = canvas.toDataURL('image/png');
                link.click();
            });
        }

        function shareLinkedIn(mission, level) {
            const name = localStorage.getItem('wpipe_user_name') || 'Arquitecto WPipe';
            const text = encodeURIComponent(`¡Logro desbloqueado! 🚀 Acabo de completar la ${mission} (Nivel ${level}) de la Senda del Maestro en WPipe.

Ya soy oficialmente Iniciado del Motor WPipe. Aprendiendo a orquestar flujos de datos industriales con Wisrovi.

#WPipe #Python #DataEngineering #Orchestration #LearningTour`);
            const url = encodeURIComponent('https://wpipe.readthedocs.io/');
            window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${url}`, '_blank');
        }

        window.addEventListener('DOMContentLoaded', updateCertName);
        setTimeout(updateCertName, 500);
    </script>


