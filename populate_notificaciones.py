#!/usr/bin/env python
"""
Script para poblar la base de datos con notificaciones y recordatorios de prueba
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veterinaria_project.settings.base')
django.setup()

from django.contrib.auth.models import User
from clientes.models import Cliente
from notificaciones.models import Notificacion, Recordatorio
from mascotas.models import Mascota
from citas.models import Cita

def crear_notificaciones_prueba():
    """Crear notificaciones de prueba"""
    print("Creando notificaciones de prueba...")

    # Obtener clientes existentes
    clientes = Cliente.objects.all()
    if not clientes:
        print("No hay clientes en la base de datos. Ejecuta populate_db.py primero.")
        return

    # Crear notificaciones de diferentes tipos
    tipos_notificaciones = [
        ('general', 'Bienvenido a Vet Love', 'Gracias por registrarte en nuestro sistema veterinario.'),
        ('cita', 'Cita programada', 'Tienes una cita programada para mañana.'),
        ('vacuna', 'Vacuna pendiente', 'Es momento de aplicar la vacuna anual de tu mascota.'),
        ('sistema', 'Actualización del sistema', 'Hemos actualizado nuestras funcionalidades.'),
    ]

    for cliente in clientes[:3]:  # Solo para los primeros 3 clientes
        for tipo, titulo, mensaje in tipos_notificaciones:
            Notificacion.objects.create(
                cliente=cliente,
                tipo=tipo,
                titulo=titulo,
                mensaje=mensaje,
                leida=False
            )
            print(f"✓ Notificación creada para {cliente}: {titulo}")

def crear_recordatorios_prueba():
    """Crear recordatorios de prueba con fechas próximas"""
    print("\nCreando recordatorios de prueba...")

    clientes = Cliente.objects.all()
    if not clientes:
        print("No hay clientes en la base de datos.")
        return

    ahora = datetime.now()

    # Recordatorios para mañana
    manana = ahora + timedelta(days=1)
    recordatorios_manana = [
        ('cita', 'Cita veterinaria mañana', f'Cita programada para {manana.strftime("%d/%m/%Y %H:%M")}'),
        ('vacuna', 'Vacuna pendiente', 'Es momento de aplicar la vacuna antirrábica'),
        ('control', 'Control mensual', 'Revisión de peso y condición general'),
    ]

    # Recordatorios para pasado mañana
    pasado_manana = ahora + timedelta(days=2)
    recordatorios_pasado_manana = [
        ('desparasitacion', 'Desparasitación', 'Aplicar desparasitante interno y externo'),
        ('medicamento', 'Medicamento diario', 'Administrar medicamento cada 12 horas'),
    ]

    # Recordatorios para dentro de una semana
    semana = ahora + timedelta(days=7)
    recordatorios_semana = [
        ('cumpleanos', 'Cumpleaños de mascota', '¡Feliz cumpleaños! No olvides celebrar con tu mascota'),
    ]

    for cliente in clientes[:2]:  # Solo para los primeros 2 clientes
        # Recordatorios para mañana
        for tipo, titulo, mensaje in recordatorios_manana:
            Recordatorio.objects.create(
                cliente=cliente,
                tipo=tipo,
                titulo=titulo,
                mensaje=mensaje,
                fecha_recordatorio=manana.replace(hour=10, minute=0, second=0, microsecond=0),
                dias_anticipacion=1,
                activo=True
            )
            print(f"✓ Recordatorio mañana creado para {cliente}: {titulo}")

        # Recordatorios para pasado mañana
        for tipo, titulo, mensaje in recordatorios_pasado_manana:
            Recordatorio.objects.create(
                cliente=cliente,
                tipo=tipo,
                titulo=titulo,
                mensaje=mensaje,
                fecha_recordatorio=pasado_manana.replace(hour=9, minute=30, second=0, microsecond=0),
                dias_anticipacion=1,
                activo=True
            )
            print(f"✓ Recordatorio pasado mañana creado para {cliente}: {titulo}")

        # Recordatorios para semana
        for tipo, titulo, mensaje in recordatorios_semana:
            Recordatorio.objects.create(
                cliente=cliente,
                tipo=tipo,
                titulo=titulo,
                mensaje=mensaje,
                fecha_recordatorio=semana.replace(hour=12, minute=0, second=0, microsecond=0),
                dias_anticipacion=3,
                activo=True
            )
            print(f"✓ Recordatorio semanal creado para {cliente}: {titulo}")

def probar_procesamiento():
    """Probar el procesamiento de recordatorios"""
    print("\nProbando procesamiento de recordatorios...")

    from django.core.management import call_command
    from io import StringIO

    # Capturar output del comando
    output = StringIO()
    call_command('procesar_recordatorios', stdout=output)
    result = output.getvalue()

    print("Resultado del procesamiento:")
    print(result)

    # Verificar que se crearon notificaciones
    nuevas_notificaciones = Notificacion.objects.filter(leida=False).count()
    print(f"\nTotal de notificaciones no leídas: {nuevas_notificaciones}")

def main():
    """Función principal"""
    print("=== POBLANDO NOTIFICACIONES Y RECORDATORIOS DE PRUEBA ===\n")

    try:
        crear_notificaciones_prueba()
        crear_recordatorios_prueba()
        probar_procesamiento()

        print("\n=== PROCESO COMPLETADO ===")
        print("Ahora puedes:")
        print("1. Iniciar sesión como cliente")
        print("2. Ver las notificaciones en /notificaciones/")
        print("3. Ver los recordatorios en /notificaciones/recordatorios/")
        print("4. Ejecutar 'python manage.py procesar_recordatorios' para procesar recordatorios pendientes")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()