from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .forms import CitaForm
from .models import Cita
from mascotas.models import Mascota

def solicitar_cita(request):
    # Verificar que el usuario tenga perfil de cliente
    if not hasattr(request.user, 'cliente'):
        messages.warning(request, 'Debes completar tu perfil de cliente antes de solicitar una cita.')
        return redirect('clientes:crear_perfil_cliente')
    
    # Verificar si el usuario tiene mascotas
    mascotas = Mascota.objects.filter(cliente=request.user.cliente)
    if not mascotas.exists():
        messages.warning(request, 'Debes agregar al menos una mascota antes de solicitar una cita.')
        return redirect('mascotas:agregar_mascota')
    
    if request.method == 'POST':
        form = CitaForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                cita = form.save(commit=False)
                cita.mascota = form.cleaned_data['mascota']
                cita.estado = 'confirmada'  # Cambiar a 'confirmada' directamente desde el modal
                cita.confirmada_por_cliente = True  # Marcar como confirmada por el cliente
                
                # Calcular duración estimada basada en el tipo de cita
                duraciones = {
                    'consulta_general': 30,
                    'vacunacion': 20,
                    'desparasitacion': 15,
                    'urgencia': 60,
                    'cirugia': 120,
                    'estetica': 90,
                    'odontologia': 45,
                    'analisis': 30,
                    'radiologia': 40,
                    'ecografia': 50,
                    'control': 20,
                    'comportamiento': 60,
                    'nutricion': 40,
                }
                cita.duracion_estimada = duraciones.get(cita.tipo, 30)
                
                cita.save()
                
                messages.success(request, 
                    f'¡Cita confirmada correctamente para {cita.mascota.nombre}! '
                    f'Recibirás un correo de confirmación pronto. '
                    f'Fecha: {cita.fecha.strftime("%d/%m/%Y a las %H:%M")}'
                )
                return redirect('citas:mis_citas')
            except Exception as e:
                messages.error(request, f'Error al guardar la cita: {str(e)}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        # Establecer fecha predeterminada (próxima hora en punto)
        ahora = timezone.now()
        siguiente_hora = ahora.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        form = CitaForm(initial={'fecha': siguiente_hora}, user=request.user)
    
    return render(request, 'citas/solicitar_cita.html', {
        'form': form,
        'mascotas': mascotas  # Pasar las mascotas al template para mostrar información
    })

def mis_citas(request):
    # Verificar que el usuario tenga perfil de cliente
    if not hasattr(request.user, 'cliente'):
        messages.warning(request, 'Debes completar tu perfil de cliente para ver tus citas.')
        return redirect('clientes:crear_perfil_cliente')
    
    # Administradores pueden ver todas las citas, clientes solo las suyas
    es_admin = request.user.is_staff or request.user.is_superuser
    
    try:
        if es_admin:
            citas = Cita.objects.all().select_related('mascota__cliente__usuario').order_by('-fecha')
        else:
            mascotas = Mascota.objects.filter(cliente=request.user.cliente)
            citas = Cita.objects.filter(mascota__in=mascotas).order_by('-fecha')
    except Exception as e:
        # Si hay error por campos faltantes, mostrar página sin citas
        messages.error(request, 'Error al cargar las citas. Por favor, contacta al administrador.')
        citas = []

    return render(request, 'citas/mis_citas.html', {
        'citas': citas,
        'tiene_perfil': True,
        'es_admin': es_admin
    })

def cancelar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)

    # Verificar permisos: administradores pueden cancelar todas, clientes solo las suyas
    es_admin = request.user.is_staff or request.user.is_superuser
    if not es_admin:
        if not hasattr(request.user, 'cliente') or cita.mascota.cliente != request.user.cliente:
            messages.error(request, 'No tienes permiso para cancelar esta cita.')
            return redirect('citas:mis_citas')

    if cita.puede_ser_cancelada():
        cita.estado = 'cancelada'
        cita.save()
        messages.success(request, 'Cita cancelada correctamente.')
    else:
        messages.error(request, 'No se puede cancelar una cita en su estado actual.')

from django.http import JsonResponse

@login_required
def cambiar_estado_cita(request, cita_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'})

    try:
        cita = get_object_or_404(Cita, id=cita_id)

        # Verificar permisos: solo administradores pueden cambiar estado
        if not request.user.is_staff:
            return JsonResponse({'success': False, 'error': 'No tienes permisos para realizar esta acción'})

        nuevo_estado = request.POST.get('estado') or request.GET.get('estado')
        if not nuevo_estado:
            return JsonResponse({'success': False, 'error': 'Estado no especificado'})

        # Validar que el estado sea válido
        estados_validos = ['programada', 'confirmada', 'completada', 'cancelada']
        if nuevo_estado not in estados_validos:
            return JsonResponse({'success': False, 'error': 'Estado no válido'})

        # Cambiar el estado
        cita.estado = nuevo_estado
        cita.save()

        return JsonResponse({
            'success': True,
            'mensaje': f'Cita cambiada a {nuevo_estado} correctamente'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

# Eliminamos la vista confirmar_cita ya que no es necesaria
# porque las citas se confirman directamente desde el modal