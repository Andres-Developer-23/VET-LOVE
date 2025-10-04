from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Mascota, HistorialMedico, Vacuna
from .forms import MascotaForm, HistorialMedicoForm, VacunaForm

@login_required
def lista_mascotas(request):
    if not hasattr(request.user, 'cliente'):
        return render(request, 'mascotas/lista_mascotas.html', {
            'mascotas': None,
            'es_cliente': False
        })
    
    try:
        cliente = request.user.cliente
        mascotas = Mascota.objects.filter(cliente=cliente)
        return render(request, 'mascotas/lista_mascotas.html', {
            'mascotas': mascotas,
            'es_cliente': True
        })
    except Exception as e:
        return render(request, 'mascotas/lista_mascotas.html', {
            'mascotas': None,
            'es_cliente': False,
            'error': str(e)
        })

@login_required
def agregar_mascota(request):
    if not hasattr(request.user, 'cliente'):
        messages.error(request, 'Debes completar tu perfil de cliente antes de agregar una mascota.')
        return redirect('clientes:crear_perfil_cliente')
    
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.cliente = request.user.cliente
            mascota.save()
            messages.success(request, f'{mascota.nombre} ha sido registrado(a) correctamente en el sistema veterinario.')
            return redirect('mascotas:lista_mascotas')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = MascotaForm()
    
    return render(request, 'mascotas/agregar_mascota.html', {
        'form': form,
        'titulo': 'Registro de Nueva Mascota'
    })

@login_required
def detalle_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    
    # Verificar que la mascota pertenece al usuario
    if not hasattr(request.user, 'cliente') or mascota.cliente != request.user.cliente:
        return HttpResponseForbidden("No tienes permiso para ver esta mascota")
    
    historial = mascota.historial_medico.all()
    vacunas = mascota.vacunas.all()
    citas = mascota.citas.all() if hasattr(mascota, 'citas') else []
    
    return render(request, 'mascotas/detalle_mascota.html', {
        'mascota': mascota,
        'historial': historial,
        'vacunas': vacunas,
        'citas': citas
    })

@login_required
def editar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    
    # Verificar que la mascota pertenece al usuario
    if not hasattr(request.user, 'cliente') or mascota.cliente != request.user.cliente:
        return HttpResponseForbidden("No tienes permiso para editar esta mascota")
    
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES, instance=mascota)
        if form.is_valid():
            form.save()
            messages.success(request, f'La información de {mascota.nombre} ha sido actualizada en el sistema.')
            return redirect('mascotas:detalle_mascota', mascota_id=mascota.id)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = MascotaForm(instance=mascota)
    
    return render(request, 'mascotas/editar_mascota.html', {
        'form': form, 
        'mascota': mascota,
        'titulo': 'Editar Información de Mascota'
    })

@login_required
def eliminar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    
    # Verificar que la mascota pertenece al usuario
    if not hasattr(request.user, 'cliente') or mascota.cliente != request.user.cliente:
        return HttpResponseForbidden("No tienes permiso para eliminar esta mascota")
    
    if request.method == 'POST':
        nombre = mascota.nombre
        mascota.delete()
        messages.success(request, f'{nombre} ha sido eliminado(a) del sistema veterinario.')
        return redirect('mascotas:lista_mascotas')
    
    return render(request, 'mascotas/eliminar_mascota.html', {'mascota': mascota})

@login_required
def agregar_historial(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    
    # Verificar que la mascota pertenece al usuario
    if not hasattr(request.user, 'cliente') or mascota.cliente != request.user.cliente:
        return HttpResponseForbidden("No tienes permiso para agregar historial a esta mascota")
    
    if request.method == 'POST':
        form = HistorialMedicoForm(request.POST)
        if form.is_valid():
            historial = form.save(commit=False)
            historial.mascota = mascota
            historial.save()
            messages.success(request, 'El historial médico ha sido registrado correctamente.')
            return redirect('mascotas:detalle_mascota', mascota_id=mascota.id)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = HistorialMedicoForm()
    
    return render(request, 'mascotas/agregar_historial.html', {
        'form': form, 
        'mascota': mascota,
        'titulo': 'Nuevo Registro Médico'
    })

@login_required
def agregar_vacuna(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    
    # Verificar que la mascota pertenece al usuario
    if not hasattr(request.user, 'cliente') or mascota.cliente != request.user.cliente:
        return HttpResponseForbidden("No tienes permiso para agregar vacunas a esta mascota")
    
    if request.method == 'POST':
        form = VacunaForm(request.POST)
        if form.is_valid():
            vacuna = form.save(commit=False)
            vacuna.mascota = mascota
            vacuna.save()
            messages.success(request, 'La vacuna ha sido registrada correctamente en el cartón de vacunación.')
            return redirect('mascotas:detalle_mascota', mascota_id=mascota.id)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = VacunaForm()
    
    return render(request, 'mascotas/agregar_vacuna.html', {
        'form': form, 
        'mascota': mascota,
        'titulo': 'Registrar Nueva Vacuna'
    })