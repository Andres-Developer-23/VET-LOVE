from django.contrib import admin
from .models import Cita

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ['mascota', 'fecha', 'tipo', 'estado', 'veterinario']
    list_filter = ['estado', 'tipo', 'fecha']
    search_fields = ['mascota__nombre', 'motivo', 'veterinario']
    date_hierarchy = 'fecha'
    ordering = ['-fecha']