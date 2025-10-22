from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'clientes'

urlpatterns = [
    # Vistas accesibles para todos los usuarios autenticados
    path('perfil/', login_required(views.perfil_cliente), name='perfil_cliente'),
    path('crear-perfil/', login_required(views.crear_perfil_cliente), name='crear_perfil_cliente'),
    # Vistas públicas
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('activar/<uidb64>/<token>/', views.activar_cuenta, name='activar_cuenta'),
]