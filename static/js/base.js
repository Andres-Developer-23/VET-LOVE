// Funciones base de la aplicación
document.addEventListener('DOMContentLoaded', function() {
    // Manejar el cierre automático de alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        },10000);
    });

    // Prevenir envío múltiple de formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';
            }
        });
    });

    // Actualizar contador del carrito
    function actualizarCarritoWidget() {
        fetch('/tienda/carrito/widget/')
            .then(response => response.json())
            .then(data => {
                const cartCount = document.getElementById('cart-count');
                if (cartCount) {
                    cartCount.textContent = data.cantidad_total;
                    // Ocultar badge si no hay items
                    if (data.cantidad_total === 0) {
                        cartCount.style.display = 'none';
                    } else {
                        cartCount.style.display = 'flex';
                    }
                }
            })
            .catch(error => console.error('Error:', error));
    }

    // Actualizar contador de notificaciones
    function actualizarNotificacionesWidget() {
        fetch('/notificaciones/conteo/')
            .then(response => response.json())
            .then(data => {
                const notifCount = document.getElementById('notificaciones-count');
                if (notifCount) {
                    const navLink = notifCount.closest('.nav-link');
                    notifCount.textContent = data.total_no_leidas;
                    // Ocultar badge si no hay notificaciones
                    if (data.total_no_leidas === 0) {
                        notifCount.style.display = 'none';
                        if (navLink) navLink.classList.remove('has-notifications');
                    } else {
                        notifCount.style.display = 'flex';
                        if (navLink) navLink.classList.add('has-notifications');
                    }
                }
            })
            .catch(error => console.error('Error:', error));
    }

    // Actualizar al cargar la página
    actualizarCarritoWidget();
    actualizarNotificacionesWidget();

    // Actualizar cada 30 segundos
    setInterval(actualizarCarritoWidget, 30000);
    setInterval(actualizarNotificacionesWidget, 30000);

    // Aplicar sticky a la caja de filtros de la tienda (detectada por icono de filtro)
    document.querySelectorAll('.card-header i.fa-filter').forEach(function(icon) {
        var card = icon.closest('.card');
        if (card) {
            card.classList.add('sticky-sidebar');
        }
    });
});