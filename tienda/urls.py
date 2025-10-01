from django.urls import path
from . import views

app_name = 'tienda'

urlpatterns = [
    # Productos
    path('', views.lista_productos, name='lista_productos'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    
    # Carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('carrito/widget/', views.carrito_widget, name='carrito_widget'),
    
    # Órdenes
    path('checkout/', views.checkout, name='checkout'),
    # path('orden/crear/', views.crear_orden, name='crear_orden'),  # Eliminar o comentar esta línea
    path('mis-ordenes/', views.mis_ordenes, name='mis_ordenes'),
    path('orden/<str:numero_orden>/', views.detalle_orden, name='detalle_orden'),
]