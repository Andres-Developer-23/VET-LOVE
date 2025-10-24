#!/usr/bin/env python
"""
Script para verificar que la configuración del proyecto esté correcta.
Ejecutar con: python check_setup.py
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veterinaria_project.settings')
django.setup()

def check_database_connection():
    """Verifica la conexión a la base de datos"""
    from django.db import connection
    try:
        cursor = connection.cursor()
        print(" Conexión a base de datos exitosa")
        return True
    except Exception as e:
        print(f" Error de conexión a base de datos: {e}")
        return False

def check_required_settings():
    """Verifica que las configuraciones requeridas estén presentes"""
    from django.conf import settings
    required_settings = [
        'SECRET_KEY',
        'DATABASES',
        'INSTALLED_APPS',
    ]

    missing = []
    for setting in required_settings:
        if not hasattr(settings, setting):
            missing.append(setting)

    if missing:
        print(f"Configuraciones faltantes: {', '.join(missing)}")
        return False
    else:
        print(" Todas las configuraciones requeridas están presentes")
        return True

def check_env_variables():
    """Verifica las variables de entorno importantes"""
    from decouple import config
    env_vars = [
        'SECRET_KEY',
        'DEBUG',
        'ALLOWED_HOSTS',
        'DATABASE_URL',
    ]

    missing = []
    for var in env_vars:
        try:
            value = config(var)
            if not value:
                missing.append(var)
        except:
            missing.append(var)

    if missing:
        print(f"  Variables de entorno faltantes o vacías: {', '.join(missing)}")
        return False
    else:
        print(" Variables de entorno configuradas correctamente")
        return True

def check_dependencies():
    """Verifica que las dependencias importantes estén instaladas"""
    dependencies = [
        'django',
        'psycopg2',
        'decouple',
        'dj_database_url',
    ]

    missing = []
    for dep in dependencies:
        try:
            __import__(dep)
        except ImportError:
            missing.append(dep)

    if missing:
        print(f" Dependencias faltantes: {', '.join(missing)}")
        print("Ejecuta: pip install -r requirements.txt")
        return False
    else:
        print(" Todas las dependencias están instaladas")
        return True

def check_database_tables():
    """Verifica que las tablas de la base de datos existan"""
    from django.core.management import execute_from_command_line
    from django.db import connection

    try:
        # Verificar si hay tablas
        with connection.cursor() as cursor:
            if connection.vendor == 'postgresql':
                cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
            elif connection.vendor == 'sqlite':
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

            tables = cursor.fetchall()
            if len(tables) >= 15:  # Deberíamos tener al menos 15 tablas para una instalación completa
                print(f" Base de datos contiene {len(tables)} tablas")
                return True
            else:
                print(f"  Base de datos contiene solo {len(tables)} tablas - ejecuta 'python manage.py migrate'")
                return False
    except Exception as e:
        print(f" Error al verificar tablas: {e}")
        return False

def main():
    """Función principal"""
    print(" Verificando configuración del proyecto Veterinaria Vet Love")
    print("=" * 60)

    checks = [
        ("Dependencias", check_dependencies),
        ("Configuraciones requeridas", check_required_settings),
        ("Variables de entorno", check_env_variables),
        ("Conexión a base de datos", check_database_connection),
        ("Tablas de base de datos", check_database_tables),
    ]

    results = []
    for name, check_func in checks:
        print(f"\n Verificando {name}...")
        result = check_func()
        results.append(result)

    print("\n" + "=" * 60)
    print(" Resumen de verificación:")

    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f" ¡Excelente! Todas las verificaciones pasaron ({passed}/{total})")
        print(" El proyecto está listo para usar")
        return 0
    else:
        print(f"  Algunas verificaciones fallaron ({passed}/{total})")
        print("Revisa los mensajes de error arriba y corrige los problemas")
        return 1

if __name__ == '__main__':
    sys.exit(main())
