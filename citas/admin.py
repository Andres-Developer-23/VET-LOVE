from django.contrib import admin
from .models import Cita

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ['mascota', 'fecha', 'tipo', 'estado', 'veterinario', 'fecha_creacion']
    list_filter = ['estado', 'tipo', 'fecha', 'fecha_creacion']
    search_fields = ['mascota__nombre', 'motivo', 'veterinario']
    readonly_fields = ['fecha_creacion']
    date_hierarchy = 'fecha'
    ordering = ['-fecha']
    
    fieldsets = (
        (None, {
            'fields': ('mascota', 'fecha', 'tipo', 'estado')
        }),
        ('Detalles de la cita', {
            'fields': ('motivo', 'veterinario', 'notas')
        }),
        ('Recordatorio', {
            'fields': ('recordatorio_enviado',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )