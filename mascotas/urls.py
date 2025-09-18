from django.urls import path
from . import views

app_name = 'mascotas'

urlpatterns = [
    path('', views.lista_mascotas, name='lista_mascotas'),
    path('agregar/', views.agregar_mascota, name='agregar_mascota'),
    path('<int:mascota_id>/', views.detalle_mascota, name='detalle_mascota'),
    path('<int:mascota_id>/editar/', views.editar_mascota, name='editar_mascota'),
    path('<int:mascota_id>/eliminar/', views.eliminar_mascota, name='eliminar_mascota'),
    path('<int:mascota_id>/agregar-historial/', views.agregar_historial, name='agregar_historial'),
    path('<int:mascota_id>/agregar-vacuna/', views.agregar_vacuna, name='agregar_vacuna'),
]