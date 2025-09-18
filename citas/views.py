from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import CitaForm
from .models import Cita
from mascotas.models import Mascota

@login_required
def solicitar_cita(request):
    if not hasattr(request.user, 'cliente'):
        messages.warning(request, 'Debes completar tu perfil antes de solicitar una cita.')
        return redirect('clientes:crear_perfil_cliente')
    
    # Verificar si el usuario tiene mascotas
    mascotas = Mascota.objects.filter(cliente=request.user.cliente)
    if not mascotas.exists():
        messages.warning(request, 'Debes agregar al menos una mascota antes de solicitar una cita.')
        return redirect('mascotas:agregar_mascota')
    
    if request.method == 'POST':
        form = CitaForm(request.POST, user=request.user)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.mascota = form.cleaned_data['mascota']
            cita.estado = 'programada'
            cita.save()
            messages.success(request, '¡Cita agendada correctamente!')
            return redirect('citas:mis_citas')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        # Establecer fecha predeterminada (próxima media hora)
        ahora = timezone.now()
        minutos = 30 - (ahora.minute % 30)
        fecha_predeterminada = ahora.replace(second=0, microsecond=0) + timezone.timedelta(minutes=minutos)
        form = CitaForm(initial={'fecha': fecha_predeterminada}, user=request.user)
    
    return render(request, 'citas/solicitar_cita.html', {
        'form': form,
        'mascotas': mascotas
    })

@login_required
def mis_citas(request):
    citas = None
    if hasattr(request.user, 'cliente'):
        mascotas = Mascota.objects.filter(cliente=request.user.cliente)
        citas = Cita.objects.filter(mascota__in=mascotas).order_by('-fecha')
    
    return render(request, 'citas/mis_citas.html', {
        'citas': citas,
        'tiene_perfil': hasattr(request.user, 'cliente')
    })

@login_required
def cancelar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    
    # Verificar que el usuario es el dueño de la mascota
    if not hasattr(request.user, 'cliente') or cita.mascota.cliente != request.user.cliente:
        messages.error(request, 'No tienes permiso para cancelar esta cita.')
        return redirect('citas:mis_citas')
    
    if cita.puede_ser_cancelada():
        cita.estado = 'cancelada'
        cita.save()
        messages.success(request, 'Cita cancelada correctamente.')
    else:
        messages.error(request, 'No se puede cancelar una cita en su estado actual.')
    
    return redirect('citas:mis_citas')