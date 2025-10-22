// Script para filtros y búsqueda
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchProductos');
    const filterButtons = document.querySelectorAll('.filter-buttons button');
    const productItems = document.querySelectorAll('.producto-item');

    // Función de búsqueda
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();

            productItems.forEach(item => {
                const productName = item.querySelector('strong').textContent.toLowerCase();
                const productDesc = item.querySelector('small') ? item.querySelector('small').textContent.toLowerCase() : '';

                if (productName.includes(searchTerm) || productDesc.includes(searchTerm)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }

    // Función de filtros
    if (filterButtons.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                const filter = this.getAttribute('data-filter');

                // Actualizar botones activos
                filterButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');

                // Aplicar filtro
                productItems.forEach(item => {
                    if (filter === 'all') {
                        item.style.display = '';
                    } else {
                        const hasFilter = item.getAttribute(`data-${filter}`) !== null &&
                                        item.getAttribute(`data-${filter}`) !== 'false' &&
                                        item.getAttribute(`data-${filter}`) !== '';
                        item.style.display = hasFilter ? '' : 'none';
                    }
                });
            });
        });
    }

    // Mostrar notificación si hay productos con stock bajo
    const lowStockItems = document.querySelectorAll('[data-stock="stock-bajo"]');
    if (lowStockItems.length > 0) {
        console.log(`⚠️ ${lowStockItems.length} productos con stock bajo`);
    }
});