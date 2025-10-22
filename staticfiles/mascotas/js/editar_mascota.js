// Funcionalidad para el formulario de editar mascota
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
        const tipoField = document.getElementById('id_tipo');

        // Validaciones básicas
        if (nombreField && !nombreField.value.trim()) {
            e.preventDefault();
            mostrarAlerta('El nombre de la mascota es obligatorio.', 'warning');
            nombreField.focus();
            return false;
        }

        if (tipoField && !tipoField.value) {
            e.preventDefault();
            mostrarAlerta('El tipo de mascota es obligatorio.', 'warning');
            tipoField.focus();
            return false;
        }

        // Validación de fecha de nacimiento
        const fechaNacimientoField = document.getElementById('id_fecha_nacimiento');
        if (fechaNacimientoField && fechaNacimientoField.value) {
            const fechaNacimiento = new Date(fechaNacimientoField.value);
            const hoy = new Date();

            if (fechaNacimiento > hoy) {
                e.preventDefault();
                mostrarAlerta('La fecha de nacimiento no puede ser futura.', 'warning');
                fechaNacimientoField.focus();
                return false;
            }

            // Calcular edad aproximada
            const edad = hoy.getFullYear() - fechaNacimiento.getFullYear();
            if (edad > 30) {
                mostrarAlerta('La edad calculada es mayor a 30 años. Verifique la fecha.', 'warning');
            }
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

    // Previsualización de imagen
    const fotoField = document.getElementById('id_foto');
    if (fotoField) {
        fotoField.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Validar tipo de archivo
                const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
                if (!allowedTypes.includes(file.type)) {
                    mostrarAlerta('Solo se permiten archivos de imagen (JPG, PNG, GIF).', 'danger');
                    this.value = '';
                    return;
                }

                // Validar tamaño (máximo 5MB)
                if (file.size > 5 * 1024 * 1024) {
                    mostrarAlerta('La imagen no puede ser mayor a 5MB.', 'danger');
                    this.value = '';
                    return;
                }

                // Mostrar previsualización
                const reader = new FileReader();
                reader.onload = function(e) {
                    const previewImg = document.querySelector('.img-fluid');
                    if (previewImg) {
                        previewImg.src = e.target.result;
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }

    console.log('Formulario de editar mascota inicializado correctamente');
});