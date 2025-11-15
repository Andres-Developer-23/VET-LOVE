from notificaciones.models import Notificacion

def notificaciones_admin(request):
    """Context processor para agregar notificaciones al admin"""
    if request.path.startswith('/admin/') and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        notificaciones_recientes = Notificacion.objects.filter(
            para_admin=True
        ).order_by('-fecha_creacion')[:10]  # Últimas 10
        return {
            'notificaciones_recientes': notificaciones_recientes,
        }
    return {}