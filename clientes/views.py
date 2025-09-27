from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import HttpResponseForbidden
from .tokens import account_activation_token
from .forms import UserForm, ClienteForm, CustomUserCreationForm, RegistroClienteForm
from .models import Cliente
from mascotas.models import Mascota
from citas.models import Cita
from mascotas.models import Vacuna

# Función para verificar si un usuario es administrador
def es_administrador(user):
    return user.is_staff or user.is_superuser

# Función para verificar si un usuario es cliente normal
def es_cliente_normal(user):
    return user.is_authenticated and not (user.is_staff or user.is_superuser)

# Vista de registro público
def registro_usuario(request):
    if request.user.is_authenticated:
        messages.info(request, 'Ya tienes una sesión activa.')
        return redirect('home')
    
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        cliente_form = RegistroClienteForm(request.POST)
        
        if user_form.is_valid() and cliente_form.is_valid():
            # Guardar usuario pero no activarlo aún
            user = user_form.save(commit=False)
            user.is_active = False  # El usuario no estará activo hasta confirmar email
            user.is_staff = False   # Asegurar que no sea staff
            user.is_superuser = False  # Asegurar que no sea superusuario
            user.save()
            
            # Asignar al grupo "Clientes" si existe
            try:
                grupo_clientes = Group.objects.get(name='Clientes')
                user.groups.add(grupo_clientes)
            except Group.DoesNotExist:
                # Si el grupo no existe, se crea
                grupo_clientes = Group.objects.create(name='Clientes')
                user.groups.add(grupo_clientes)
            
            # Guardar cliente
            cliente = cliente_form.save(commit=False)
            cliente.usuario = user
            cliente.save()
            
            # Enviar email de confirmación
            current_site = get_current_site(request)
            mail_subject = 'Activa tu cuenta en Veterinaria HappyPets'
            message = render_to_string('clientes/activar_cuenta_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            
            try:
                email.send()
                messages.success(request, 'Por favor, confirma tu email para completar el registro. Te hemos enviado un enlace de activación.')
                return redirect('login')
            except Exception as e:
                # Si falla el envío de email, eliminar el usuario creado
                user.delete()
                messages.error(request, f'Error al enviar el email de confirmación: {str(e)}')
                return redirect('registro_usuario')
    else:
        user_form = CustomUserCreationForm()
        cliente_form = RegistroClienteForm()
    
    return render(request, 'clientes/registro.html', {
        'user_form': user_form,
        'cliente_form': cliente_form
    })

# Vista para activar cuenta
def activar_cuenta(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        # Crear perfil de cliente si no existe
        if not hasattr(user, 'cliente'):
            Cliente.objects.create(
                usuario=user,
                telefono='+000000000',
                direccion='Dirección por definir',
                preferencias_comunicacion='email'
            )
        
        messages.success(request, '¡Tu cuenta ha sido activada! Ahora puedes iniciar sesión.')
        return redirect('login')
    else:
        messages.error(request, 'El enlace de activación es inválido o ha expirado.')
        return redirect('home')

# Vista de perfil del cliente (solo para usuarios normales)
@login_required
def perfil_cliente(request):
    # Verificar que el usuario no sea staff/admin
    if request.user.is_staff or request.user.is_superuser:
        messages.warning(request, 'Los administradores deben usar el panel de administración.')
        return redirect('admin:index')
    
    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        return redirect('clientes:crear_perfil_cliente')
    
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

# Vista para crear perfil de cliente
@login_required
def crear_perfil_cliente(request):
    # Verificar que el usuario no sea staff/admin
    if request.user.is_staff or request.user.is_superuser:
        return HttpResponseForbidden("Los administradores no pueden crear perfiles de cliente.")
    
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