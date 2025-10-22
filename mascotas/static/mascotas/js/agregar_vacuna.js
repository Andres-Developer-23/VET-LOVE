// Funcionalidad para el formulario de agregar vacuna
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
        const nombreField = document.getElementById('id_nombre');
        const fechaAplicacionField = document.getElementById('id_fecha_aplicacion');

        // Validaciones básicas
        if (nombreField && !nombreField.value.trim()) {
            e.preventDefault();
            mostrarAlerta('El nombre de la vacuna es obligatorio.', 'warning');
            nombreField.focus();
            return false;
        }

        if (fechaAplicacionField && !fechaAplicacionField.value) {
            e.preventDefault();
            mostrarAlerta('La fecha de aplicación es obligatoria.', 'warning');
            fechaAplicacionField.focus();
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
    const fechaFields = document.querySelectorAll('input[type="date"]');
    fechaFields.forEach(field => {
        field.addEventListener('change', function() {
            // Validar que la fecha no sea futura para aplicación
            if (this.id === 'id_fecha_aplicacion') {
                const selectedDate = new Date(this.value);
                const today = new Date();
                today.setHours(0, 0, 0, 0);

                if (selectedDate > today) {
                    mostrarAlerta('La fecha de aplicación no puede ser futura.', 'warning');
                    this.value = '';
                    this.focus();
                }
            }
        });
    });

    // Auto-calcular fecha próxima si hay un patrón estándar
    const fechaAplicacionField = document.getElementById('id_fecha_aplicacion');
    const fechaProximaField = document.getElementById('id_fecha_proxima');

    if (fechaAplicacionField && fechaProximaField) {
        fechaAplicacionField.addEventListener('change', function() {
            if (this.value && !fechaProximaField.value) {
                // Sugerir fecha próxima (ejemplo: 1 año después)
                const aplicacionDate = new Date(this.value);
                const proximaDate = new Date(aplicacionDate);
                proximaDate.setFullYear(aplicacionDate.getFullYear() + 1);

                const year = proximaDate.getFullYear();
                const month = String(proximaDate.getMonth() + 1).padStart(2, '0');
                const day = String(proximaDate.getDate()).padStart(2, '0');
                fechaProximaField.value = `${year}-${month}-${day}`;

                mostrarAlerta('Se ha sugerido una fecha próxima (1 año después). Puedes modificarla si es necesario.', 'info');
            }
        });
    }

    console.log('Formulario de agregar vacuna inicializado correctamente');
});