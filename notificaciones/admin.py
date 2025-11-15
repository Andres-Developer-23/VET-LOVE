from django.contrib import admin
from .models import Notificacion, Recordatorio

# Configurar el template del index del admin
admin.site.index_template = 'admin/index.html'

# Sobrescribir el método index para agregar contexto de notificaciones
original_index = admin.site.index

def custom_index(request, extra_context=None):
    from veterinaria_project.context_processors import notificaciones_admin

    # Obtener el contexto de notificaciones
    notif_context = notificaciones_admin(request)
    if extra_context is None:
        extra_context = {}
    extra_context.update(notif_context)

    return original_index(request, extra_context)

admin.site.index = custom_index

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'prioridad', 'leida', 'fecha_creacion', 'para_admin')
    list_filter = ('tipo', 'prioridad', 'leida', 'para_admin', 'fecha_creacion')
    search_fields = ('titulo', 'mensaje')
    readonly_fields = ('fecha_creacion', 'fecha_lectura')
    ordering = ('-fecha_creacion',)

@admin.register(Recordatorio)
class RecordatorioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'fecha_recordatorio', 'enviado', 'activo')
    list_filter = ('tipo', 'enviado', 'activo', 'fecha_recordatorio')
    search_fields = ('titulo', 'mensaje')
    readonly_fields = ('fecha_envio',)
    ordering = ('fecha_recordatorio',)
