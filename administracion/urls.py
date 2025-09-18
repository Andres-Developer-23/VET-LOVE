from django.urls import path
from . import views

app_name = 'administracion'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard_admin'),
    path('dashboard/exportar/', views.exportar_datos, name='exportar_datos'),
]