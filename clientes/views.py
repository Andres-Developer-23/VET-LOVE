from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserForm, ClienteForm
from .models import Cliente
from mascotas.models import Mascota
from citas.models import Cita
from mascotas.models import Vacuna

@login_required
def perfil_cliente(request):
    try:
        cliente = request.user.cliente
    except:
        return redirect('clientes:crear_perfil')
    
    # Obtener estadísticas para el perfil
    mascotas_count = Mascota.objects.filter(cliente=cliente).count()
    citas_count = Cita.objects.filter(mascota__cliente=cliente).count()
    vacunas_count = Vacuna.objects.filter(mascota__cliente=cliente).count()
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        cliente_form = ClienteForm(request.POST, request.FILES, instance=cliente)
        
        if user_form.is_valid() and cliente_form.is_valid():
            user_form.save()
            cliente_form.save()
            messages.success(request, 'Tu perfil ha sido actualizado correctamente.')
            return redirect('clientes:perfil_cliente')
    else:
        user_form = UserForm(instance=request.user)
        cliente_form = ClienteForm(instance=cliente)
    
    return render(request, 'clientes/perfil.html', {
        'user_form': user_form,
        'cliente_form': cliente_form,
        'cliente': cliente,
        'mascotas_count': mascotas_count,
        'citas_count': citas_count,
        'vacunas_count': vacunas_count,
    })

@login_required
def crear_perfil_cliente(request):
    if hasattr(request.user, 'cliente'):
        return redirect('clientes:perfil_cliente')
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        cliente_form = ClienteForm(request.POST, request.FILES)
        
        if user_form.is_valid() and cliente_form.is_valid():
            user_form.save()
            cliente = cliente_form.save(commit=False)
            cliente.usuario = request.user
            cliente.save()
            messages.success(request, 'Perfil creado correctamente.')
            return redirect('clientes:perfil_cliente')
    else:
        user_form = UserForm(instance=request.user)
        cliente_form = ClienteForm()
    
    return render(request, 'clientes/crear_perfil.html', {
        'user_form': user_form,
        'cliente_form': cliente_form
    })