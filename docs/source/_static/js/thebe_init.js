document.addEventListener('DOMContentLoaded', function() {
    console.log("WPipe Thebe: Initializing...");

    // 1. Verificar si el usuario ya activó el motor en esta sesión
    const isEngineActive = sessionStorage.getItem('wpipe_thebe_active') === 'true';

    if (isEngineActive && window.thebelab) {
        console.log("WPipe Thebe: Restoring active session...");
        window.thebelab.bootstrap();
    }

    // 2. Escuchar cambios de estado para actualizar UI y persistencia
    document.addEventListener('thebe-status-changed', function(e) {
        const status = e.detail.status;
        console.log("WPipe Thebe Status:", status);
        
        const activateBtn = document.querySelector('.thebe-button');
        
        if (status === "building" || status === "starting") {
            if (activateBtn) activateBtn.innerHTML = "🚀 SINCRONIZANDO MOTOR...";
            sessionStorage.setItem('wpipe_thebe_active', 'true');
        } 
        else if (status === "ready") {
            if (activateBtn) {
                activateBtn.innerHTML = "✅ MOTOR CONECTADO";
                setTimeout(() => activateBtn.style.display = 'none', 1500);
            }
        }
        else if (status === "failed") {
            if (activateBtn) {
                activateBtn.innerHTML = "❌ REINTENTAR CONEXIÓN";
                activateBtn.style.background = "#ef4444";
                sessionStorage.removeItem('wpipe_thebe_active');
            }
        }
    });

    // 3. Capturar el clic inicial si el motor no estaba activo
    document.body.addEventListener('click', function(e) {
        if (e.target.classList.contains('thebe-button')) {
            sessionStorage.setItem('wpipe_thebe_active', 'true');
            // thebelab.bootstrap() se llama automáticamente por la directiva de Sphinx
            // pero nos aseguramos por si acaso:
            if (window.thebelab) window.thebelab.bootstrap();
        }
    });
});
