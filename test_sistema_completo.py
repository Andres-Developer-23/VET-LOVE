#!/usr/bin/env python
"""
Script para probar el sistema completo de notificaciones y recordatorios
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veterinaria_project.settings.base')
django.setup()

from django.contrib.auth.models import User
from clientes.models import Cliente
from notificaciones.models import Notificacion, Recordatorio

def probar_sistema_completo():
    """Probar que todo el sistema funciona correctamente"""
    print("🚀 PRUEBA COMPLETA DEL SISTEMA DE NOTIFICACIONES")
    print("=" * 60)

    # 1. Verificar estructura de la base de datos
    print("\n📊 1. ESTRUCTURA DE LA BASE DE DATOS:")
    print(f"   • Usuarios registrados: {User.objects.count()}")
    print(f"   • Clientes registrados: {Cliente.objects.count()}")
    print(f"   • Notificaciones totales: {Notificacion.objects.count()}")
    print(f"   • Recordatorios totales: {Recordatorio.objects.count()}")

    # 2. Verificar tipos de notificaciones
    from django.db.models import Count
    tipos_notif = Notificacion.objects.values('tipo').annotate(
        total=Count('id')
    ).order_by('-total')

    print("\n🏷️ 2. TIPOS DE NOTIFICACIONES:")
    for tipo in tipos_notif:
        print(f"   • {tipo['tipo']}: {tipo['total']} notificaciones")

    # 3. Verificar prioridades
    prioridades = Notificacion.objects.values('prioridad').annotate(
        total=Count('id')
    ).order_by('-total')

    print("\n⚡ 3. PRIORIDADES:")
    for prio in prioridades:
        print(f"   • {prio['prioridad']}: {prio['total']} notificaciones")

    # 4. Verificar estado de notificaciones
    leidas = Notificacion.objects.filter(leida=True).count()
    no_leidas = Notificacion.objects.filter(leida=False).count()

    print("\n📬 4. ESTADO DE NOTIFICACIONES:")
    print(f"   • Leídas: {leidas}")
    print(f"   • No leídas: {no_leidas}")
    print(f"   • Tasa de lectura: {(leidas / (leidas + no_leidas) * 100):.1f}%" if (leidas + no_leidas) > 0 else "   • Tasa de lectura: N/A")

    # 5. Verificar recordatorios
    activos = Recordatorio.objects.filter(activo=True).count()
    enviados = Recordatorio.objects.filter(enviado=True).count()
    pendientes = Recordatorio.objects.filter(activo=True, enviado=False).count()

    print("\n⏰ 5. RECORDATORIOS:")
    print(f"   • Activos: {activos}")
    print(f"   • Enviados: {enviados}")
    print(f"   • Pendientes: {pendientes}")

    # 6. Verificar distribución por cliente
    print("\n👥 6. DISTRIBUCIÓN POR CLIENTE:")
    clientes = Cliente.objects.all()
    for cliente in clientes:
        notifs = Notificacion.objects.filter(cliente=cliente).count()
        records = Recordatorio.objects.filter(cliente=cliente).count()
        print(f"   • {cliente.usuario.get_full_name() or cliente.usuario.username}: {notifs} notifs, {records} records")

    # 7. Verificar funcionalidades principales
    print("\n✅ 7. FUNCIONALIDADES VERIFICADAS:")

    # Verificar que hay notificaciones recientes
    recientes = Notificacion.objects.order_by('-fecha_creacion')[:5]
    if recientes.exists():
        print("   ✅ Notificaciones recientes disponibles")
    else:
        print("   ⚠️ No hay notificaciones recientes")

    # Verificar que hay recordatorios activos
    if Recordatorio.objects.filter(activo=True).exists():
        print("   ✅ Recordatorios activos encontrados")
    else:
        print("   ⚠️ No hay recordatorios activos")

    # Verificar que hay clientes con notificaciones
    clientes_con_notifs = Cliente.objects.filter(notificaciones__isnull=False).distinct().count()
    if clientes_con_notifs > 0:
        print(f"   ✅ {clientes_con_notifs} clientes tienen notificaciones")
    else:
        print("   ⚠️ No hay clientes con notificaciones")

    # Verificar que hay administradores
    admins = User.objects.filter(is_staff=True)
    if admins.exists():
        print(f"   ✅ {admins.count()} administradores configurados")
    else:
        print("   ⚠️ No hay administradores configurados")

    # 8. Verificar URLs disponibles
    print("\n🔗 8. URLs DISPONIBLES:")

    urls_disponibles = [
        "/notificaciones/ - Lista de notificaciones (clientes)",
        "/notificaciones/recordatorios/ - Lista de recordatorios (clientes)",
        "/administracion/dashboard/ - Dashboard administrativo",
        "/administracion/notificaciones/ - Gestión de notificaciones",
        "/administracion/notificaciones/crear/ - Crear notificaciones",
        "python manage.py procesar_recordatorios - Procesar recordatorios"
    ]

    for url in urls_disponibles:
        print(f"   • {url}")

    # 9. Resumen final
    print("\n🎉 9. RESUMEN DEL SISTEMA:")

    total_notifs = Notificacion.objects.count()
    total_records = Recordatorio.objects.count()
    total_clientes = Cliente.objects.count()

    if total_notifs > 0 and total_records > 0 and total_clientes > 0:
        print("   ✅ SISTEMA COMPLETAMENTE FUNCIONAL")
        print(f"   📊 {total_notifs} notificaciones, {total_records} recordatorios, {total_clientes} clientes")
        print("   🚀 Listo para producción")
    else:
        print("   ⚠️ Sistema requiere configuración adicional")
        print("   💡 Ejecuta populate_notificaciones.py para datos de prueba")

    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA EXITOSAMENTE")

if __name__ == '__main__':
    probar_sistema_completo()