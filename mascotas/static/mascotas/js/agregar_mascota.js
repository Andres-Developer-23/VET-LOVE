// Funcionalidad para el formulario de agregar mascota
document.addEventListener('DOMContentLoaded', function() {
    // Agregar clase required-field a labels de campos obligatorios
    const requiredFields = document.querySelectorAll('input[required], select[required], textarea[required]');
    requiredFields.forEach(field => {
        const label = document.querySelector(`label[for="${field.id}"]`);
        if (label) {
            label.classList.add('required-field');
        }
    });

    // Mejorar la experiencia de usuario en campos de fecha
    const dateFields = document.querySelectorAll('input[type="date"]');
    dateFields.forEach(field => {
        field.addEventListener('focus', function() {
            this.showPicker && this.showPicker();
        });
    });

    // Animación suave al hacer scroll a secciones con errores
    const errorFields = document.querySelectorAll('.field-errors');
    if (errorFields.length > 0) {
        const firstError = errorFields[0].closest('.floating-label');
        if (firstError) {
            firstError.scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
        }
    }
});