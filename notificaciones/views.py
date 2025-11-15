from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Notificacion, Recordatorio
from clientes.models import Cliente

@login_required
def lista_notificaciones(request):
    """Vista para mostrar la lista de notificaciones del usuario"""
    from django.contrib.auth.models import Group
    from django.db.models import Q

    # Verificar si es veterinario
    if request.user.groups.filter(name='Veterinarios').exists():
        try:
            veterinario = request.user.perfil_veterinario_app
            notificaciones = Notificacion.objects.filter(
                Q(veterinario=veterinario) | Q(para_admin=True) if request.user.is_staff or request.user.is_superuser else Q(veterinario=veterinario)
            ).order_by('-fecha_creacion')
        except AttributeError:
            messages.error(request, "No se encontró información de veterinario asociada a tu cuenta.")
            return redirect('home')
    else:
        try:
            cliente = request.user.cliente
            notificaciones = Notificacion.objects.filter(
                Q(cliente=cliente) | Q(para_admin=True) if request.user.is_staff or request.user.is_superuser else Q(cliente=cliente)
            ).order_by('-fecha_creacion')
        except Cliente.DoesNotExist:
            messages.error(request, "No se encontró información de cliente asociada a tu cuenta.")
            return redirect('home')

    notificaciones_no_leidas = notificaciones.filter(leida=False)

    # Marcar todas como leídas si se solicita
    if request.GET.get('marcar_leidas'):
        notificaciones_no_leidas.update(leida=True)
        messages.success(request, "Todas las notificaciones han sido marcadas como leídas.")
        return redirect('notificaciones:lista')

    context = {
        'notificaciones': notificaciones,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'total_no_leidas': notificaciones_no_leidas.count(),
    }

    return render(request, 'notificaciones/lista_notificaciones.html', context)

@login_required
@require_POST
def marcar_leida(request, notificacion_id):
    """Vista para marcar una notificación como leída (AJAX)"""
    from django.contrib.auth.models import Group
    from django.db.models import Q

    try:
        if request.user.groups.filter(name='Veterinarios').exists():
            veterinario = request.user.perfil_veterinario_app
            notificaciones_queryset = Notificacion.objects.filter(
                Q(veterinario=veterinario) | Q(para_admin=True) if request.user.is_staff or request.user.is_superuser else Q(veterinario=veterinario)
            )
            notificacion = get_object_or_404(notificaciones_queryset, id=notificacion_id)
            notificacion.marcar_como_leida()

            total_no_leidas = Notificacion.objects.filter(
                Q(veterinario=veterinario) | Q(para_admin=True) if request.user.is_staff or request.user.is_superuser else Q(veterinario=veterinario),
                leida=False
            ).count()

            return JsonResponse({
                'success': True,
                'total_no_leidas': total_no_leidas
            })
        else:
            cliente = request.user.cliente
            notificaciones_queryset = Notificacion.objects.filter(
                Q(cliente=cliente) | Q(para_admin=True) if request.user.is_staff or request.user.is_superuser else Q(cliente=cliente)
            )
            notificacion = get_object_or_404(notificaciones_queryset, id=notificacion_id)
            notificacion.marcar_como_leida()

            total_no_leidas = Notificacion.objects.filter(
                Q(cliente=cliente) | Q(para_admin=True) if request.user.is_staff or request.user.is_superuser else Q(cliente=cliente),
                leida=False
            ).count()

            return JsonResponse({
                'success': True,
                'total_no_leidas': total_no_leidas
            })
    except (Cliente.DoesNotExist, AttributeError):
        return JsonResponse({'success': False, 'error': 'Usuario no encontrado'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def lista_recordatorios(request):
    """Vista para mostrar recordatorios activos del usuario"""
    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        messages.error(request, "No se encontró información de cliente asociada a tu cuenta.")
        return redirect('home')

    recordatorios = Recordatorio.objects.filter(
        cliente=cliente,
        activo=True,
        fecha_recordatorio__gte=timezone.now()
    ).order_by('fecha_recordatorio')

    context = {
        'recordatorios': recordatorios,
    }

    return render(request, 'notificaciones/lista_recordatorios.html', context)

@login_required
def detalle_notificacion(request, notificacion_id):
    """Vista para mostrar el detalle de una notificación específica"""
    from django.contrib.auth.models import Group
    from django.db.models import Q

    try:
        if request.user.groups.filter(name='Veterinarios').exists():
            veterinario = request.user.perfil_veterinario_app
            notificaciones_queryset = Notificacion.objects.filter(
                Q(veterinario=veterinario) | Q(para_admin=True) if request.user.is_staff or request.user.is_superuser else Q(veterinario=veterinario)
            )
            notificacion = get_object_or_404(notificaciones_queryset, id=notificacion_id)
        else:
            cliente = request.user.cliente
            notificaciones_queryset = Notificacion.objects.filter(
                Q(cliente=cliente) | Q(para_admin=True) if request.user.is_staff or request.user.is_superuser else Q(cliente=cliente)
            )
            notificacion = get_object_or_404(notificaciones_queryset, id=notificacion_id)

        # Marcar como leída si no lo está
        if not notificacion.leida:
            notificacion.marcar_como_leida()

        context = {
            'notificacion': notificacion,
        }

        return render(request, 'notificaciones/detalle_notificacion.html', context)

    except (Cliente.DoesNotExist, AttributeError):
        messages.error(request, "No se encontró información de usuario asociada a tu cuenta.")
        return redirect('home')

@login_required
def conteo_notificaciones(request):
    """Vista AJAX para obtener el conteo de notificaciones no leídas"""
    from django.contrib.auth.models import Group
    from django.db.models import Q

    try:
        if request.user.groups.filter(name='Veterinarios').exists():
            veterinario = request.user.perfil_veterinario_app
            total_no_leidas = Notificacion.objects.filter(
                Q(veterinario=veterinario) | Q(para_admin=True) if request.user.is_staff or request.user.is_superuser else Q(veterinario=veterinario),
                leida=False
            ).count()
        else:
            cliente = request.user.cliente
            total_no_leidas = Notificacion.objects.filter(
                Q(cliente=cliente) | Q(para_admin=True) if request.user.is_staff or request.user.is_superuser else Q(cliente=cliente),
                leida=False
            ).count()

        return JsonResponse({
            'total_no_leidas': total_no_leidas
        })
    except (Cliente.DoesNotExist, AttributeError):
        return JsonResponse({'total_no_leidas': 0})
    except Exception as e:
        return JsonResponse({'total_no_leidas': 0, 'error': str(e)})
