import os
import django
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veterinaria_project.settings')

try:
    django.setup()
    
    from django.conf import settings
    print("=== INSTALLED_APPS ===")
    for i, app in enumerate(settings.INSTALLED_APPS):
        print(f"{i+1}. {app}")
    
    print("\n=== BUSCANDO DUPLICADOS ===")
    from collections import Counter
    app_counts = Counter(settings.INSTALLED_APPS)
    
    duplicates = {app: count for app, count in app_counts.items() if count > 1}
    if duplicates:
        print("DUPLICADOS ENCONTRADOS:")
        for app, count in duplicates.items():
            print(f"  {app}: {count} veces")
    else:
        print("No se encontraron duplicados en INSTALLED_APPS")
        
except Exception as e:
    print(f"Error: {e}")