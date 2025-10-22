from django.contrib import admin
from .models import Categoria, Producto, Carrito, ItemCarrito, Orden, ItemOrden, Comentario
from django.db.models import F, Avg
from django.contrib import messages
from django.utils.translation import ngettext

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre']
    list_editable = ['activo']

class LowStockFilter(admin.SimpleListFilter):
    title = 'Stock'
    parameter_name = 'stock_bajo'

    def lookups(self, request, model_admin):
        return (
            ('1', 'Bajo (<= mínimo)'),
            ('0', 'Normal (> mínimo)'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(stock__lte=F('stock_minimo'))
        if self.value() == '0':
            return queryset.filter(stock__gt=F('stock_minimo'))
        return queryset

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'precio_descuento', 'stock', 'activo', 'destacado']
    list_filter = ['categoria', LowStockFilter, 'tipo', 'activo', 'destacado', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock', 'activo', 'destacado']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    actions = ['activar', 'desactivar']

    @admin.action(description='Activar productos seleccionados')
    def activar(self, request, queryset):
        updated = queryset.update(activo=True)
        self.message_user(
            request,
            ngettext('%d producto activado.', '%d productos activados.', updated) % updated,
            messages.SUCCESS
        )

    @admin.action(description='Desactivar productos seleccionados')
    def desactivar(self, request, queryset):
        updated = queryset.update(activo=False)
        self.message_user(
            request,
            ngettext('%d producto desactivado.', '%d productos desactivados.', updated) % updated,
            messages.WARNING
        )

class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    extra = 0

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'cantidad_total', 'total', 'fecha_actualizacion']
    inlines = [ItemCarritoInline]
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']

class ItemOrdenInline(admin.TabularInline):
    model = ItemOrden
    extra = 0
    readonly_fields = ['subtotal']

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ['numero_orden', 'usuario', 'estado', 'total', 'fecha_creacion']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['numero_orden', 'usuario__username']
    inlines = [ItemOrdenInline]
    readonly_fields = ['numero_orden', 'fecha_creacion', 'fecha_actualizacion']
    list_editable = ['estado']

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['producto', 'usuario', 'calificacion', 'fecha_creacion', 'aprobado']
    list_filter = ['calificacion', 'aprobado', 'fecha_creacion', 'producto__categoria']
    search_fields = ['producto__nombre', 'usuario__username', 'comentario']
    list_editable = ['aprobado']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    actions = ['aprobar_comentarios', 'rechazar_comentarios']

    @admin.action(description='Aprobar comentarios seleccionados')
    def aprobar_comentarios(self, request, queryset):
        updated = queryset.update(aprobado=True)
        self.message_user(
            request,
            ngettext('%d comentario aprobado.', '%d comentarios aprobados.', updated) % updated,
            messages.SUCCESS
        )

    @admin.action(description='Rechazar comentarios seleccionados')
    def rechazar_comentarios(self, request, queryset):
        updated = queryset.update(aprobado=False)
        self.message_user(
            request,
            ngettext('%d comentario rechazado.', '%d comentarios rechazados.', updated) % updated,
            messages.WARNING
        )