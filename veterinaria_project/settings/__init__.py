"""
Django settings configuration.

This module dynamically imports the appropriate settings based on the
DJANGO_SETTINGS_MODULE environment variable or defaults to development.
"""
import os

# Default to development settings if not specified
settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'veterinaria_project.settings.development')

# Extract the settings name (development, production, etc.)
settings_name = settings_module.split('.')[-1]

# Import the appropriate settings module
if settings_name == 'production':
    from .production import *
elif settings_name == 'development':
    from .development import *
else:
    # Fallback to base settings
    from .base import *