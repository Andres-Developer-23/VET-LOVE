from django.urls import path
from . import views
from clientes.decorators import usuario_autenticado_required

app_name = 'tienda'

urlpatterns = [
    # Productos (públicos - no requieren login)
    path('', views.lista_productos, name='lista_productos'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),

    # Carrito (requiere autenticación)
    path('carrito/', usuario_autenticado_required(views.ver_carrito), name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', usuario_autenticado_required(views.agregar_al_carrito), name='agregar_al_carrito'),
    path('carrito/actualizar/<int:item_id>/', usuario_autenticado_required(views.actualizar_carrito), name='actualizar_carrito'),
    path('carrito/eliminar/<int:item_id>/', usuario_autenticado_required(views.eliminar_del_carrito), name='eliminar_del_carrito'),
    path('carrito/vaciar/', usuario_autenticado_required(views.vaciar_carrito), name='vaciar_carrito'),
    path('carrito/widget/', usuario_autenticado_required(views.carrito_widget), name='carrito_widget'),

    # Órdenes (requiere autenticación)
    path('checkout/', usuario_autenticado_required(views.checkout), name='checkout'),
    # path('orden/crear/', views.crear_orden, name='crear_orden'),  # Eliminar o comentar esta línea
    path('mis-ordenes/', usuario_autenticado_required(views.mis_ordenes), name='mis_ordenes'),
    path('pago/respuesta/<str:numero_orden>/', usuario_autenticado_required(views.respuesta_pago), name='respuesta_pago'),
    path('pago/confirmacion/', views.confirmacion_pago, name='confirmacion_pago'),
    path('orden/<str:numero_orden>/consultar-pago/', usuario_autenticado_required(views.consultar_estado_pago), name='consultar_estado_pago'),
    path('orden/<str:numero_orden>/', usuario_autenticado_required(views.detalle_orden), name='detalle_orden'),
]