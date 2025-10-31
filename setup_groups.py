#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veterinaria_project.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from clientes.models import Cliente
from mascotas.models import Mascota, HistorialMedico, Vacuna
from citas.models import Cita

def setup_groups():
    # Crear grupo de Clientes
    grupo_clientes, created = Group.objects.get_or_create(name='Clientes')

    # Permisos para clientes (solo para sus propios datos)
    content_types = [
        ContentType.objects.get_for_model(Cliente),
        ContentType.objects.get_for_model(Mascota),
        ContentType.objects.get_for_model(HistorialMedico),
        ContentType.objects.get_for_model(Vacuna),
        ContentType.objects.get_for_model(Cita),
    ]

    # Asignar permisos básicos (esto es solo para el ORM, la lógica real está en las vistas)
    for content_type in content_types:
        permisos = Permission.objects.filter(content_type=content_type, codename__in=['add', 'change', 'view'])
        grupo_clientes.permissions.add(*permisos)

    print("Grupo 'Clientes' configurado correctamente.")

    # Crear grupo de Veterinarios
    grupo_veterinarios, created = Group.objects.get_or_create(name='Veterinarios')

    # Permisos para veterinarios (pueden gestionar mascotas, historial médico, citas, etc.)
    permisos_veterinarios = []
    for content_type in content_types:
        # Veterinarios pueden ver, agregar y cambiar (pero no eliminar) registros médicos
        permisos = Permission.objects.filter(
            content_type=content_type,
            codename__in=['add', 'change', 'view', 'delete']
        )
        permisos_veterinarios.extend(permisos)

    grupo_veterinarios.permissions.add(*permisos_veterinarios)
    print("Grupo 'Veterinarios' configurado correctamente.")

    # Crear grupo de Administradores si no existe
    Group.objects.get_or_create(name='Administradores')
    print("Grupo 'Administradores' configurado correctamente.")

if __name__ == '__main__':
    setup_groups()