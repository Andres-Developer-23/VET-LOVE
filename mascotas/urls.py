from django.urls import path
from . import views
from clientes.decorators import usuario_autenticado_required
from django.contrib.auth.decorators import login_required

app_name = 'mascotas'

urlpatterns = [
    # Vistas accesibles para usuarios autenticados (clientes y administradores)
    path('', login_required(views.lista_mascotas), name='lista_mascotas'),
    path('agregar/', login_required(views.agregar_mascota), name='agregar_mascota'),
    path('<int:mascota_id>/', login_required(views.detalle_mascota), name='detalle_mascota'),
    path('<int:mascota_id>/editar/', login_required(views.editar_mascota), name='editar_mascota'),
    path('<int:mascota_id>/eliminar/', login_required(views.eliminar_mascota), name='eliminar_mascota'),
    path('<int:mascota_id>/agregar-historial/', login_required(views.agregar_historial), name='agregar_historial'),
    path('<int:mascota_id>/agregar-vacuna/', login_required(views.agregar_vacuna), name='agregar_vacuna'),
    path('<int:mascota_id>/calendario-vacunas.json', login_required(views.calendario_vacunas), name='calendario_vacunas'),
    path('<int:mascota_id>/descargar-carnet/', login_required(views.descargar_carnet_pdf), name='descargar_carnet_pdf'),
    path('<int:mascota_id>/descargar-carnet-identificacion/', login_required(views.descargar_carnet_identificacion_pdf), name='descargar_carnet_identificacion_pdf'),
    path('<int:mascota_id>/descargar-plantilla-carnet/', login_required(views.descargar_plantilla_carnet_pdf), name='descargar_plantilla_carnet_pdf'),
]