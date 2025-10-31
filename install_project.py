#!/usr/bin/env python
"""
Script de instalación automática para Veterinaria Vet Love
Ejecuta todos los pasos de instalación de manera automática.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description):
    """Ejecuta un comando y muestra el resultado."""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        print(f"Salida de error: {e.stderr}")
        return False

def main():
    """Función principal de instalación."""
    print("🐾 Instalando Veterinaria Vet Love...")
    print("=" * 50)

    # Verificar que estamos en el directorio correcto
    if not Path("manage.py").exists():
        print("❌ Error: Ejecuta este script desde la raíz del proyecto (donde está manage.py)")
        sys.exit(1)

    # 1. Verificar Python
    python_version = sys.version_info
    if python_version < (3, 8):
        print(f"❌ Error: Se requiere Python 3.8 o superior. Versión actual: {python_version.major}.{python_version.minor}")
        sys.exit(1)
    print(f"✅ Python {python_version.major}.{python_version.minor} detectado")

    # 2. Crear entorno virtual si no existe
    if not Path(".venv").exists():
        if not run_command("python -m venv .venv", "Crear entorno virtual"):
            sys.exit(1)
    else:
        print("✅ Entorno virtual ya existe")

    # 3. Activar entorno virtual
    if platform.system() == "Windows":
        activate_cmd = ".venv\\Scripts\\activate"
        pip_cmd = ".venv\\Scripts\\pip"
        python_cmd = ".venv\\Scripts\\python"
    else:
        activate_cmd = "source .venv/bin/activate"
        pip_cmd = ".venv/bin/pip"
        python_cmd = ".venv/bin/python"

    # 4. Instalar dependencias
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Instalar dependencias"):
        print("⚠️  Advertencia: Algunas dependencias fallaron, pero continuando...")
        print("   Intentando instalar dependencias críticas individualmente...")

        # Instalar dependencias críticas una por una
        critical_deps = [
            "django",
            "python-decouple",
            "dj-database-url",
            "django-crispy-forms",
            "crispy-bootstrap5"
        ]

        for dep in critical_deps:
            run_command(f"{pip_cmd} install {dep}", f"Instalar {dep}")

    # 5. Verificar archivo .env
    if not Path(".env").exists():
        if Path(".env.example").exists():
            if run_command("copy .env.example .env" if platform.system() == "Windows" else "cp .env.example .env", "Copiar archivo .env"):
                print("⚠️  IMPORTANTE: Edita el archivo .env con tu SECRET_KEY y configuración")
        else:
            print("⚠️  Advertencia: No se encontró .env.example, crea manualmente el archivo .env")
    else:
        print("✅ Archivo .env ya existe")

    # 6. Ejecutar migraciones
    if not run_command(f"{python_cmd} manage.py migrate", "Ejecutar migraciones de base de datos"):
        sys.exit(1)

    # 7. Configurar grupos de usuarios
    if not run_command(f'{python_cmd} manage.py shell -c "from setup_groups import setup_groups; setup_groups()"', "Configurar grupos de usuarios"):
        sys.exit(1)

    # 8. Recopilar archivos estáticos
    if not run_command(f"{python_cmd} manage.py collectstatic --noinput", "Recopilar archivos estáticos"):
        sys.exit(1)

    print("\n" + "=" * 50)
    print("🎉 ¡Instalación completada exitosamente!")
    print("\n📋 Próximos pasos:")
    print("1. Si no tienes superusuario, ejecuta: python manage.py createsuperuser")
    print("2. Inicia el servidor: python manage.py runserver")
    print("3. Accede a la aplicación: http://localhost:8000")
    print("4. Panel de administración: http://localhost:8000/admin/")
    print("\n⚠️  Recuerda configurar tu SECRET_KEY en el archivo .env si no lo has hecho")

if __name__ == "__main__":
    main()