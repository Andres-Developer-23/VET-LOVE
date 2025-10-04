from django.contrib import admin
from .models import Mascota, HistorialMedico, Vacuna

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = [
        'nombre', 'tipo', 'raza', 'sexo', 'cliente', 'edad', 
        'peso_actual', 'estado_vacunacion', 'desparasitacion', 'fecha_registro'
    ]
    list_filter = [
        'tipo', 'sexo', 'esterilizado', 'estado_vacunacion', 
        'desparasitacion', 'fecha_registro'
    ]
    search_fields = [
        'nombre', 'raza', 'microchip', 'cliente__usuario__first_name', 
        'cliente__usuario__last_name'
    ]
    readonly_fields = ['fecha_registro', 'edad']
    date_hierarchy = 'fecha_registro'
    
    fieldsets = (
        ('Información Básica', {
            'fields': (
                'nombre', 'cliente', 'tipo', 'raza', 'sexo', 
                'fecha_nacimiento', 'peso_actual'
            )
        }),
        ('Identificación', {
            'fields': ('microchip', 'foto', 'color', 'caracteristicas')
        }),
        ('Información Médica Crítica', {
            'fields': (
                'alergias_tipo', 'alergias_conocidas',
                'enfermedades_tipo', 'enfermedades_cronicas',
                'medicacion_actual', 'comportamiento_consulta'
            )
        }),
        ('Historial Quirúrgico', {
            'fields': (
                'cirugias_previas', 'fecha_ultima_cirugia',
                'esterilizado', 'fecha_esterilizacion'
            )
        }),
        ('Prevención y Control', {
            'fields': (
                'estado_vacunacion', 'fecha_ultima_vacuna',
                'desparasitacion', 'fecha_ultima_desparasitacion'
            )
        }),
        ('Contacto y Referencias', {
            'fields': ('veterinario_habitual', 'telefono_emergencia')
        }),
        ('Cuidados y Comportamiento', {
            'fields': (
                'tipo_alimentacion', 'frecuencia_alimentacion', 
                'comportamiento', 'permite_manejo', 
                'observaciones_comportamiento'
            )
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
    list_display = [
        'mascota', 'fecha', 'veterinario', 'peso', 'temperatura', 
        'diagnostico_corto'
    ]
    list_filter = ['fecha', 'veterinario', 'condicion_corporal']
    search_fields = [
        'mascota__nombre', 'veterinario', 'diagnostico', 'motivo_consulta'
    ]
    readonly_fields = ['fecha']
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información General', {
            'fields': ('mascota', 'veterinario', 'fecha', 'motivo_consulta')
        }),
        ('Signos Vitales', {
            'fields': (
                'peso', 'temperatura', 'frecuencia_cardiaca', 
                'frecuencia_respiratoria', 'condicion_corporal'
            )
        }),
        ('Diagnóstico y Tratamiento', {
            'fields': ('diagnostico', 'tratamiento', 'observaciones')
        }),
        ('Seguimiento', {
            'fields': ('vacunas_aplicadas', 'proxima_cita')
        }),
    )
    
    def diagnostico_corto(self, obj):
        return obj.diagnostico[:50] + '...' if len(obj.diagnostico) > 50 else obj.diagnostico
    diagnostico_corto.short_description = 'Diagnóstico'

@admin.register(Vacuna)
class VacunaAdmin(admin.ModelAdmin):
    list_display = [
        'mascota', 'nombre', 'lote', 'fecha_aplicacion', 
        'fecha_proxima', 'aplicada', 'laboratorio'
    ]
    list_filter = [
        'nombre', 'aplicada', 'fecha_aplicacion', 'laboratorio', 'via_aplicacion'
    ]
    search_fields = ['mascota__nombre', 'nombre', 'lote', 'laboratorio']
    date_hierarchy = 'fecha_aplicacion'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('mascota', 'nombre', 'aplicada')
        }),
        ('Fechas', {
            'fields': ('fecha_aplicacion', 'fecha_proxima')
        }),
        ('Detalles de la Vacuna', {
            'fields': ('lote', 'laboratorio', 'via_aplicacion', 'sitio_aplicacion')
        }),
        ('Control de Calidad', {
            'fields': ('reacciones_adversas',)
        }),
    )