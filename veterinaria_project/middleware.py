from django.http import HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import redirect

class RestrictAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar si el usuario intenta acceder al admin sin permisos
        if request.path.startswith('/admin/') and not request.path.startswith('/admin/login/'):
            if request.user.is_authenticated and not (request.user.is_staff or request.user.is_superuser):
                return HttpResponseForbidden("No tienes permisos para acceder al panel de administración.")
        
        response = self.get_response(request)
        return response

class RedirectAuthenticatedUsers:
    def __init__(self, get_response):
        self.get_response = get_response
        # Definir las URLs que queremos redirigir
        self.redirect_urls = [
            reverse('login'),
            reverse('clientes:registro_usuario'),
        ]

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.path in self.redirect_urls:
                if request.user.is_staff or request.user.is_superuser:
                    return redirect('admin:index')
                else:
                    return redirect('home')
        
        response = self.get_response(request)
        return response

class RedirectAdminToDashboard:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Redirigir admins autenticados que visiten la página de inicio al dashboard
        if (request.user.is_authenticated and 
            request.user.is_staff and 
            request.path == '/' and 
            not request.GET.get('noredirect')):
            from django.urls import reverse
            return redirect(reverse('administracion:dashboard_admin'))
        
        return response