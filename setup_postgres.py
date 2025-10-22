#!/usr/bin/env python
"""
Script para configurar PostgreSQL para el proyecto Veterinaria Vet Love.
Ejecutar con: python setup_postgres.py
"""
import os
import sys
import subprocess
from pathlib import Path

def run_command(command, shell=False):
    """Ejecuta un comando y retorna el resultado"""
    try:
        if shell:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command.split(), capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_postgresql_running():
    """Verifica si PostgreSQL está ejecutándose"""
    import platform
    system = platform.system().lower()

    if system == "windows":
        # En Windows, verificar si el servicio está ejecutándose
        success, stdout, stderr = run_command('sc query "postgresql-x64-14" | find "RUNNING"', shell=True)
        if not success:
            # Intentar con otras versiones comunes
            for version in ["15", "14", "13", "12", "11"]:
                success, stdout, stderr = run_command(f'sc query "postgresql-x64-{version}" | find "RUNNING"', shell=True)
                if success:
                    break
        return success
    else:
        # En Linux/macOS
        success, stdout, stderr = run_command("pg_isready -h localhost -p 5432")
        return success

def create_database():
    """Crea la base de datos VETERINARIA_APP"""
    import platform
    system = platform.system().lower()

    print("📦 Creando base de datos VETERINARIA_APP...")

    # Intentar crear la base de datos
    if system == "windows":
        # En Windows, psql puede requerir especificar la contraseña
        commands = [
            'psql -U postgres -c "CREATE DATABASE VETERINARIA_APP;"',
            'psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE VETERINARIA_APP TO postgres;"'
        ]
    else:
        commands = [
            'psql -U postgres -c "CREATE DATABASE VETERINARIA_APP;"',
            'psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE VETERINARIA_APP TO postgres;"'
        ]

    for cmd in commands:
        success, stdout, stderr = run_command(cmd, shell=True)
        if not success:
            print(f"⚠️  Error ejecutando: {cmd}")
            print(f"Error: {stderr}")
            print("💡 Si hay problemas de autenticación, ejecuta manualmente:")
            print("   psql -U postgres")
            print("   CREATE DATABASE VETERINARIA_APP;")
            print("   \\q")
            return False

    print("✅ Base de datos VETERINARIA_APP creada exitosamente")
    return True

def set_postgres_password():
    """Configura la contraseña del usuario postgres"""
    import platform
    system = platform.system().lower()

    print("🔑 Configurando contraseña del usuario postgres...")

    password = "01032001"

    if system == "windows":
        # En Windows, intentar cambiar la contraseña
        cmd = f'psql -U postgres -c "ALTER USER postgres PASSWORD \'{password}\';"'
        success, stdout, stderr = run_command(cmd, shell=True)

        if success:
            print("✅ Contraseña del usuario postgres configurada")
            return True
        else:
            print("⚠️  No se pudo cambiar la contraseña automáticamente en Windows")
            print("Posibles soluciones:")
            print("1. Durante la instalación de PostgreSQL, configura la contraseña '01032001'")
            print("2. O ejecuta en CMD como administrador:")
            print('   psql -U postgres -c "ALTER USER postgres PASSWORD \'01032001\';"')
            print("3. Si no funciona, configura la autenticación en pg_hba.conf")
            return False
    else:
        # En Linux/macOS
        cmd = f'psql -U postgres -c "ALTER USER postgres PASSWORD \'{password}\';"'
        success, stdout, stderr = run_command(cmd, shell=True)

        if success:
            print("✅ Contraseña del usuario postgres configurada")
            return True
        else:
            print("⚠️  No se pudo cambiar la contraseña automáticamente")
            print("Posibles soluciones:")
            print("1. Ejecutar como superusuario: sudo -u postgres psql")
            print("2. Dentro de psql ejecutar: ALTER USER postgres PASSWORD '01032001';")
            print("3. O configurar manualmente la autenticación en pg_hba.conf")
            return False

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    print("🔍 Probando conexión a la base de datos...")

    try:
        import psycopg2
        conn = psycopg2.connect(
            dbname="VETERINARIA_APP",
            user="postgres",
            password="01032001",
            host="localhost",
            port="5432"
        )
        conn.close()
        print("✅ Conexión a PostgreSQL exitosa")
        return True
    except ImportError:
        print("❌ psycopg2 no está instalado")
        return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def main():
    """Función principal"""
    import platform
    system = platform.system().lower()

    print("🐘 Configurando PostgreSQL para Veterinaria Vet Love")
    print("=" * 50)

    # Verificar si PostgreSQL está instalado y ejecutándose
    if not check_postgresql_running():
        print("❌ PostgreSQL no está ejecutándose")
        print("Instala y ejecuta PostgreSQL:")
        if system == "windows":
            print("Windows:")
            print("1. Descarga PostgreSQL desde: https://www.postgresql.org/download/windows/")
            print("2. Ejecuta el instalador como administrador")
            print("3. Durante la instalación, configura la contraseña '01032001' para el usuario postgres")
            print("4. Asegúrate de que el servicio PostgreSQL esté ejecutándose")
            print("5. Verifica con: pg_isready -h localhost -p 5432")
        else:
            print("Ubuntu/Debian: sudo apt install postgresql postgresql-contrib && sudo systemctl start postgresql")
            print("CentOS/RHEL: sudo yum install postgresql-server && sudo postgresql-setup initdb && sudo systemctl start postgresql")
            print("macOS: brew install postgresql && brew services start postgresql")
        return 1

    print("✅ PostgreSQL está ejecutándose")

    # Configurar contraseña
    if not set_postgres_password():
        print("⚠️  Continuando con la configuración...")

    # Crear base de datos
    if not create_database():
        print("❌ Error creando la base de datos")
        return 1

    # Probar conexión
    if not test_database_connection():
        print("❌ Error de conexión a la base de datos")
        print("Verifica la configuración en el archivo .env")
        return 1

    print("\n" + "=" * 50)
    print("🎉 ¡PostgreSQL configurado exitosamente!")
    print("Ahora puedes ejecutar:")
    print("  python manage.py migrate")
    print("  python check_setup.py")
    return 0

if __name__ == '__main__':
    sys.exit(main())