#!/usr/bin/env python
"""
Script para probar que los botones de notificaciones funcionan correctamente
"""
import os
import sys
import django
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veterinaria_project.settings.base')
django.setup()

from clientes.models import Cliente
from notificaciones.models import Notificacion

def test_boton_crear_notificacion():
    """Probar que el botón de crear notificación funciona"""
    print("=== PRUEBA DEL BOTÓN CREAR NOTIFICACIÓN ===")

    # Crear cliente de prueba si no existe
    if not User.objects.filter(username='testuser').exists():
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Usuario',
            last_name='Prueba'
        )
        Cliente.objects.create(
            usuario=user,
            telefono='123456789',
            direccion='Dirección de prueba'
        )
        print("✓ Usuario y cliente de prueba creados")

    # Crear cliente admin si no existe
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='Sistema'
        )
        print("✓ Usuario admin creado")

    # Probar con cliente Django test
    from django.test import Client
    client = Client()

    # Login como admin
    login_success = client.login(username='admin', password='admin123')
    if login_success:
        print("✓ Login como admin exitoso")

        # Probar acceder a la página de crear notificación
        try:
            response = client.get('/administracion/notificaciones/crear/')
            if response.status_code == 200:
                print("✓ Página de crear notificación accesible")

                # Verificar que contiene el formulario
                if 'Destinatario' in response.content.decode():
                    print("✓ Formulario contiene campo Destinatario")
                else:
                    print("❌ Formulario no contiene campo Destinatario")

                if 'Cliente Específico' in response.content.decode():
                    print("✓ Formulario contiene campo Cliente")
                else:
                    print("❌ Formulario no contiene campo Cliente")

                # Probar enviar formulario
                cliente = Cliente.objects.first()
                if cliente:
                    data = {
                        'destinatario': 'cliente',
                        'cliente': cliente.id,
                        'tipo': 'general',
                        'titulo': 'Notificación de prueba',
                        'mensaje': 'Esta es una notificación de prueba',
                        'prioridad': 'normal',
                        'url_relacionada': ''
                    }

                    response_post = client.post('/administracion/notificaciones/crear/', data)
                    if response_post.status_code == 302:  # Redirección exitosa
                        print("✓ Formulario enviado exitosamente")

                        # Verificar que se creó la notificación
                        notif_count = Notificacion.objects.filter(titulo='Notificación de prueba').count()
                        if notif_count > 0:
                            print(f"✓ Notificación creada correctamente ({notif_count} notificación(es))")
                        else:
                            print("❌ Notificación no se creó")
                    else:
                        print(f"❌ Error al enviar formulario: {response_post.status_code}")
                        print("Contenido:", response_post.content.decode()[:500])
                else:
                    print("❌ No hay clientes disponibles para la prueba")

            else:
                print(f"❌ Error al acceder a la página: {response.status_code}")
                print("Contenido:", response.content.decode()[:500])

        except Exception as e:
            print(f"❌ Error al acceder a la página: {e}")

    else:
        print("❌ Error en login como admin")

def main():
    """Función principal"""
    try:
        test_boton_crear_notificacion()
        print("\n=== PRUEBA COMPLETADA ===")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()