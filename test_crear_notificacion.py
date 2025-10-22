#!/usr/bin/env python
"""
Script para probar la funcionalidad de crear notificaciones
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veterinaria_project.settings.base')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from clientes.models import Cliente
from notificaciones.models import Notificacion

def test_crear_notificacion_cliente():
    """Probar crear notificación para un cliente específico"""
    print("=== Probando creación de notificación para cliente específico ===")

    # Crear cliente de prueba si no existe
    try:
        user = User.objects.get(username='testuser')
        cliente = user.cliente
    except:
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Usuario',
            last_name='Prueba'
        )
        cliente = Cliente.objects.create(
            usuario=user,
            telefono='123456789',
            direccion='Dirección de prueba'
        )

    print(f"Cliente de prueba: {cliente}")

    # Contar notificaciones antes
    notifs_antes = Notificacion.objects.filter(cliente=cliente).count()
    print(f"Notificaciones antes: {notifs_antes}")

    # Crear notificación usando el cliente de Django
    client = Client()
    admin_user = User.objects.filter(is_staff=True).first()
    if admin_user:
        client.force_login(admin_user)

        response = client.post('/administracion/notificaciones/crear/', {
            'destinatario': 'cliente',
            'cliente': cliente.id,
            'tipo': 'general',
            'titulo': 'Notificación de prueba para cliente',
            'mensaje': 'Esta es una notificación de prueba enviada a un cliente específico.',
            'prioridad': 'normal',
            'url_relacionada': ''
        })

        print(f"Respuesta HTTP: {response.status_code}")
        if response.status_code == 302:  # Redirección exitosa
            print("✅ Notificación creada exitosamente")
        else:
            print(f"❌ Error al crear notificación: {response.content.decode()}")

        # Contar notificaciones después
        notifs_despues = Notificacion.objects.filter(cliente=cliente).count()
        print(f"Notificaciones después: {notifs_despues}")

        # Verificar que se creó
        if notifs_despues > notifs_antes:
            nueva_notif = Notificacion.objects.filter(cliente=cliente).order_by('-fecha_creacion').first()
            print(f"✅ Nueva notificación: {nueva_notif.titulo}")
        else:
            print("❌ No se creó la notificación")
    else:
        print("❌ No hay usuario administrador disponible")

def test_crear_notificacion_global():
    """Probar crear notificación global para todos los usuarios"""
    print("\n=== Probando creación de notificación global ===")

    # Contar notificaciones globales antes
    global_antes = Notificacion.objects.filter(cliente__isnull=True).count()
    print(f"Notificaciones globales antes: {global_antes}")

    # Crear notificación global
    client = Client()
    admin_user = User.objects.filter(is_staff=True).first()
    if admin_user:
        client.force_login(admin_user)

        response = client.post('/administracion/notificaciones/crear/', {
            'destinatario': 'todos',
            'tipo': 'sistema',
            'titulo': 'Notificación global de prueba',
            'mensaje': 'Esta es una notificación global enviada a todos los usuarios del sistema.',
            'prioridad': 'alta',
            'url_relacionada': '/'
        })

        print(f"Respuesta HTTP: {response.status_code}")
        if response.status_code == 302:  # Redirección exitosa
            print("✅ Notificación global creada exitosamente")
        else:
            print(f"❌ Error al crear notificación global: {response.content.decode()}")

        # Contar notificaciones globales después
        global_despues = Notificacion.objects.filter(cliente__isnull=True).count()
        print(f"Notificaciones globales después: {global_despues}")

        # Verificar que se creó
        if global_despues > global_antes:
            nueva_global = Notificacion.objects.filter(cliente__isnull=True).order_by('-fecha_creacion').first()
            print(f"✅ Nueva notificación global: {nueva_global.titulo}")
        else:
            print("❌ No se creó la notificación global")
    else:
        print("❌ No hay usuario administrador disponible")

def test_formulario_get():
    """Probar que el formulario se carga correctamente"""
    print("\n=== Probando carga del formulario ===")

    client = Client()
    admin_user = User.objects.filter(is_staff=True).first()
    if admin_user:
        client.force_login(admin_user)

        response = client.get('/administracion/notificaciones/crear/')
        print(f"Respuesta GET: {response.status_code}")

        if 'destinatario' in response.content.decode():
            print("✅ Formulario contiene campo destinatario")
        else:
            print("❌ Formulario no contiene campo destinatario")

        if 'Cliente Específico' in response.content.decode():
            print("✅ Formulario contiene campo cliente")
        else:
            print("❌ Formulario no contiene campo cliente")
    else:
        print("❌ No hay usuario administrador disponible")

def main():
    """Función principal"""
    print("=== PRUEBA DE CREACIÓN DE NOTIFICACIONES ===\n")

    try:
        test_formulario_get()
        test_crear_notificacion_cliente()
        test_crear_notificacion_global()

        print("\n=== PRUEBA COMPLETADA ===")
        print("Verifica en el navegador que las notificaciones aparecen correctamente.")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()