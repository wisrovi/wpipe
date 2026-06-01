.. raw:: html

    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>

    <div id="cert-final-container" style="margin-top: 50px; text-align: center;">
        <div id="certificate-final" style="width: 800px; height: 500px; margin: 0 auto; background: linear-gradient(135deg, #020617 0%, #0f172a 50%, #1e293b 100%); border: 10px solid #00f2fe; border-radius: 20px; padding: 40px; color: white; position: relative; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; box-sizing: border-box; overflow: hidden;">
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; opacity: 0.15; background: url('data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23 47c3.314 0 6-2.686 6-6s-2.686-6-6-6-6 2.686-6 6 2.686 6 6 6z' fill='%2300f2fe' fill-opacity='0.4' fill-rule='evenodd'/%3E%3C/svg%3E');"></div>
            
            <div style="position: relative; z-index: 1;">
                <h1 style="color: #00f2fe; margin: 0; font-size: 2.8em; text-transform: uppercase; font-weight: 800; letter-spacing: 2px;">Arquitecto de Pipelines</h1>
                <p style="font-size: 1.2em; margin-top: 5px; opacity: 0.8; letter-spacing: 1px;">CERTIFICACIÓN PROFESIONAL WPipe</p>
                
                <div style="margin: 35px 0;">
                    <p style="font-size: 1.3em; margin-bottom: 5px; opacity: 0.9;">Se certifica que:</p>
                    <h2 id="cert-name-final" style="font-size: 3.8em; color: white; border-bottom: 3px solid #00f2fe; display: inline-block; padding: 0 50px; margin: 0; font-family: serif; text-shadow: 0 0 15px rgba(0, 242, 254, 0.3);">Arquitecto WPipe</h2>
                </div>
                
                <div style="margin-top: 20px;">
                    <p style="max-width: 650px; margin: 0 auto; font-size: 1.15em; line-height: 1.6; color: #cbd5e0;">Ha completado satisfactoriamente los <b>140 niveles</b> de "La Senda del Maestro", demostrando maestría absoluta en orquestación industrial, paralelismo masivo y arquitecturas distribuidas.</p>
                </div>
                
                <div style="margin-top: 35px; display: flex; justify-content: space-between; align-items: flex-end; padding: 0 50px;">
                    <div style="text-align: left;">
                        <p style="margin: 0; font-weight: bold; color: #00f2fe;">WISROVI ECOSYSTEM</p>
                        <p style="margin: 0; font-size: 0.85em; opacity: 0.6;">Verification Code: WP-140-ZEN</p>
                    </div>
                    <div style="text-align: right;">
                         <div style="width: 90px; height: 90px; background: rgba(0, 242, 254, 0.1); border: 2px solid #00f2fe; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 3em; box-shadow: 0 0 30px rgba(0, 242, 254, 0.4);">🎓</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div style="margin-top: 30px; display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;">
            <button onclick="downloadCert('certificate-final', 'Certificado_WPipe_Maestro.png')" style="padding: 15px 40px; border-radius: 50px; border: none; background: #00f2fe; color: #020617; font-weight: 800; cursor: pointer; display: flex; align-items: center; gap: 10px; font-size: 1.1em; transition: all 0.3s;">
                🏆 Descargar mi Título (PNG)
            </button>
            <button onclick="shareLinkedIn('Senda del Maestro: 140 Niveles', '140')" style="padding: 15px 40px; border-radius: 50px; border: 2px solid #00f2fe; background: transparent; color: #00f2fe; font-weight: 800; cursor: pointer; display: flex; align-items: center; gap: 10px; font-size: 1.1em; transition: all 0.3s;">
                💼 Publicar en mi LinkedIn
            </button>
        </div>
    </div>

    <script>
        function updateCertNameFinal() {
            const name = localStorage.getItem('wpipe_user_name') || 'Arquitecto WPipe';
            const nameEl = document.getElementById('cert-name-final');
            if (nameEl) nameEl.innerText = name;
        }

        function downloadCert(divId, filename) {
            const element = document.getElementById(divId);
            html2canvas(element, {
                scale: 3,
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
            const text = encodeURIComponent(`¡Día de graduación! 🎓 He completado los 140 niveles de La Senda del Maestro en WPipe.

Me he certificado como Arquitecto de Pipelines, dominando el arte de la orquestación industrial. Gracias al tour de aprendizaje de Wisrovi por este viaje increíble.

#WPipe #Architecture #Graduation #Python #DataEngineering #Wisrovi`);
            const url = encodeURIComponent('https://wpipe.readthedocs.io/');
            window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${url}`, '_blank');
        }

        window.addEventListener('DOMContentLoaded', updateCertNameFinal);
        setTimeout(updateCertNameFinal, 500);
    </script>


📜 Próximos Pasos
================

Ahora que eres un experto en WPipe, te recomendamos:

1. **Contribuir al Núcleo**: Revisa el :doc:`../../contributing` y ayuda a mejorar el motor.
2. **Desplegar en Producción**: Sigue la guía de :doc:`../production_deployment`.
3. **Compartir tu Éxito**: Añade tu nombre a :doc:`../../USERS` y cuéntanos qué has construido.

*La maestría no es un destino, es un proceso continuo. Sigue construyendo.*
