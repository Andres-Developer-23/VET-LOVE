import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veterinaria_project.settings.development')
django.setup()

from django.contrib.auth.models import User
from django.db.models import Q

print('=== ANÁLISIS DE USUARIOS ===')
print('Total usuarios:', User.objects.count())
print('Usuarios staff:', User.objects.filter(is_staff=True).count())
print('Usuarios veterinarios:', User.objects.filter(groups__name='Veterinarios').count())
print('Usuarios clientes:', User.objects.filter(is_staff=False).exclude(groups__name='Veterinarios').count())

print('\n=== LISTA DE USUARIOS ===')
for u in User.objects.all()[:10]:
    print(f'  {u.username} - {u.get_full_name()} - Staff: {u.is_staff} - Groups: {[g.name for g in u.groups.all()]}')

print('\n=== PRUEBA DE FILTROS ===')
# Simular filtros como en la vista
tipo_filtro = 'todos'
busqueda = 'juan'

usuarios_query = User.objects.select_related()

# Aplicar filtros
if tipo_filtro == 'staff':
    usuarios_query = usuarios_query.filter(is_staff=True)
elif tipo_filtro == 'veterinarios':
    usuarios_query = usuarios_query.filter(groups__name='Veterinarios')
elif tipo_filtro == 'clientes':
    usuarios_query = usuarios_query.filter(is_staff=False).exclude(groups__name='Veterinarios')

if busqueda:
    usuarios_query = usuarios_query.filter(
        Q(username__icontains=busqueda) |
        Q(first_name__icontains=busqueda) |
        Q(last_name__icontains=busqueda) |
        Q(email__icontains=busqueda)
    )

print(f'Usuarios con filtro tipo="{tipo_filtro}" y busqueda="{busqueda}": {usuarios_query.count()}')
for u in usuarios_query[:5]:
    print(f'  {u.username} - {u.get_full_name()}')

print('\n=== PRUEBA SIN FILTROS ===')
usuarios_sin_filtro = User.objects.all()
print(f'Todos los usuarios sin filtros: {usuarios_sin_filtro.count()}')
for u in usuarios_sin_filtro[:5]:
    print(f'  {u.username} - {u.get_full_name()}')

print('\n=== SIMULACIÓN DE LA URL DEL USUARIO ===')
# Simular exactamente lo que recibe la vista desde la URL
# http://127.0.0.1:8000/administracion/dashboard/?tipo=todos&estado=todos&busqueda=juan

from django.http import QueryDict
from django.test import RequestFactory

# Crear una request simulada
factory = RequestFactory()
request = factory.get('/administracion/dashboard/?tipo=todos&estado=todos&busqueda=juan')

print(f'Parámetros GET: {dict(request.GET)}')

# Simular la lógica exacta de la vista gestionar_usuarios
tipo_filtro = request.GET.get('tipo', 'todos')
busqueda = request.GET.get('busqueda', '')
estado_filtro = request.GET.get('estado', 'todos')

print(f'tipo_filtro: "{tipo_filtro}"')
print(f'busqueda: "{busqueda}"')
print(f'estado_filtro: "{estado_filtro}"')

usuarios_query = User.objects.select_related()

# Aplicar filtros exactamente como en la vista
if tipo_filtro == 'staff':
    usuarios_query = usuarios_query.filter(is_staff=True)
elif tipo_filtro == 'veterinarios':
    usuarios_query = usuarios_query.filter(groups__name='Veterinarios')
elif tipo_filtro == 'clientes':
    usuarios_query = usuarios_query.filter(is_staff=False).exclude(groups__name='Veterinarios')

if estado_filtro == 'activos':
    usuarios_query = usuarios_query.filter(is_active=True)
elif estado_filtro == 'inactivos':
    usuarios_query = usuarios_query.filter(is_active=False)

if busqueda:
    usuarios_query = usuarios_query.filter(
        Q(username__icontains=busqueda) |
        Q(first_name__icontains=busqueda) |
        Q(last_name__icontains=busqueda) |
        Q(email__icontains=busqueda)
    )

print(f'Usuarios encontrados con filtros aplicados: {usuarios_query.count()}')
for u in usuarios_query[:5]:
    print(f'  {u.username} - {u.get_full_name()} - Email: {u.email}')