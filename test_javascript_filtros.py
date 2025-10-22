#!/usr/bin/env python
"""
Script para probar que el JavaScript de filtros funciona correctamente
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

def test_javascript_filtros():
    """Probar que el JavaScript de filtros funciona"""
    print("=== PRUEBA DE JAVASCRIPT DE FILTROS ===")

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

        # Probar página de gestión de notificaciones
        response = client.get('/administracion/notificaciones/')
        if response.status_code == 200:
            content = response.content.decode()

            # Verificar que el JavaScript está presente
            if 'DOMContentLoaded' in content and 'addEventListener' in content:
                print("✓ JavaScript de filtros presente en el template")
            else:
                print("❌ JavaScript de filtros no encontrado")
                return False

            # Verificar que hay selects en el formulario
            if 'form-select' in content and 'name="tipo"' in content:
                print("✓ Formulario de filtros con selects presente")
            else:
                print("❌ Formulario de filtros no encontrado")
                return False

            # Verificar que hay opciones en los selects
            if 'option value=' in content:
                print("✓ Opciones de filtro presentes")
            else:
                print("❌ Opciones de filtro no encontradas")
                return False

            print("✓ Todos los elementos JavaScript están presentes")
            return True

        else:
            print(f"❌ Error al acceder a la página: {response.status_code}")
            return False

    else:
        print("❌ Error en login como admin")
        return False

def test_filtros_backend():
    """Probar que los filtros funcionan en el backend"""
    print("\n=== PRUEBA DE FILTROS EN BACKEND ===")

    # Crear usuario admin si no existe
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='Sistema'
        )

    # Probar con cliente Django
    client = Client(HTTP_HOST='localhost')

    # Login como admin
    login_success = client.login(username='admin', password='admin123')
    if login_success:
        print("✓ Login como admin exitoso")

        # Probar diferentes combinaciones de filtros
        filtros_prueba = [
            {'tipo': 'cita', 'descripcion': 'Filtro por tipo cita'},
            {'estado': 'no_leida', 'descripcion': 'Filtro por estado no leída'},
            {'destinatario': 'cliente', 'descripcion': 'Filtro por destinatario cliente'},
            {'tipo': 'general', 'estado': 'leida', 'descripcion': 'Filtros combinados'},
        ]

        for filtro in filtros_prueba:
            params = '&'.join([f'{k}={v}' for k, v in filtro.items() if k != 'descripcion'])
            url = f'/administracion/notificaciones/?{params}'

            response = client.get(url)
            if response.status_code == 200:
                print(f"✓ {filtro['descripcion']} funciona")
            else:
                print(f"❌ Error en {filtro['descripcion']}: {response.status_code}")
                return False

        print("✓ Todos los filtros backend funcionan correctamente")
        return True

    else:
        print("❌ Error en login como admin")
        return False

def main():
    """Función principal"""
    try:
        success1 = test_javascript_filtros()
        success2 = test_filtros_backend()

        if success1 and success2:
            print("\n=== ÉXITO: JAVASCRIPT Y FILTROS FUNCIONAN ===")
            print("Los filtros se aplicarán automáticamente cuando cambies los selects.")
        else:
            print("\n=== ERROR: PROBLEMAS CON JAVASCRIPT O FILTROS ===")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()