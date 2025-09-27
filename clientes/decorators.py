from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test

def cliente_required(function=None):
    """
    Decorador que verifica que el usuario sea un cliente normal (no staff/admin)
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and not (u.is_staff or u.is_superuser),
        login_url='/accounts/login/'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def administrador_required(function=None):
    """
    Decorador que verifica que el usuario sea administrador
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and (u.is_staff or u.is_superuser),
        login_url='/admin/login/'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator