from django.urls import path
from . import views
from .decorators import cliente_required, administrador_required

app_name = 'clientes'

urlpatterns = [
    path('perfil/', cliente_required(views.perfil_cliente), name='perfil_cliente'),
    path('crear-perfil/', cliente_required(views.crear_perfil_cliente), name='crear_perfil_cliente'),
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('activar/<uidb64>/<token>/', views.activar_cuenta, name='activar_cuenta'),
]