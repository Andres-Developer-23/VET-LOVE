from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Avg
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.urls import reverse
from .models import Producto, Categoria, Carrito, ItemCarrito, Orden, ItemOrden, Comentario
from .forms import OrdenForm, ComentarioForm
import random
import string
from decimal import Decimal

def lista_productos(request):
    try:
        categorias = Categoria.objects.filter(activo=True)
        productos = Producto.objects.filter(activo=True)

        # Filtros
        categoria_id = request.GET.get('categoria')
        tipo = request.GET.get('tipo')
        tipo_mascota = request.GET.get('tipo_mascota')
        buscar = request.GET.get('buscar')
        categoria_filtro = request.GET.get('categoria_filtro')  # Nuevo filtro para categorías por nombre

        if categoria_id:
            productos = productos.filter(categoria_id=categoria_id)
        if tipo:
            productos = productos.filter(tipo=tipo)
        if tipo_mascota and tipo_mascota != 'todos':
            productos = productos.filter(tipo_mascota=tipo_mascota)
        if buscar:
            productos = productos.filter(nombre__icontains=buscar)
        if categoria_filtro:
            # Filtrar por nombre de categoría (para enlaces desde la página de inicio)
            productos = productos.filter(categoria__nombre__icontains=categoria_filtro)
    except Exception as e:
        # Si hay error con la base de datos, mostrar página sin productos
        categorias = []
        productos = []

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

    # Comentarios del producto
    comentarios = producto.comentarios.filter(aprobado=True).select_related('usuario')
    calificacion_promedio = comentarios.aggregate(Avg('calificacion'))['calificacion__avg'] or 0

    # Formulario de comentario (solo para usuarios autenticados)
    comentario_form = None
    usuario_ha_comentado = False

    if request.user.is_authenticated:
        usuario_ha_comentado = comentarios.filter(usuario=request.user).exists()
        if not usuario_ha_comentado:
            if request.method == 'POST' and 'comentario' in request.POST:
                comentario_form = ComentarioForm(request.POST)
                if comentario_form.is_valid():
                    comentario = comentario_form.save(commit=False)
                    comentario.producto = producto
                    comentario.usuario = request.user
                    comentario.save()
                    messages.success(request, '¡Gracias por tu comentario!')
                    return redirect('tienda:detalle_producto', producto_id=producto_id)
            else:
                comentario_form = ComentarioForm()

    context = {
        'producto': producto,
        'productos_relacionados': productos_relacionados,
        'comentarios': comentarios,
        'calificacion_promedio': calificacion_promedio,
        'comentario_form': comentario_form,
        'usuario_ha_comentado': usuario_ha_comentado,
    }
    return render(request, 'tienda/detalle_producto.html', context)

def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    context = {
        'carrito': carrito,
    }
    return render(request, 'tienda/carrito.html', context)

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

    return redirect('tienda:detalle_producto', producto_id=producto_id)

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

def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    item.delete()
    messages.success(request, 'Producto eliminado del carrito')
    return redirect('tienda:ver_carrito')

def vaciar_carrito(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    carrito.items.all().delete()
    messages.success(request, 'Carrito vaciado')
    return redirect('tienda:ver_carrito')

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
            # Procesar pago con Epayco
            return procesar_pago_epayco(request, form.cleaned_data, carrito)
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

@transaction.atomic
def procesar_pago_epayco(request, form_data, carrito):
    """Procesa el pago con Epayco usando SDK moderno - envío directo de datos"""

    from django.conf import settings

    # Generar número de orden único
    def generar_numero_orden():
        return 'ORD' + ''.join(random.choices(string.digits, k=8))

    numero_orden = generar_numero_orden()
    while Orden.objects.filter(numero_orden=numero_orden).exists():
        numero_orden = generar_numero_orden()

    # Calcular totales (incluyendo envío)
    subtotal = carrito.total
    envio = 0 if subtotal >= 50000 else 5000
    # IVA sobre subtotal + envío
    base_impuesto = subtotal + envio
    impuesto = base_impuesto * Decimal('0.19')  # 19% de IVA
    total = base_impuesto + impuesto

    # Validar rangos de pago permitidos por Epayco
    if total < 1000:
        messages.error(request, 'El total mínimo para pagos en línea es de $1.000 COP.')
        return redirect('tienda:checkout')
    if total > 500000:
        messages.error(request, 'El total de la compra excede el límite máximo permitido para pagos en línea ($500.000 COP). Por favor, contacta con nosotros para procesar tu pedido.')
        return redirect('tienda:checkout')

    # Crear orden pendiente
    orden = Orden.objects.create(
        usuario=request.user,
        numero_orden=numero_orden,
        subtotal=subtotal,
        impuesto=impuesto,
        total=total,
        direccion_envio=form_data['direccion_envio'],
        notas=form_data['notas'],
        estado='pendiente'  # Pendiente hasta confirmar pago
    )

    # Crear items de orden (sin actualizar stock aún)
    for item_carrito in carrito.items.all():
        ItemOrden.objects.create(
            orden=orden,
            producto=item_carrito.producto,
            cantidad=item_carrito.cantidad,
            precio=item_carrito.producto.precio_final,
            subtotal=item_carrito.subtotal
        )

    # URLs de callback
    custom_response_url = getattr(settings, 'EPAYCO_RESPONSE_URL', None)
    custom_confirmation_url = getattr(settings, 'EPAYCO_CONFIRMATION_URL', None)

    if custom_response_url and custom_confirmation_url:
        response_url = f"{custom_response_url.rstrip('/')}/{orden.numero_orden}/"
        confirmation_url = custom_confirmation_url
    else:
        response_url = request.build_absolute_uri(f'/tienda/pago/respuesta/{orden.numero_orden}/')
        confirmation_url = request.build_absolute_uri('/tienda/pago/confirmacion/')

    # Datos del cliente
    cliente = request.user.cliente if hasattr(request.user, 'cliente') else None
    billing_name = request.user.get_full_name() or request.user.username
    billing_email = request.user.email
    billing_address = cliente.direccion if cliente else ''
    billing_phone = cliente.telefono if cliente else ''

    # Preparar datos para el SDK de JavaScript - versión simplificada
    epayco_data = {
        'key': settings.EPAYCO_PUBLIC_KEY,
        'amount': str(int(total)),  # Asegurar que sea entero
        'name': f'Compra Vet Love - Orden {orden.numero_orden}',
        'description': f'Compra en Veterinaria Vet Love - Orden {orden.numero_orden}',
        'currency': 'COP',
        'invoice': orden.numero_orden,
        'country': 'CO',
        'lang': 'es',
        'external': 'false',  # false = iframe, true = popup
        'response': response_url,
        'confirmation': confirmation_url,
        'email_billing': billing_email,
        'name_billing': billing_name,
        'address_billing': billing_address,
        'phone_billing': billing_phone,
        'method_confirmation': 'POST',
        'test': 'true' if settings.EPAYCO_TEST else 'false'
    }

    # Validar que el amount esté en el rango válido de Epayco
    amount_int = int(total)
    if amount_int < 1000 or amount_int > 500000:
        messages.error(request, f'El monto {amount_int} no está en el rango válido para Epayco (1.000 - 500.000 COP).')
        orden.delete()  # Eliminar orden creada si no es válida
        return redirect('tienda:checkout')

    # Renderizar template con datos para SDK
    context = {
        'orden': orden,
        'epayco_data': epayco_data,
        'debug': settings.DEBUG,
    }

    return render(request, 'tienda/pago_epayco_sdk.html', context)

def mis_ordenes(request):
    ordenes = Orden.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    context = {
        'ordenes': ordenes,
    }
    return render(request, 'tienda/mis_ordenes.html', context)

def detalle_orden(request, numero_orden):
    try:
        if request.user.is_staff:
            orden = Orden.objects.get(numero_orden=numero_orden)
        else:
            orden = Orden.objects.get(numero_orden=numero_orden, usuario=request.user)
    except Orden.DoesNotExist:
        messages.error(request, 'No se encontró la orden solicitada o no tienes permiso para verla.')
        return redirect('tienda:mis_ordenes')

    context = {
        'orden': orden,
    }
    return render(request, 'tienda/detalle_orden.html', context)

# Vista para el widget del carrito (AJAX)
def carrito_widget(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    return JsonResponse({
        'cantidad_total': carrito.cantidad_total,
        'total': float(carrito.total)
    })
def respuesta_pago(request, numero_orden):
    """Vista de respuesta para el usuario después del pago"""
    try:
        orden = Orden.objects.get(numero_orden=numero_orden, usuario=request.user)
    except Orden.DoesNotExist:
        messages.error(request, 'Orden no encontrada.')
        return redirect('tienda:mis_ordenes')

    context = {
        'orden': orden,
    }
    return render(request, 'tienda/respuesta_pago.html', context)

def confirmacion_pago(request):
    """Vista de confirmación para Epayco (webhook)"""
    import logging
    logger = logging.getLogger(__name__)

    if request.method == 'POST':
        logger.info("=== RECEIVED EPAYCO CONFIRMATION ===")
        logger.info(f"POST data: {dict(request.POST)}")

        # Datos enviados por Epayco
        x_ref_payco = request.POST.get('x_ref_payco')
        x_transaction_id = request.POST.get('x_transaction_id')
        x_amount = request.POST.get('x_amount')
        x_currency_code = request.POST.get('x_currency_code')
        x_signature = request.POST.get('x_signature')
        x_cod_response = request.POST.get('x_cod_response')
        x_response = request.POST.get('x_response')
        x_response_reason_text = request.POST.get('x_response_reason_text')
        x_reference = request.POST.get('x_reference')  # número de orden

        logger.info(f"Order reference: {x_reference}")
        logger.info(f"Response code: {x_cod_response}")
        logger.info(f"Response: {x_response}")

        # Verificar firma (opcional pero recomendado)
        # Aquí deberías verificar la firma con tu p_key

        try:
            orden = Orden.objects.get(numero_orden=x_reference)
            logger.info(f"Order found: {orden.numero_orden}")

            if x_cod_response == '1':  # Pago aprobado
                logger.info("Payment approved")
                orden.estado = 'confirmada'
                # Actualizar stock
                for item in orden.items.all():
                    producto = item.producto
                    producto.stock -= item.cantidad
                    producto.save()
                    logger.info(f"Stock updated for {producto.nombre}: -{item.cantidad}")

                # Vaciar carrito si existe
                try:
                    carrito = Carrito.objects.get(usuario=orden.usuario)
                    carrito.items.all().delete()
                    logger.info("Cart emptied")
                except Exception as e:
                    logger.warning(f"Could not empty cart: {e}")

            elif x_cod_response == '2':  # Pago rechazado
                logger.info("Payment rejected")
                orden.estado = 'cancelada'
            elif x_cod_response == '3':  # Pago pendiente
                logger.info("Payment pending")
                orden.estado = 'pendiente'
            else:
                logger.warning(f"Unknown response code: {x_cod_response}")
                orden.estado = 'cancelada'

            orden.save()
            logger.info(f"Order status updated to: {orden.estado}")

        except Orden.DoesNotExist:
            logger.error(f"Order not found: {x_reference}")
        except Exception as e:
            logger.error(f"Error processing payment confirmation: {e}")

        return HttpResponse('OK')

    logger.warning("Confirmation received with non-POST method")
    return HttpResponse('Método no permitido', status=405)
@login_required
def consultar_estado_pago(request, numero_orden):
    """Vista para consultar el estado de un pago usando la API de Epayco"""
    try:
        orden = Orden.objects.get(numero_orden=numero_orden, usuario=request.user)
    except Orden.DoesNotExist:
        messages.error(request, 'Orden no encontrada.')
        return redirect('tienda:mis_ordenes')

    # Si la orden ya está confirmada o cancelada, mostrar estado actual
    if orden.estado in ['confirmada', 'cancelada']:
        messages.info(request, f'La orden ya está {orden.get_estado_display()}.')
        return redirect('tienda:detalle_orden', numero_orden=numero_orden)

    # Consultar estado en Epayco usando la API
    from django.conf import settings
    import requests

    try:
        url = 'https://api.secure.epayco.co/transaction/detail'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.EPAYCO_PRIVATE_KEY}'
        }
        data = {
            'filter': {
                'referencePayco': orden.numero_orden  # Usamos el número de orden como referencia
            }
        }

        response = requests.post(url, headers=headers, json=data, timeout=30)

        if response.status_code == 200:
            result = response.json()
            if result.get('success') and result.get('data'):
                transaction_data = result['data']
                status = transaction_data.get('status', '').lower()

                # Actualizar estado de la orden basado en la respuesta de Epayco
                if status == 'aceptada' and orden.estado != 'confirmada':
                    orden.estado = 'confirmada'
                    # Actualizar stock
                    for item in orden.items.all():
                        producto = item.producto
                        producto.stock -= item.cantidad
                        producto.save()
                    # Vaciar carrito
                    try:
                        carrito = Carrito.objects.get(usuario=orden.usuario)
                        carrito.items.all().delete()
                    except:
                        pass
                    orden.save()
                    messages.success(request, '¡Pago confirmado! Tu orden ha sido procesada exitosamente.')

                elif status in ['rechazada', 'cancelada'] and orden.estado != 'cancelada':
                    orden.estado = 'cancelada'
                    orden.save()
                    messages.warning(request, 'El pago fue rechazado o cancelado.')

                else:
                    messages.info(request, f'Estado del pago: {transaction_data.get("response", "Pendiente")}')

            else:
                messages.warning(request, 'No se pudo obtener información del pago.')
        else:
            messages.error(request, f'Error al consultar Epayco: {response.status_code}')

    except requests.RequestException as e:
        messages.error(request, f'Error de conexión con Epayco: {str(e)}')
    except Exception as e:
        messages.error(request, f'Error al procesar la consulta: {str(e)}')

    return redirect('tienda:detalle_orden', numero_orden=numero_orden)


# Esta vista ya no es necesaria - comentada o eliminada
# @login_required
# def crear_orden(request):
#     pass

# Esta vista ya no es necesaria - comentada o eliminada
# @login_required
# def crear_orden(request):
#     pass