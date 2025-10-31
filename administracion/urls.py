from django.urls import path
from . import views
from clientes.decorators import administrador_required

app_name = 'administracion'

urlpatterns = [
    # Dashboard administrador
    path('dashboard/', administrador_required(views.dashboard), name='dashboard_admin'),
    path('dashboard/exportar/', administrador_required(views.exportar_datos), name='exportar_datos'),
    path('api/estadisticas/', administrador_required(views.estadisticas_api), name='estadisticas_api'),
    path('preview-pagina-web/', administrador_required(views.preview_pagina_web), name='preview_pagina_web'),
    path('preview-tienda/', administrador_required(views.preview_tienda), name='preview_tienda'),
    path('dashboard/tienda/', administrador_required(views.preview_tienda), name='dashboard_tienda'),

    # Gestión de notificaciones
    path('notificaciones/', administrador_required(views.gestion_notificaciones), name='gestion_notificaciones'),
    path('notificaciones/crear/', administrador_required(views.crear_notificacion), name='crear_notificacion'),

    # Gestión de usuarios
    path('usuarios/', administrador_required(views.gestionar_usuarios), name='gestion_usuarios'),
    path('usuarios/crear/', administrador_required(views.crear_usuario), name='crear_usuario'),
    path('usuarios/editar/<int:user_id>/', administrador_required(views.editar_usuario), name='editar_usuario'),

    # Gestión de citas
    path('citas/cambiar-estado/<int:cita_id>/', administrador_required(views.cambiar_estado_cita), name='cambiar_estado_cita'),

    # Plantillas de carnets
    path('plantillas-carnets/', administrador_required(views.descargar_plantillas_carnets), name='descargar_plantillas_carnets'),

    # URLs para veterinarios
    path('veterinario/dashboard/', views.dashboard_veterinario, name='dashboard_veterinario'),
]