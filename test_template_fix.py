#!/usr/bin/env python
"""
Script para verificar que los templates funcionan correctamente
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veterinaria_project.settings.base')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_template_access():
    """Probar que los templates se cargan correctamente"""
    print("=== PRUEBA DE ACCESO A TEMPLATES ===")

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

    # Probar con cliente Django configurado para testing
    client = Client(HTTP_HOST='localhost')

    # Login como admin
    login_success = client.login(username='admin', password='admin123')
    if login_success:
        print("✓ Login como admin exitoso")

        # Probar acceder al dashboard
        try:
            response = client.get('/administracion/dashboard/')
            if response.status_code == 200:
                print("✓ Dashboard accesible")
            else:
                print(f"❌ Error en dashboard: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error accediendo al dashboard: {e}")
            return False

        # Probar acceder a crear notificación
        try:
            response = client.get('/administracion/notificaciones/crear/')
            if response.status_code == 200:
                print("✓ Página de crear notificación accesible")
                if 'Destinatario' in response.content.decode():
                    print("✓ Template contiene formulario correcto")
                else:
                    print("❌ Template no contiene formulario esperado")
                    return False
            else:
                print(f"❌ Error en crear notificación: {response.status_code}")
                print("Contenido:", response.content.decode()[:200])
                return False
        except Exception as e:
            print(f"❌ Error accediendo a crear notificación: {e}")
            return False

        # Probar acceder a gestión de notificaciones
        try:
            response = client.get('/administracion/notificaciones/')
            if response.status_code == 200:
                print("✓ Página de gestión de notificaciones accesible")
            else:
                print(f"❌ Error en gestión de notificaciones: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error accediendo a gestión de notificaciones: {e}")
            return False

        print("✓ Todos los templates funcionan correctamente")
        return True

    else:
        print("❌ Error en login como admin")
        return False

if __name__ == '__main__':
    success = test_template_access()
    if success:
        print("\n=== ÉXITO: TODOS LOS TEMPLATES FUNCIONAN ===")
        sys.exit(0)
    else:
        print("\n=== ERROR: PROBLEMAS CON LOS TEMPLATES ===")
        sys.exit(1)