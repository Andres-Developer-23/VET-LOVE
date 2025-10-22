// Gestión de citas en el dashboard
function cambiarEstadoCita(citaId, nuevoEstado) {
    if (!confirm(`¿Estás seguro de cambiar el estado de esta cita a "${nuevoEstado.toUpperCase()}"?`)) {
        return;
    }

    // Mostrar loading
    const button = event.target.closest('button');
    const originalHTML = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    button.disabled = true;

    // Enviar petición AJAX
    fetch(`/citas/cambiar-estado/${citaId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: `estado=${encodeURIComponent(nuevoEstado)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Actualizar la interfaz
            location.reload();
        } else {
            alert('Error al cambiar el estado de la cita: ' + (data.error || 'Error desconocido'));
            button.innerHTML = originalHTML;
            button.disabled = false;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error de conexión al cambiar el estado de la cita');
        button.innerHTML = originalHTML;
        button.disabled = false;
    });
}

// Función para filtrar citas en tiempo real
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('input[name="cita_busqueda"]');
    const estadoSelect = document.querySelector('select[name="cita_estado"]');
    const tipoSelect = document.querySelector('select[name="cita_tipo"]');

    function filtrarCitas() {
        const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
        const estadoFiltro = estadoSelect ? estadoSelect.value : '';
        const tipoFiltro = tipoSelect ? tipoSelect.value : '';

        const filas = document.querySelectorAll('tbody tr');

        filas.forEach(fila => {
            if (fila.querySelector('td[colspan]')) return; // Saltar fila de "no hay citas"

            const textoFila = fila.textContent.toLowerCase();
            const estadoCita = fila.querySelector('.badge') ? fila.querySelector('.badge').textContent.toLowerCase() : '';
            const tipoCita = fila.cells[3] ? fila.cells[3].textContent.toLowerCase() : '';

            const coincideBusqueda = !searchTerm || textoFila.includes(searchTerm);
            const coincideEstado = !estadoFiltro || estadoCita.includes(estadoFiltro);
            const coincideTipo = !tipoFiltro || tipoCita.includes(tipoFiltro);

            fila.style.display = (coincideBusqueda && coincideEstado && coincideTipo) ? '' : 'none';
        });
    }

    if (searchInput) searchInput.addEventListener('input', filtrarCitas);
    if (estadoSelect) estadoSelect.addEventListener('change', filtrarCitas);
    if (tipoSelect) tipoSelect.addEventListener('change', filtrarCitas);

    // Resaltar citas urgentes
    const citasUrgentes = document.querySelectorAll('.badge-urgent').closest('tr');
    citasUrgentes.forEach(fila => {
        fila.style.borderLeft = '4px solid #dc3545';
        fila.style.backgroundColor = 'rgba(220, 53, 69, 0.05)';
    });

    console.log('✅ Gestión de citas inicializada');
});