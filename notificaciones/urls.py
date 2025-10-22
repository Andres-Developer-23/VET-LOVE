from django.urls import path
from . import views

app_name = 'notificaciones'

urlpatterns = [
    path('', views.lista_notificaciones, name='lista'),
    path('recordatorios/', views.lista_recordatorios, name='recordatorios'),
    path('<int:notificacion_id>/', views.detalle_notificacion, name='detalle'),
    path('marcar-leida/<int:notificacion_id>/', views.marcar_leida, name='marcar_leida'),
    path('conteo/', views.conteo_notificaciones, name='conteo'),
]