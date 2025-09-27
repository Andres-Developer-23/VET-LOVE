from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from .models import Cliente

# Remover el grupo "Clientes" del admin para usuarios normales
admin.site.unregister(Group)

class ClienteInline(admin.StackedInline):
    model = Cliente
    can_delete = False
    verbose_name_plural = 'Información adicional'
    fields = ('telefono', 'direccion', 'preferencias_comunicacion', 'foto_perfil')
    readonly_fields = ('fecha_registro',)

class CustomUserAdmin(UserAdmin):
    inlines = (ClienteInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    # Restringir qué usuarios pueden ver/modificar en el admin
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Los staff normales solo ven usuarios no staff
            return qs.filter(is_staff=False, is_superuser=False)
        return qs

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefono', 'preferencias_comunicacion', 'fecha_registro')
    list_filter = ('preferencias_comunicacion', 'fecha_registro')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name', 'telefono')
    readonly_fields = ('fecha_registro',)
    date_hierarchy = 'fecha_registro'
    
    # Restringir acceso a clientes específicos para staff no superusuarios
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Los staff normales no pueden ver clientes
            return qs.none()
        return qs

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)