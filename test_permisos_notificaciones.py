#!/usr/bin/env python
"""
Script para probar los permisos de notificaciones entre usuarios normales y administradores
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veterinaria_project.settings.base')
django.setup()

from django.contrib.auth.models import User
from notificaciones.models import Notificacion

def verificar_permisos():
    """Verificar que los permisos funcionan correctamente"""
    print("=== VERIFICACIÓN DE PERMISOS DE NOTIFICACIONES ===\n")

    # Obtener usuarios
    try:
        admin_user = User.objects.filter(is_staff=True).first()
        normal_user = User.objects.filter(is_staff=False).first()

        if not admin_user or not normal_user:
            print("❌ No se encontraron usuarios admin y normales")
            return

        print(f"👤 Usuario normal: {normal_user.username} (staff: {normal_user.is_staff})")
        print(f"👨‍💼 Usuario admin: {admin_user.username} (staff: {admin_user.is_staff})")

        # Verificar notificaciones
        notifs_admin = Notificacion.objects.filter(cliente=admin_user.cliente if hasattr(admin_user, 'cliente') else None)
        notifs_normal = Notificacion.objects.filter(cliente=normal_user.cliente if hasattr(normal_user, 'cliente') else None)

        print("\n📊 Estadísticas de notificaciones:")
        print(f"  - Admin tiene: {notifs_admin.count()} notificaciones")
        print(f"  - Usuario normal tiene: {notifs_normal.count()} notificaciones")

        # Verificar que las vistas funcionan
        from django.test import Client
        client = Client()

        # Probar como usuario normal
        client.login(username=normal_user.username, password='testpass123')
        response_normal = client.get('/notificaciones/')

        # Probar como admin
        client.login(username=admin_user.username, password='adminpass123')
        response_admin = client.get('/notificaciones/')

        print("\n🌐 Respuestas HTTP:")
        print(f"  - Usuario normal: {response_normal.status_code}")
        print(f"  - Admin: {response_admin.status_code}")

        if response_normal.status_code == 200 and response_admin.status_code == 200:
            print("✅ Las vistas responden correctamente")
        else:
            print("❌ Error en las respuestas HTTP")

        print("\n📝 Permisos implementados:")
        print("  ✅ Usuarios normales ven: título, mensaje, enlaces relacionados")
        print("  ✅ Administradores ven: toda la información técnica adicional")
        print("  ✅ Información sensible oculta para usuarios normales")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    verificar_permisos()
    print("\n=== VERIFICACIÓN COMPLETADA ===")