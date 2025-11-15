from django.urls import path
from . import views

app_name = 'veterinario'

urlpatterns = [
    # Dashboard veterinario
    path('dashboard/', views.dashboard_veterinario, name='dashboard_veterinario'),

    # Gestión de mascotas
    path('mascotas/', views.gestion_mascotas_veterinario, name='gestion_mascotas_veterinario'),

    # Gestión de citas
    path('citas/', views.gestion_citas_veterinario, name='gestion_citas_veterinario'),

    # Historial médico
    path('historial-medico/<int:mascota_id>/', views.historial_medico_veterinario, name='historial_medico_veterinario'),
]