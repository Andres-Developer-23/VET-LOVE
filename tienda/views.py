from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.urls import reverse
from .models import Producto, Categoria, Carrito, ItemCarrito, Orden, ItemOrden
from .forms import OrdenForm
import random
import string
from decimal import Decimal

def lista_productos(request):
    categorias = Categoria.objects.filter(activo=True)
    productos = Producto.objects.filter(activo=True)
    
    # Filtros
    categoria_id = request.GET.get('categoria')
    tipo = request.GET.get('tipo')
    buscar = request.GET.get('buscar')
    
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    if tipo:
        productos = productos.filter(tipo=tipo)
    if buscar:
        productos = productos.filter(nombre__icontains=buscar)
    
    context = {
        'productos': productos,
        'categorias': categorias,
        'categoria_actual': int(categoria_id) if categoria_id else None,
    }
    return render(request, 'tienda/lista_productos.html', context)

def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id, activo=True)
    productos = Producto.objects.filter(categoria=categoria, activo=True)
    
    context = {
        'productos': productos,
        'categoria': categoria,
        'categorias': Categoria.objects.filter(activo=True),
    }
    return render(request, 'tienda/productos_por_categoria.html', context)

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    productos_relacionados = Producto.objects.filter(
        categoria=producto.categoria, 
        activo=True
    ).exclude(id=producto.id)[:4]
    
    context = {
        'producto': producto,
        'productos_relacionados': productos_relacionados,
    }
    return render(request, 'tienda/detalle_producto.html', context)

@login_required
def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    context = {
        'carrito': carrito,
    }
    return render(request, 'tienda/carrito.html', context)

@login_required
@require_POST
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    cantidad = int(request.POST.get('cantidad', 1))
    
    if cantidad <= 0:
        messages.error(request, 'La cantidad debe ser mayor a 0')
        return redirect('tienda:detalle_producto', producto_id=producto_id)
    
    if producto.stock < cantidad:
        messages.error(request, f'No hay suficiente stock. Stock disponible: {producto.stock}')
        return redirect('tienda:detalle_producto', producto_id=producto_id)
    
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    
    item, item_created = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'cantidad': cantidad}
    )
    
    if not item_created:
        item.cantidad += cantidad
        item.save()
    
    messages.success(request, f'"{producto.nombre}" agregado al carrito')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'carrito_count': carrito.cantidad_total,
            'message': f'"{producto.nombre}" agregado al carrito'
        })
    
    return redirect('tienda:ver_carrito')

@login_required
@require_POST
def actualizar_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    cantidad = int(request.POST.get('cantidad', 1))
    
    if cantidad <= 0:
        item.delete()
        messages.success(request, 'Producto eliminado del carrito')
    else:
        if item.producto.stock < cantidad:
            messages.error(request, f'No hay suficiente stock. Stock disponible: {item.producto.stock}')
            return redirect('tienda:ver_carrito')
        
        item.cantidad = cantidad
        item.save()
        messages.success(request, 'Carrito actualizado')
    
    return redirect('tienda:ver_carrito')

@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    item.delete()
    messages.success(request, 'Producto eliminado del carrito')
    return redirect('tienda:ver_carrito')

@login_required
def vaciar_carrito(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    carrito.items.all().delete()
    messages.success(request, 'Carrito vaciado')
    return redirect('tienda:ver_carrito')

@login_required
def checkout(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    
    if carrito.cantidad_total == 0:
        messages.error(request, 'Tu carrito está vacío')
        return redirect('tienda:lista_productos')
    
    # Verificar stock
    for item in carrito.items.all():
        if item.cantidad > item.producto.stock:
            messages.error(request, f'No hay suficiente stock de "{item.producto.nombre}". Stock disponible: {item.producto.stock}')
            return redirect('tienda:ver_carrito')
    
    if request.method == 'POST':
        form = OrdenForm(request.POST)
        if form.is_valid():
            # Procesar la orden directamente aquí
            return procesar_orden(request, form.cleaned_data, carrito)
    else:
        # Prellenar con datos del usuario si existen
        initial_data = {}
        if hasattr(request.user, 'cliente'):
            cliente = request.user.cliente
            initial_data['direccion_envio'] = cliente.direccion or ''
        
        form = OrdenForm(initial=initial_data)
    
    context = {
        'carrito': carrito,
        'form': form,
    }
    return render(request, 'tienda/checkout.html', context)

@login_required
@transaction.atomic
def procesar_orden(request, form_data, carrito):
    """Procesa la creación de la orden"""
    
    # Generar número de orden único
    def generar_numero_orden():
        return 'ORD' + ''.join(random.choices(string.digits, k=8))
    
    numero_orden = generar_numero_orden()
    while Orden.objects.filter(numero_orden=numero_orden).exists():
        numero_orden = generar_numero_orden()
    
    # Calcular totales (incluyendo envío) - CORREGIDO
    subtotal = carrito.total
    envio = 0 if subtotal >= 50000 else 5000
    impuesto = subtotal * Decimal('0.19')  # 19% de IVA - Usar Decimal en lugar de float
    total = subtotal + impuesto + envio
    
    # Crear orden
    orden = Orden.objects.create(
        usuario=request.user,
        numero_orden=numero_orden,
        subtotal=subtotal,
        impuesto=impuesto,
        total=total,
        direccion_envio=form_data['direccion_envio'],
        notas=form_data['notas']
    )
    
    # Crear items de orden y actualizar stock
    for item_carrito in carrito.items.all():
        ItemOrden.objects.create(
            orden=orden,
            producto=item_carrito.producto,
            cantidad=item_carrito.cantidad,
            precio=item_carrito.producto.precio_final,
            subtotal=item_carrito.subtotal
        )
        
        # Actualizar stock
        producto = item_carrito.producto
        producto.stock -= item_carrito.cantidad
        producto.save()
    
    # Vaciar carrito
    carrito.items.all().delete()
    
    messages.success(request, f'¡Orden #{orden.numero_orden} creada exitosamente!')
    return redirect('tienda:detalle_orden', numero_orden=orden.numero_orden)

@login_required
def mis_ordenes(request):
    ordenes = Orden.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    context = {
        'ordenes': ordenes,
    }
    return render(request, 'tienda/mis_ordenes.html', context)

@login_required
def detalle_orden(request, numero_orden):
    orden = get_object_or_404(Orden, numero_orden=numero_orden, usuario=request.user)
    context = {
        'orden': orden,
    }
    return render(request, 'tienda/detalle_orden.html', context)

# Vista para el widget del carrito (AJAX)
@login_required
def carrito_widget(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    return JsonResponse({
        'cantidad_total': carrito.cantidad_total,
        'total': float(carrito.total)
    })

# Esta vista ya no es necesaria - comentada o eliminada
# @login_required
# def crear_orden(request):
#     pass