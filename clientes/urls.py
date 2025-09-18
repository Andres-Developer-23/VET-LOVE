# clientes/urls.py - Debe tener esto:
from django.urls import path
from . import views

app_name = 'clientes'  # Namespace de la aplicación

urlpatterns = [
    path('perfil/', views.perfil_cliente, name='perfil_cliente'),  # ← nombre correcto
    path('crear-perfil/', views.crear_perfil_cliente, name='crear_perfil_cliente'),
]