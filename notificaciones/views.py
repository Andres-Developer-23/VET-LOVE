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
    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        messages.error(request, "No se encontró información de cliente asociada a tu cuenta.")
        return redirect('home')

    notificaciones = Notificacion.objects.filter(cliente=cliente).order_by('-fecha_creacion')
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
    try:
        cliente = request.user.cliente
        notificacion = get_object_or_404(Notificacion, id=notificacion_id, cliente=cliente)
        notificacion.marcar_como_leida()

        return JsonResponse({
            'success': True,
            'total_no_leidas': Notificacion.objects.filter(cliente=cliente, leida=False).count()
        })
    except Cliente.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Cliente no encontrado'})
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
    try:
        cliente = request.user.cliente
        notificacion = get_object_or_404(Notificacion, id=notificacion_id, cliente=cliente)

        # Marcar como leída si no lo está
        if not notificacion.leida:
            notificacion.marcar_como_leida()

        context = {
            'notificacion': notificacion,
        }

        return render(request, 'notificaciones/detalle_notificacion.html', context)

    except Cliente.DoesNotExist:
        messages.error(request, "No se encontró información de cliente asociada a tu cuenta.")
        return redirect('home')

@login_required
def conteo_notificaciones(request):
    """Vista AJAX para obtener el conteo de notificaciones no leídas"""
    try:
        cliente = request.user.cliente
        total_no_leidas = Notificacion.objects.filter(cliente=cliente, leida=False).count()

        return JsonResponse({
            'total_no_leidas': total_no_leidas
        })
    except Cliente.DoesNotExist:
        return JsonResponse({'total_no_leidas': 0})
    except Exception as e:
        return JsonResponse({'total_no_leidas': 0, 'error': str(e)})
