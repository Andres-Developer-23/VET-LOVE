from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def redireccionar_despues_login(request):
    if request.user.is_staff:
        return redirect('administracion:dashboard_admin')
    else:
        return redirect('mascotas:lista_mascotas')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='inicio.html'), name='home'),
    path('mascotas/', include('mascotas.urls')),
    path('clientes/', include('clientes.urls')),
    path('citas/', include('citas.urls')),
    path('administracion/', include('administracion.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('redireccionar/', redireccionar_despues_login, name='redireccionar'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)