from django.contrib import admin, messages
from .models import Mascota, HistorialMedico, Vacuna
from veterinario.models import Veterinario

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = [
        'nombre', 'tipo', 'raza', 'sexo', 'cliente', 'veterinario_asignado', 'edad',
        'peso_actual', 'estado_vacunacion', 'desparasitacion', 'fecha_registro'
    ]
    list_filter = [
        'tipo', 'sexo', 'esterilizado', 'estado_vacunacion',
        'desparasitacion', 'veterinario_asignado', 'fecha_registro'
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
        ('Asignación de Veterinario', {
            'fields': ('veterinario_asignado',),
            'description': 'Selecciona el veterinario responsable de esta mascota. Si no hay veterinarios disponibles, primero registra uno en la sección Veterinarios.'
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

    def save_model(self, request, obj, form, change):
        # Guardar el veterinario anterior para comparar
        veterinario_anterior = None
        if change:  # Si es una edición
            mascota_original = Mascota.objects.get(pk=obj.pk)
            veterinario_anterior = mascota_original.veterinario_asignado

        # Guardar el objeto
        super().save_model(request, obj, form, change)

        # Mensajes personalizados
        if change:
            if obj.veterinario_asignado != veterinario_anterior:
                if obj.veterinario_asignado:
                    messages.success(
                        request,
                        f'¡Excelente! La mascota "{obj.nombre}" ha sido asignada al veterinario Dr. {obj.veterinario_asignado.nombre_completo}.'
                    )
                else:
                    messages.info(
                        request,
                        f'La asignación de veterinario para "{obj.nombre}" ha sido removida.'
                    )
            else:
                messages.success(
                    request,
                    f'Los datos de la mascota "{obj.nombre}" ({obj.get_tipo_display()}) se han actualizado correctamente.'
                )
        else:
            messages.success(
                request,
                f'¡Nueva mascota registrada! "{obj.nombre}" ({obj.get_tipo_display()}) ha sido agregada al sistema.'
            )

    def delete_model(self, request, obj):
        messages.warning(
            request,
            f'La mascota "{obj.nombre}" ({obj.get_tipo_display()}) ha sido eliminada del sistema.'
        )
        super().delete_model(request, obj)

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
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            messages.success(
                request,
                f'El historial médico de "{obj.mascota.nombre}" ha sido actualizado correctamente.'
            )
        else:
            messages.success(
                request,
                f'Nuevo historial médico registrado para "{obj.mascota.nombre}".'
            )

    def delete_model(self, request, obj):
        messages.warning(
            request,
            f'El historial médico de "{obj.mascota.nombre}" (fecha: {obj.fecha.strftime("%d/%m/%Y")}) ha sido eliminado.'
        )
        super().delete_model(request, obj)

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

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            messages.success(
                request,
                f'La vacuna "{obj.nombre}" de "{obj.mascota.nombre}" ha sido actualizada correctamente.'
            )
        else:
            messages.success(
                request,
                f'Nueva vacuna "{obj.nombre}" registrada para "{obj.mascota.nombre}".'
            )

    def delete_model(self, request, obj):
        messages.warning(
            request,
            f'La vacuna "{obj.nombre}" de "{obj.mascota.nombre}" ha sido eliminada del registro.'
        )
        super().delete_model(request, obj)

@admin.register(Veterinario)
class VeterinarioAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'especialidad', 'numero_colegiado', 'telefono', 'activo']
    list_filter = ['activo', 'especialidad']
    search_fields = ['nombre_completo', 'numero_colegiado', 'usuario__username']
    readonly_fields = ['usuario']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            messages.success(
                request,
                f'Los datos del veterinario Dr. {obj.nombre_completo} han sido actualizados correctamente.'
            )
        else:
            messages.success(
                request,
                f'¡Nuevo veterinario registrado! Dr. {obj.nombre_completo} ha sido agregado al sistema.'
            )

    def delete_model(self, request, obj):
        messages.warning(
            request,
            f'El veterinario Dr. {obj.nombre_completo} ha sido removido del sistema.'
        )
        super().delete_model(request, obj)