#!/usr/bin/env python
"""
Script para verificar PostgreSQL en Windows
Ejecutar con: python check_postgres_windows.py
"""
import os
import subprocess
import sys

def check_postgresql_paths():
    """Busca instalaciones de PostgreSQL en rutas comunes"""
    common_paths = [
        r"C:\Program Files\PostgreSQL",
        r"C:\Program Files (x86)\PostgreSQL"
    ]

    found_paths = []
    for base_path in common_paths:
        if os.path.exists(base_path):
            # Buscar versiones
            try:
                subdirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d)) and d.isdigit()]
                for version in subdirs:
                    bin_path = os.path.join(base_path, version, "bin")
                    if os.path.exists(bin_path):
                        found_paths.append((version, bin_path))
            except:
                pass

    return found_paths

def test_postgresql_connection(bin_path):
    """Prueba la conexión usando pg_isready"""
    pg_isready = os.path.join(bin_path, "pg_isready.exe")
    if os.path.exists(pg_isready):
        try:
            result = subprocess.run([pg_isready, "-h", "localhost", "-p", "5432"],
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except:
            return False
    return False

def test_psql_connection(bin_path):
    """Prueba la conexión usando psql"""
    psql = os.path.join(bin_path, "psql.exe")
    if os.path.exists(psql):
        try:
            # Intentar conectar sin contraseña primero
            result = subprocess.run([psql, "-U", "postgres", "-c", "SELECT version();"],
                                  capture_output=True, text=True, timeout=10,
                                  input="01032001\n" if "password" in str(result.stderr).lower() else "")
            return result.returncode == 0
        except:
            return False
    return False

def main():
    print("🔍 Verificando PostgreSQL en Windows")
    print("=" * 40)

    # Buscar instalaciones
    installations = check_postgresql_paths()

    if not installations:
        print("❌ No se encontraron instalaciones de PostgreSQL")
        print("\n📋 Instrucciones de instalación:")
        print("1. Ve a: https://www.postgresql.org/download/windows/")
        print("2. Descarga e instala PostgreSQL")
        print("3. Durante la instalación:")
        print("   - Configura contraseña '01032001' para usuario postgres")
        print("   - Instala pgAdmin y Command Line Tools")
        print("4. Reinicia este script")
        return 1

    print(f"✅ Encontradas {len(installations)} instalación(es) de PostgreSQL:")
    for version, path in installations:
        print(f"   Versión {version}: {path}")

    # Probar conexiones
    print("\n🔍 Probando conexiones...")
    working_installations = []

    for version, bin_path in installations:
        print(f"\n📋 Probando PostgreSQL {version}...")

        # Verificar si el servicio está ejecutándose
        if test_postgresql_connection(bin_path):
            print("   ✅ Servicio PostgreSQL ejecutándose")
            working_installations.append((version, bin_path))
        else:
            print("   ❌ Servicio PostgreSQL no responde")

        # Intentar conexión con psql
        if test_psql_connection(bin_path):
            print("   ✅ Conexión psql exitosa")
        else:
            print("   ⚠️  Conexión psql requiere configuración")

    if working_installations:
        print(f"\n🎉 ¡PostgreSQL está funcionando! ({len(working_installations)} instalación(es))")
        print("\n📋 Próximos pasos:")
        print("1. Crear base de datos:")
        version, bin_path = working_installations[0]  # Usar la primera
        psql_path = os.path.join(bin_path, "psql.exe")
        print(f'   "{psql_path}" -U postgres -c "CREATE DATABASE VETERINARIA_APP;"')

        print("2. Configurar .env:")
        print("   DATABASE_URL=postgresql://postgres:01032001@localhost:5432/VETERINARIA_APP")

        print("3. Ejecutar migraciones:")
        print("   python manage.py migrate")

        return 0
    else:
        print("\n❌ PostgreSQL instalado pero no funcionando")
        print("\n🔧 Posibles soluciones:")
        print("1. Inicia el servicio PostgreSQL:")
        print("   - Abre 'services.msc'")
        print("   - Busca 'postgresql' y haz clic derecho > Iniciar")
        print("2. Verifica que el puerto 5432 no esté bloqueado")
        print("3. Revisa la configuración de autenticación en pg_hba.conf")
        return 1

if __name__ == '__main__':
    sys.exit(main())