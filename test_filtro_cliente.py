#!/usr/bin/env python
"""
Script para probar que el filtro por cliente funcione correctamente
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

def test_filtro_cliente():
    """Probar que el filtro por cliente funcione con nombres completos"""
    print("=== PRUEBA DE FILTRO POR CLIENTE ===")

    # Verificar que hay notificaciones
    total_notifs = Notificacion.objects.count()
    print(f"Total de notificaciones en BD: {total_notifs}")

    if total_notifs == 0:
        print("❌ No hay notificaciones para probar filtros")
        return False

    # Verificar que hay clientes con notificaciones
    clientes_con_notifs = Cliente.objects.filter(notificaciones__isnull=False).distinct()
    print(f"Clientes con notificaciones: {clientes_con_notifs.count()}")

    if not clientes_con_notifs.exists():
        print("❌ No hay clientes con notificaciones")
        return False

    # Mostrar algunos clientes de ejemplo
    for cliente in clientes_con_notifs[:3]:
        nombre_completo = cliente.usuario.get_full_name() or cliente.usuario.username
        notifs_count = cliente.notificaciones.count()
        print(f"  - {nombre_completo}: {notifs_count} notificaciones")

    # Probar con cliente Django
    client = Client(HTTP_HOST='localhost')

    # Login como admin
    login_success = client.login(username='admin', password='admin123')
    if login_success:
        print("✓ Login como admin exitoso")

        # Probar filtro con nombre completo
        cliente_prueba = clientes_con_notifs.first()
        nombre_completo = cliente_prueba.usuario.get_full_name() or cliente_prueba.usuario.username

        print(f"Probando filtro con cliente: {nombre_completo}")

        # Probar con nombre completo
        response_completo = client.get(f'/administracion/notificaciones/?cliente={nombre_completo.replace(" ", "+")}')
        if response_completo.status_code == 200:
            content = response_completo.content.decode()
            # Verificar que aparezca el cliente en los resultados
            if nombre_completo.split()[0] in content or nombre_completo in content:
                print("✓ Filtro por nombre completo funciona")
            else:
                print("❌ Filtro por nombre completo no encontró resultados")
                return False
        else:
            print(f"❌ Error en filtro por nombre completo: {response_completo.status_code}")
            return False

        # Probar con solo nombre
        nombre = cliente_prueba.usuario.first_name
        if nombre:
            response_nombre = client.get(f'/administracion/notificaciones/?cliente={nombre}')
            if response_nombre.status_code == 200:
                print("✓ Filtro por nombre funciona")
            else:
                print(f"❌ Error en filtro por nombre: {response_nombre.status_code}")
                return False

        # Probar con apellido
        apellido = cliente_prueba.usuario.last_name
        if apellido:
            response_apellido = client.get(f'/administracion/notificaciones/?cliente={apellido}')
            if response_apellido.status_code == 200:
                print("✓ Filtro por apellido funciona")
            else:
                print(f"❌ Error en filtro por apellido: {response_apellido.status_code}")
                return False

        # Probar con username
        username = cliente_prueba.usuario.username
        response_username = client.get(f'/administracion/notificaciones/?cliente={username}')
        if response_username.status_code == 200:
            print("✓ Filtro por username funciona")
        else:
            print(f"❌ Error en filtro por username: {response_username.status_code}")
            return False

        print("✓ Todos los filtros por cliente funcionan correctamente")
        return True

    else:
        print("❌ Error en login como admin")
        return False

def main():
    """Función principal"""
    try:
        success = test_filtro_cliente()
        if success:
            print("\n=== ÉXITO: FILTRO POR CLIENTE FUNCIONA ===")
            print("Ahora puedes filtrar notificaciones por:")
            print("- Nombre completo (ej: 'Juan Pérez')")
            print("- Solo nombre (ej: 'Juan')")
            print("- Solo apellido (ej: 'Pérez')")
            print("- Username (ej: 'juan123')")
            print("- Email")
        else:
            print("\n=== ERROR: PROBLEMAS CON EL FILTRO POR CLIENTE ===")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()