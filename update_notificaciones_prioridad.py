#!/usr/bin/env python
"""
Script para actualizar las prioridades de las notificaciones existentes
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veterinaria_project.settings.base')
django.setup()

from notificaciones.models import Notificacion

def actualizar_prioridades():
    """Actualizar prioridades de notificaciones existentes"""
    print("Actualizando prioridades de notificaciones existentes...")

    # Vacunas tienen prioridad alta
    vacunas_actualizadas = Notificacion.objects.filter(
        tipo='vacuna',
        prioridad='normal'
    ).update(prioridad='alta')

    print(f"✓ Actualizadas {vacunas_actualizadas} notificaciones de vacunas a prioridad alta")

    # Citas urgentes tienen prioridad alta
    citas_urgentes = Notificacion.objects.filter(
        tipo='cita',
        titulo__icontains='urgente',
        prioridad='normal'
    ).update(prioridad='alta')

    print(f"✓ Actualizadas {citas_urgentes} notificaciones de citas urgentes")

    # Citas de emergencia tienen prioridad urgente
    citas_emergencia = Notificacion.objects.filter(
        tipo='cita',
        titulo__icontains='emergencia',
        prioridad='normal'
    ).update(prioridad='urgente')

    print(f"✓ Actualizadas {citas_emergencia} notificaciones de emergencias")

    # Verificar resultados
    total_notifs = Notificacion.objects.count()
    alta_prioridad = Notificacion.objects.filter(prioridad='alta').count()
    urgente_prioridad = Notificacion.objects.filter(prioridad='urgente').count()

    print("\nResumen de prioridades:")
    print(f"  - Total de notificaciones: {total_notifs}")
    print(f"  - Prioridad alta: {alta_prioridad}")
    print(f"  - Prioridad urgente: {urgente_prioridad}")

if __name__ == '__main__':
    actualizar_prioridades()
    print("\n=== ACTUALIZACIÓN COMPLETADA ===")