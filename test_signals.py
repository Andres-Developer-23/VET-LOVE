#!/usr/bin/env python
"""
Script para probar las señales de notificaciones
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veterinaria_project.settings.base')
django.setup()

from clientes.models import Cliente
from mascotas.models import Mascota
from citas.models import Cita
from mascotas.models import Vacuna
from notificaciones.models import Notificacion, Recordatorio
from datetime import datetime, timedelta

def test_cita_signal():
    """Probar señal de creación de cita"""
    print("=== Probando señal de cita ===")

    cliente = Cliente.objects.first()
    mascota = cliente.mascotas.first()

    if not cliente or not mascota:
        print("No hay cliente o mascota disponible")
        return

    print(f"Cliente: {cliente}")
    print(f"Mascota: {mascota}")

    # Contar notificaciones y recordatorios antes
    notifs_antes = Notificacion.objects.filter(cliente=cliente).count()
    records_antes = Recordatorio.objects.filter(cliente=cliente).count()

    print(f"Notificaciones antes: {notifs_antes}")
    print(f"Recordatorios antes: {records_antes}")

    # Crear cita
    manana = datetime.now() + timedelta(days=1)
    cita = Cita.objects.create(
        mascota=mascota,
        fecha=manana.replace(hour=15, minute=30),
        tipo='consulta_general',
        motivo='Prueba de señal de notificaciones',
        estado='programada'
    )

    print(f"Cita creada: {cita}")

    # Contar después
    notifs_despues = Notificacion.objects.filter(cliente=cliente).count()
    records_despues = Recordatorio.objects.filter(cliente=cliente).count()

    print(f"Notificaciones después: {notifs_despues}")
    print(f"Recordatorios después: {records_despues}")

    # Ver las nuevas
    nuevas_notifs = Notificacion.objects.filter(cliente=cliente).order_by('-fecha_creacion')[:2]
    nuevos_records = Recordatorio.objects.filter(cliente=cliente).order_by('-fecha_recordatorio')[:1]

    print("\nNuevas notificaciones:")
    for n in nuevas_notifs:
        print(f"  - {n.titulo}: {n.mensaje[:60]}...")

    print("\nNuevos recordatorios:")
    for r in nuevos_records:
        print(f"  - {r.titulo} para {r.fecha_recordatorio}")

def test_vacuna_signal():
    """Probar señal de creación de vacuna"""
    print("\n=== Probando señal de vacuna ===")

    cliente = Cliente.objects.first()
    mascota = cliente.mascotas.first()

    if not cliente or not mascota:
        print("No hay cliente o mascota disponible")
        return

    # Contar antes
    notifs_antes = Notificacion.objects.filter(cliente=cliente).count()
    records_antes = Recordatorio.objects.filter(cliente=cliente).count()

    # Crear vacuna con fecha próxima
    fecha_proxima = datetime.now().date() + timedelta(days=30)
    vacuna = Vacuna.objects.create(
        mascota=mascota,
        nombre='Vacuna Test',
        fecha_aplicacion=datetime.now().date(),
        fecha_proxima=fecha_proxima,
        aplicada=True
    )

    print(f"Vacuna creada: {vacuna}")

    # Contar después
    notifs_despues = Notificacion.objects.filter(cliente=cliente).count()
    records_despues = Recordatorio.objects.filter(cliente=cliente).count()

    print(f"Notificaciones: {notifs_antes} -> {notifs_despues}")
    print(f"Recordatorios: {records_antes} -> {records_despues}")

    # Ver las nuevas
    nuevas_notifs = Notificacion.objects.filter(cliente=cliente).order_by('-fecha_creacion')[:1]
    nuevos_records = Recordatorio.objects.filter(cliente=cliente).order_by('-fecha_recordatorio')[:1]

    print("\nNueva notificación de vacuna:")
    for n in nuevas_notifs:
        print(f"  - {n.titulo}: {n.mensaje[:60]}...")

    print("\nNuevo recordatorio de vacuna:")
    for r in nuevos_records:
        print(f"  - {r.titulo} para {r.fecha_recordatorio}")

def main():
    """Función principal"""
    print("=== PRUEBA DE SEÑALES DE NOTIFICACIONES ===\n")

    try:
        test_cita_signal()
        test_vacuna_signal()

        print("\n=== PRUEBA COMPLETADA ===")
        print("Las señales están funcionando correctamente!")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()