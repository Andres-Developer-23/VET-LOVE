from django.contrib import admin
from .models import Mascota, HistorialMedico, Vacuna

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'raza', 'sexo', 'cliente', 'edad', 'fecha_registro']
    list_filter = ['tipo', 'sexo', 'fecha_registro']
    search_fields = ['nombre', 'raza', 'cliente__usuario__first_name', 'cliente__usuario__last_name']
    readonly_fields = ['fecha_registro', 'edad']
    date_hierarchy = 'fecha_registro'
    fieldsets = (
        (None, {
            'fields': ('nombre', 'cliente')
        }),
        ('Información de la mascota', {
            'fields': ('tipo', 'raza', 'sexo', 'fecha_nacimiento', 'foto', 'caracteristicas')
        }),
        ('Metadata', {
            'fields': ('fecha_registro',),
            'classes': ('collapse',)
        }),
    )

    def edad(self, obj):
        return obj.edad()
    edad.short_description = 'Edad'

@admin.register(HistorialMedico)
class HistorialMedicoAdmin(admin.ModelAdmin):
    list_display = ['mascota', 'fecha', 'veterinario', 'diagnostico_corto', 'peso']
    list_filter = ['fecha', 'veterinario']
    search_fields = ['mascota__nombre', 'veterinario', 'diagnostico']
    readonly_fields = ['fecha']
    date_hierarchy = 'fecha'
    
    def diagnostico_corto(self, obj):
        return obj.diagnostico[:50] + '...' if len(obj.diagnostico) > 50 else obj.diagnostico
    diagnostico_corto.short_description = 'Diagnóstico'

@admin.register(Vacuna)
class VacunaAdmin(admin.ModelAdmin):
    list_display = ['mascota', 'nombre', 'fecha_aplicacion', 'fecha_proxima', 'aplicada']
    list_filter = ['nombre', 'aplicada', 'fecha_aplicacion']
    search_fields = ['mascota__nombre', 'nombre']
    date_hierarchy = 'fecha_aplicacion'