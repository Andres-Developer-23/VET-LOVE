from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages

def cliente_required(function=None):
    """
    Decorador que verifica que el usuario sea un cliente normal (no staff/admin)
    y tenga un perfil de cliente completo
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Debes iniciar sesión para acceder a esta página.')
                return redirect('login')

            if request.user.is_staff or request.user.is_superuser:
                messages.error(request, 'Los administradores no pueden acceder a las funciones de cliente.')
                return redirect('administracion:dashboard_admin')

            if not hasattr(request.user, 'cliente'):
                messages.warning(request, 'Debes completar tu perfil de cliente para acceder a esta función.')
                return redirect('clientes:crear_perfil_cliente')

            return view_func(request, *args, **kwargs)
        return _wrapped_view

    if function:
        return decorator(function)
    return decorator

def administrador_required(function=None):
    """
    Decorador que verifica que el usuario sea administrador (staff)
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('/admin/login/')

            if not (request.user.is_staff or request.user.is_superuser):
                messages.error(request, 'No tienes permisos para acceder a esta página.')
                return redirect('mascotas:lista_mascotas')

            return view_func(request, *args, **kwargs)
        return _wrapped_view

    if function:
        return decorator(function)
    return decorator

def usuario_autenticado_required(function=None):
    """
    Decorador que permite acceso tanto a clientes como a administradores,
    pero requiere autenticación
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Debes iniciar sesión para acceder a esta página.')
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return _wrapped_view

    if function:
        return decorator(function)
    return decorator