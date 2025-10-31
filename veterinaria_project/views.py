from django.shortcuts import render
from tienda.models import Producto
from django.db import connection
from django.conf import settings

def home(request):
    """Vista para la página de inicio con productos destacados y promociones"""
    try:
        # Verificar si las tablas existen usando SQL apropiado para PostgreSQL
        with connection.cursor() as cursor:
            if 'postgresql' in settings.DATABASES['default']['ENGINE']:
                # PostgreSQL
                cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'tienda_producto');")
            else:
                # SQLite
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tienda_producto';")

            table_exists = cursor.fetchone()
            if not table_exists or not table_exists[0]:
                raise Exception("Tabla tienda_producto no existe")

        # Obtener productos destacados y en oferta para el carrusel
        productos_destacados = Producto.objects.filter(
            activo=True,
            destacado=True
        ).select_related('categoria')[:6]  # Máximo 6 productos para 2 slides

        # Si no hay suficientes destacados, agregar productos en oferta
        if productos_destacados.count() < 6:
            productos_oferta = Producto.objects.filter(
                activo=True,
                precio_descuento__isnull=False
            ).exclude(id__in=productos_destacados.values_list('id', flat=True))[:6-len(productos_destacados)]

            productos_destacados = list(productos_destacados) + list(productos_oferta)

        # Si aún no hay suficientes, agregar productos recientes
        if len(productos_destacados) < 6:
            productos_recientes = Producto.objects.filter(
                activo=True
            ).exclude(id__in=[p.id for p in productos_destacados])[:6-len(productos_destacados)]

            productos_destacados.extend(productos_recientes)

        # Obtener productos para promociones (productos en oferta con imágenes)
        productos_promocion = Producto.objects.filter(
            activo=True,
            precio_descuento__isnull=False,
            imagen__isnull=False
        ).select_related('categoria').order_by('-fecha_creacion')[:3]  # 3 productos para las 3 promociones
    except Exception as e:
        # Si hay error con la base de datos, mostrar página sin productos
        productos_destacados = []
        productos_promocion = []

    context = {
        'productos_destacados': productos_destacados,
        'productos_promocion': productos_promocion,
    }

    return render(request, 'inicio.html', context)