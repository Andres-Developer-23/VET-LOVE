// Colores para los gráficos
const colors = {
    primary: '#007bff',
    success: '#28a745',
    info: '#17a2b8',
    warning: '#ffc107',
    danger: '#dc3545',
    secondary: '#6c757d',
    dark: '#343a40',
    purple: '#6f42c1',
    pink: '#e83e8c',
    teal: '#20c997',
    orange: '#fd7e14'
};

// Configuración global de Chart.js
Chart.defaults.font.family = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif";
Chart.defaults.font.size = 12;

// Datos iniciales
const citasPorEstado = {{ citas_por_estado_json|safe }};
const mascotasPorTipo = {{ mascotas_por_tipo_json|safe }};
const productosPorCategoria = {{ productos_por_categoria_json|safe }};
const ordenesPorEstado = {{ ordenes_por_estado_json|safe }};
const citasUltimos7Dias = {{ citas_ultimos_7_dias_json|safe }};
const ventasUltimos7Dias = {{ ventas_ultimos_7_dias_json|safe }};

// FUNCIONES EXISTENTES
function actualizarDatos() {
    fetch('{% url "administracion:estadisticas_api" %}')
        .then(response => response.json())
        .then(data => {
            console.log('Datos actualizados:', data);
            mostrarNotificacion('Datos actualizados correctamente', 'success');
        })
        .catch(error => {
            console.error('Error al actualizar:', error);
            mostrarNotificacion('Error al actualizar datos', 'danger');
        });
}

function mostrarNotificacion(mensaje, tipo) {
    const alert = document.createElement('div');
    alert.className = `alert alert-${tipo} alert-dismissible fade show position-fixed`;
    alert.style.cssText = 'top: 80px; right: 20px; z-index: 1050; min-width: 300px;';
    alert.innerHTML = `
        ${mensaje}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alert);

    setTimeout(() => {
        alert.remove();
    }, 3000);
}

// Función global para exportación
function exportar(formato) {
    console.log(`🎯 Iniciando exportación: ${formato}`);

    const form = document.getElementById('exportForm');
    const formatoInput = document.getElementById('formatoInput');

    if (!form) {
        console.error('❌ Formulario de exportación no encontrado');
        alert('Error interno: Formulario no encontrado');
        return;
    }

    if (!formatoInput) {
        console.error('❌ Input de formato no encontrado');
        alert('Error interno: Campo de formato no encontrado');
        return;
    }

    // Establecer el formato
    formatoInput.value = formato;

    // Mostrar indicador de carga en todos los botones de exportación
    const buttons = form.querySelectorAll('button');
    buttons.forEach(btn => {
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Procesando...';
    });

    console.log(`📤 Enviando formulario con formato: ${formato}`);
    form.submit();
}

// Inicializar cuando el documento esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Dashboard JavaScript cargado correctamente');

    // Verificar que la función exportar existe
    if (typeof exportar === 'function') {
        console.log('✅ Función exportar disponible');
    } else {
        console.error('❌ Función exportar no encontrada');
    }

    // Actualizar automáticamente cada 5 minutos
    setInterval(actualizarDatos, 300000);

    // Inicializar gráficos cuando se cambie de pestaña
    const tabEl = document.querySelector('button[data-bs-target="#overview"]');
    if (tabEl) {
        tabEl.addEventListener('shown.bs.tab', function() {
            // Re-renderizar gráficos si es necesario
            if (typeof renderEstadoCitasChart === 'function') {
                setTimeout(() => {
                    renderEstadoCitasChart();
                    renderTipoMascotasChart();
                    renderProductosCategoriaChart();
                    renderOrdenesEstadoChart();
                    renderTendenciaCitasChart();
                    renderTendenciaVentasChart();
                }, 100);
            }
        });
    }
});