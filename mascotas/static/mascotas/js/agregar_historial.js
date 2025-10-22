// Funcionalidad para el formulario de agregar historial médico
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    if (!form) return;

    // Función para mostrar alertas
    function mostrarAlerta(mensaje, tipo = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${tipo} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Insertar al inicio del contenedor principal
        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(alertDiv, container.firstChild);
        }

        // Auto-remover después de 5 segundos
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    // Validación del formulario antes de enviar
    form.addEventListener('submit', function(e) {
        const veterinarioField = document.getElementById('id_veterinario');
        const diagnosticoField = document.getElementById('id_diagnostico');

        // Validaciones básicas
        if (veterinarioField && !veterinarioField.value.trim()) {
            e.preventDefault();
            mostrarAlerta('El nombre del veterinario es obligatorio.', 'warning');
            veterinarioField.focus();
            return false;
        }

        if (diagnosticoField && !diagnosticoField.value.trim()) {
            e.preventDefault();
            mostrarAlerta('El diagnóstico es obligatorio.', 'warning');
            diagnosticoField.focus();
            return false;
        }

        // Mostrar indicador de carga
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Guardando...';
        }

        // El formulario se enviará normalmente
        return true;
    });

    // Mejorar la experiencia de usuario
    const pesoField = document.getElementById('id_peso');
    if (pesoField) {
        pesoField.addEventListener('input', function() {
            // Validar que el peso sea un número positivo
            const value = parseFloat(this.value);
            if (this.value && (isNaN(value) || value <= 0 || value > 200)) {
                mostrarAlerta('El peso debe ser un número positivo válido (máximo 200 kg).', 'warning');
                this.value = '';
                this.focus();
            }
        });
    }

    console.log('Formulario de agregar historial médico inicializado correctamente');
});