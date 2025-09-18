from django.urls import path
from . import views

app_name = 'citas'

urlpatterns = [
    path('solicitar/', views.solicitar_cita, name='solicitar_cita'),
    path('mis-citas/', views.mis_citas, name='mis_citas'),
    path('cancelar/<int:cita_id>/', views.cancelar_cita, name='cancelar_cita'),
]