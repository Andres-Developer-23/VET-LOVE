#!/usr/bin/env python
"""
Script para probar el cambio de estado de citas
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
from mascotas.models import Mascota
from citas.models import Cita
from datetime import datetime

def test_cambiar_estado_cita():
    """Probar cambiar el estado de una cita"""
    print("=== PRUEBA DE CAMBIO DE ESTADO DE CITA ===")

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

    # Crear cita de prueba si no existe
    citas = Cita.objects.filter(estado='programada')
    if not citas.exists():
        # Crear cliente y mascota si no existen
        if not Cliente.objects.exists():
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
            mascota = Mascota.objects.create(
                nombre='TestMascota',
                tipo='perro',
                raza='Labrador',
                sexo='macho',
                cliente=cliente
            )
            print("✓ Cliente y mascota de prueba creados")

        cliente = Cliente.objects.first()
        mascota = cliente.mascotas.first()

        # Crear cita
        cita = Cita.objects.create(
            mascota=mascota,
            fecha=datetime.now().replace(hour=10, minute=0),
            tipo='consulta_general',
            motivo='Cita de prueba',
            estado='programada'
        )
        print(f"✓ Cita de prueba creada: ID {cita.id}")
    else:
        cita = citas.first()
        print(f"✓ Usando cita existente: ID {cita.id}")

    # Probar con cliente Django
    client = Client(HTTP_HOST='localhost')

    # Login como admin
    login_success = client.login(username='admin', password='admin123')
    if login_success:
        print("✓ Login como admin exitoso")

        # Probar cambiar estado a confirmado
        response = client.post(f'/administracion/citas/cambiar-estado/{cita.id}/', {
            'estado': 'confirmada'
        })

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✓ Estado cambiado exitosamente a 'confirmada'")
                print(f"  Mensaje: {data.get('mensaje')}")

                # Verificar que se creó la notificación
                from notificaciones.models import Notificacion
                notifs = Notificacion.objects.filter(
                    cliente=cita.mascota.cliente,
                    tipo='cita'
                ).order_by('-fecha_creacion')[:1]

                if notifs.exists():
                    notif = notifs.first()
                    print(f"✓ Notificación creada: {notif.titulo}")
                else:
                    print("❌ No se creó la notificación")

                # Probar cambiar a completada
                response2 = client.post(f'/administracion/citas/cambiar-estado/{cita.id}/', {
                    'estado': 'completada'
                })

                if response2.status_code == 200:
                    data2 = response2.json()
                    if data2.get('success'):
                        print("✓ Estado cambiado exitosamente a 'completada'")
                    else:
                        print(f"❌ Error al cambiar a completada: {data2.get('error')}")
                else:
                    print(f"❌ Error HTTP al cambiar a completada: {response2.status_code}")

            else:
                print(f"❌ Error al cambiar estado: {data.get('error')}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"Contenido: {response.content.decode()[:200]}")

    else:
        print("❌ Error en login como admin")

def main():
    """Función principal"""
    try:
        test_cambiar_estado_cita()
        print("\n=== PRUEBA COMPLETADA ===")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()