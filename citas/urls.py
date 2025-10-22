from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'citas'

urlpatterns = [
    # Vistas accesibles para usuarios autenticados (clientes y administradores)
    path('solicitar/', login_required(views.solicitar_cita), name='solicitar_cita'),
    path('mis-citas/', login_required(views.mis_citas), name='mis_citas'),
    path('cambiar-estado/<int:cita_id>/', login_required(views.cambiar_estado_cita), name='cambiar_estado_cita'),
    path('cancelar/<int:cita_id>/', login_required(views.cancelar_cita), name='cancelar_cita'),
]