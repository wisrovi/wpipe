Nivel 80: demo_level80.py
=========================

Este es el nivel 80 del tour de aprendizaje.

Código Fuente
------------

.. literalinclude:: ../../../../examples/00_honey_pot/03_yield/demo_level80.py
   :language: python
   :linenos:

Resultado de Ejecución
----------------------

.. code-block:: text

   
   >>> Lambda con lógica condicional...
   
   🔍 Verificando sistema...
   🌡️ ALERTA: Sobrecalentamiento!
   Viaje_L80_LambdaComplex - Processing pipeline tasks ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00

.. raw:: html

    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    
    <div id="cert-m3-container" style="margin-top: 50px; text-align: center;">
        <div id="certificate-m3" style="width: 800px; height: 500px; margin: 0 auto; background: linear-gradient(135deg, #020617 0%, #7f1d1d 100%); border: 10px solid #ef4444; border-radius: 20px; padding: 40px; color: white; position: relative; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; box-sizing: border-box;">
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; opacity: 0.1; background-image: repeating-linear-gradient(45deg, #ffffff 0, #ffffff 1px, transparent 0, transparent 50%); background-size: 10px 10px;"></div>
            
            <div style="position: relative; z-index: 1;">
                <h1 style="color: #ef4444; margin: 0; font-size: 3em; text-transform: uppercase; font-weight: 800;">Certificado de Misión</h1>
                <p style="font-size: 1.2em; margin-top: 10px; opacity: 0.8;">WPipe Learning Tour: Misiones 2 y 3 Completadas</p>
                
                <div style="margin: 40px 0;">
                    <p style="font-size: 1.5em; margin-bottom: 5px;">Se otorga a:</p>
                    <h2 id="cert-name-m3" style="font-size: 3.5em; color: white; border-bottom: 2px solid #ef4444; display: inline-block; padding: 0 40px; margin: 0; font-family: serif;">Arquitecto WPipe</h2>
                </div>
                
                <div style="margin-top: 30px;">
                    <h3 style="color: #ef4444; font-size: 1.8em; margin: 0;">Guardián de la Resiliencia WPipe</h3>
                    <p style="max-width: 600px; margin: 15px auto; font-size: 1.1em; color: #cbd5e0;">Por dominar la lógica de control avanzada, estrategias de reintento y persistencia mediante Checkpoints en entornos críticos.</p>
                </div>
                
                <div style="margin-top: 40px; display: flex; justify-content: space-between; align-items: flex-end; padding: 0 40px;">
                    <div style="text-align: left;">
                        <p style="margin: 0; font-weight: bold;">WPipe v2.3.0 LTS</p>
                        <p style="margin: 0; font-size: 0.9em; opacity: 0.7;">Wisrovi Ecosystem</p>
                    </div>
                    <div style="width: 80px; height: 80px; background: #ef4444; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2.5em; box-shadow: 0 0 20px rgba(239, 68, 68, 0.5);">🛡️</div>
                </div>
            </div>
        </div>
        
        <div style="margin-top: 30px; display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;">
            <button onclick="downloadCert('certificate-m3', 'Certificado_WPipe_Resiliencia.png')" style="padding: 12px 30px; border-radius: 50px; border: none; background: #ef4444; color: white; font-weight: 800; cursor: pointer; display: flex; align-items: center; gap: 10px;">
                ⬇️ Descargar Diploma (PNG)
            </button>
            <button onclick="shareLinkedIn('Misión 3: El Guardián de la Resiliencia', '80')" style="padding: 12px 30px; border-radius: 50px; border: 2px solid #ef4444; background: transparent; color: #ef4444; font-weight: 800; cursor: pointer; display: flex; align-items: center; gap: 10px;">
                🔗 Compartir en LinkedIn
            </button>
        </div>
    </div>

    <script>
        function updateCertNameM3() {
            const name = localStorage.getItem('wpipe_user_name') || 'Arquitecto WPipe';
            const nameEl = document.getElementById('cert-name-m3');
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
            const text = encodeURIComponent(`¡Nuevo hito alcanzado! 🛡️ He completado el nivel ${level} de WPipe, certificándome como Guardián de la Resiliencia.

Dominando Checkpoints, WAL Mode y lógica de control avanzada. Mi camino hacia la maestría continúa.

#WPipe #Python #Resilience #DataEngineering #Wisrovi`);
            const url = encodeURIComponent('https://wpipe.readthedocs.io/');
            window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${url}`, '_blank');
        }

        window.addEventListener('DOMContentLoaded', updateCertNameM3);
        setTimeout(updateCertNameM3, 500);
    </script>


