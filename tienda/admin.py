from django.contrib import admin
from .models import Categoria, Producto, Carrito, ItemCarrito, Orden, ItemOrden

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre']
    list_editable = ['activo']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'precio_descuento', 'stock', 'activo', 'destacado']
    list_filter = ['categoria', 'tipo', 'activo', 'destacado', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock', 'activo', 'destacado']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']

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