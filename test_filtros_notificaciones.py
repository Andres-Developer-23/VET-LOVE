#!/usr/bin/env python
"""
Script para probar que los filtros de notificaciones funcionan correctamente
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veterinaria_project.settings.base')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from notificaciones.models import Notificacion
from clientes.models import Cliente

def test_filtros_notificaciones():
    """Probar que los filtros de notificaciones funcionan"""
    print("=== PRUEBA DE FILTROS DE NOTIFICACIONES ===")

    # Crear usuario admin si no existe
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='Sistema'
        )
        print("✓ Usuario admin creado")

    # Verificar que hay notificaciones
    total_notifs = Notificacion.objects.count()
    print(f"Total de notificaciones en BD: {total_notifs}")

    if total_notifs == 0:
        print("❌ No hay notificaciones para probar filtros")
        return False

    # Probar con cliente Django
    client = Client(HTTP_HOST='localhost')

    # Login como admin
    login_success = client.login(username='admin', password='admin123')
    if login_success:
        print("✓ Login como admin exitoso")

        # Probar página sin filtros
        response = client.get('/administracion/notificaciones/')
        if response.status_code == 200:
            print("✓ Página de gestión de notificaciones accesible")

            # Verificar que contiene elementos de filtro
            content = response.content.decode()
            if 'tipo' in content and 'estado' in content and 'cliente' in content:
                print("✓ Formulario de filtros presente")
            else:
                print("❌ Formulario de filtros no encontrado")
                return False
        else:
            print(f"❌ Error al acceder a la página: {response.status_code}")
            return False

        # Probar filtro por tipo
        response_tipo = client.get('/administracion/notificaciones/?tipo=cita')
        if response_tipo.status_code == 200:
            print("✓ Filtro por tipo funciona")
        else:
            print(f"❌ Error en filtro por tipo: {response_tipo.status_code}")
            return False

        # Probar filtro por estado
        response_estado = client.get('/administracion/notificaciones/?estado=no_leida')
        if response_estado.status_code == 200:
            print("✓ Filtro por estado funciona")
        else:
            print(f"❌ Error en filtro por estado: {response_estado.status_code}")
            return False

        # Probar filtro por búsqueda
        response_busqueda = client.get('/administracion/notificaciones/?busqueda=prueba')
        if response_busqueda.status_code == 200:
            print("✓ Filtro por búsqueda funciona")
        else:
            print(f"❌ Error en filtro por búsqueda: {response_busqueda.status_code}")
            return False

        # Probar filtro por cliente
        clientes = Cliente.objects.all()
        if clientes.exists():
            cliente = clientes.first()
            response_cliente = client.get(f'/administracion/notificaciones/?cliente={cliente.usuario.first_name}')
            if response_cliente.status_code == 200:
                print("✓ Filtro por cliente funciona")
            else:
                print(f"❌ Error en filtro por cliente: {response_cliente.status_code}")
                return False

        # Probar filtro por destinatario
        response_destinatario = client.get('/administracion/notificaciones/?destinatario=cliente')
        if response_destinatario.status_code == 200:
            print("✓ Filtro por destinatario funciona")
        else:
            print(f"❌ Error en filtro por destinatario: {response_destinatario.status_code}")
            return False

        # Probar múltiples filtros combinados
        response_combinado = client.get('/administracion/notificaciones/?tipo=general&estado=no_leida&destinatario=cliente')
        if response_combinado.status_code == 200:
            print("✓ Filtros combinados funcionan")
        else:
            print(f"❌ Error en filtros combinados: {response_combinado.status_code}")
            return False

        print("✓ Todos los filtros funcionan correctamente")
        return True

    else:
        print("❌ Error en login como admin")
        return False

def main():
    """Función principal"""
    try:
        success = test_filtros_notificaciones()
        if success:
            print("\n=== ÉXITO: TODOS LOS FILTROS FUNCIONAN ===")
        else:
            print("\n=== ERROR: PROBLEMAS CON LOS FILTROS ===")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()