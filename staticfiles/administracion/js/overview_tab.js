// Gráficos para la pestaña de resumen

// Definir colores para los gráficos
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

function renderEstadoCitasChart() {
    const ctx = document.getElementById('estadoCitasChart');
    if (!ctx) return;

    const context = ctx.getContext('2d');
    const data = {
        labels: citasPorEstado.map(item => item.estado.toUpperCase()),
        datasets: [{
            data: citasPorEstado.map(item => item.total),
            backgroundColor: [
                colors.success, colors.primary, colors.warning, colors.danger, colors.info
            ],
            borderWidth: 0
        }]
    };

    new Chart(context, {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((context.parsed / total) * 100);
                            return `${context.label}: ${context.parsed} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

function renderTipoMascotasChart() {
    const ctx = document.getElementById('tipoMascotasChart');
    if (!ctx) return;

    const context = ctx.getContext('2d');
    const data = {
        labels: mascotasPorTipo.map(item => item.tipo.toUpperCase()),
        datasets: [{
            data: mascotasPorTipo.map(item => item.total),
            backgroundColor: [
                colors.primary, colors.success, colors.warning, colors.info, colors.danger
            ],
            borderWidth: 0
        }]
    };

    new Chart(context, {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        drawBorder: false
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

function renderProductosCategoriaChart() {
    const ctx = document.getElementById('productosCategoriaChart');
    if (!ctx) return;

    const context = ctx.getContext('2d');
    const data = {
        labels: productosPorCategoria.map(item => item.categoria__nombre?.toUpperCase() || 'SIN CATEGORÍA'),
        datasets: [{
            data: productosPorCategoria.map(item => item.total),
            backgroundColor: [
                colors.teal, colors.orange, colors.pink, colors.purple, colors.info, colors.warning
            ],
            borderWidth: 0
        }]
    };

    new Chart(context, {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        drawBorder: false
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

function renderOrdenesEstadoChart() {
    const ctx = document.getElementById('ordenesEstadoChart');
    if (!ctx) return;

    const context = ctx.getContext('2d');
    const data = {
        labels: ordenesPorEstado.map(item => item.estado.toUpperCase()),
        datasets: [{
            data: ordenesPorEstado.map(item => item.total),
            backgroundColor: [
                colors.success, colors.info, colors.warning, colors.secondary, colors.danger
            ],
            borderWidth: 0
        }]
    };

    new Chart(context, {
        type: 'pie',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                }
            }
        }
    });
}

function renderTendenciaCitasChart() {
    const ctx = document.getElementById('tendenciaCitasChart');
    if (!ctx) return;

    const context = ctx.getContext('2d');
    const data = {
        labels: citasUltimos7Dias.map(item => item.dia),
        datasets: [{
            label: 'Citas por Día',
            data: citasUltimos7Dias.map(item => item.total),
            borderColor: colors.primary,
            backgroundColor: 'rgba(0, 123, 255, 0.1)',
            borderWidth: 3,
            fill: true,
            tension: 0.4
        }]
    };

    new Chart(context, {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        drawBorder: false
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

function renderTendenciaVentasChart() {
    const ctx = document.getElementById('tendenciaVentasChart');
    if (!ctx) return;

    const context = ctx.getContext('2d');
    const data = {
        labels: ventasUltimos7Dias.map(item => item.dia),
        datasets: [{
            label: 'Ventas por Día',
            data: ventasUltimos7Dias.map(item => item.total),
            borderColor: colors.purple,
            backgroundColor: 'rgba(111, 66, 193, 0.1)',
            borderWidth: 3,
            fill: true,
            tension: 0.4
        }]
    };

    new Chart(context, {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        drawBorder: false
                    },
                    ticks: {
                        callback: function(value) {
                            return '$' + value;
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// Inicializar gráficos cuando la pestaña esté activa
document.addEventListener('DOMContentLoaded', function() {
    console.log('Inicializando gráficos del dashboard...');

    // Verificar que las variables de datos estén disponibles
    if (typeof citasPorEstado === 'undefined') {
        console.error('Error: citasPorEstado no está definido');
        return;
    }
    if (typeof mascotasPorTipo === 'undefined') {
        console.error('Error: mascotasPorTipo no está definido');
        return;
    }
    if (typeof productosPorCategoria === 'undefined') {
        console.error('Error: productosPorCategoria no está definido');
        return;
    }
    if (typeof ordenesPorEstado === 'undefined') {
        console.error('Error: ordenesPorEstado no está definido');
        return;
    }
    if (typeof citasUltimos7Dias === 'undefined') {
        console.error('Error: citasUltimos7Dias no está definido');
        return;
    }
    if (typeof ventasUltimos7Dias === 'undefined') {
        console.error('Error: ventasUltimos7Dias no está definido');
        return;
    }

    console.log('Datos verificados, renderizando gráficos...');

    // Inicializar gráficos inmediatamente para la pestaña activa
    try {
        renderEstadoCitasChart();
        console.log('✅ Gráfico de estado de citas renderizado');
    } catch (error) {
        console.error('❌ Error renderizando gráfico de estado de citas:', error);
    }

    try {
        renderTipoMascotasChart();
        console.log('✅ Gráfico de tipos de mascotas renderizado');
    } catch (error) {
        console.error('❌ Error renderizando gráfico de tipos de mascotas:', error);
    }

    try {
        renderProductosCategoriaChart();
        console.log('✅ Gráfico de productos por categoría renderizado');
    } catch (error) {
        console.error('❌ Error renderizando gráfico de productos por categoría:', error);
    }

    try {
        renderOrdenesEstadoChart();
        console.log('✅ Gráfico de órdenes por estado renderizado');
    } catch (error) {
        console.error('❌ Error renderizando gráfico de órdenes por estado:', error);
    }

    try {
        renderTendenciaCitasChart();
        console.log('✅ Gráfico de tendencia de citas renderizado');
    } catch (error) {
        console.error('❌ Error renderizando gráfico de tendencia de citas:', error);
    }

    try {
        renderTendenciaVentasChart();
        console.log('✅ Gráfico de tendencia de ventas renderizado');
    } catch (error) {
        console.error('❌ Error renderizando gráfico de tendencia de ventas:', error);
    }

    console.log('🎉 Todos los gráficos han sido inicializados');
});