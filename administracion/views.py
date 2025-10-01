from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta, datetime, date
from django.db.models import Count, Q, Sum, F
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import csv
import json
from django.core.serializers.json import DjangoJSONEncoder

from clientes.models import Cliente
from mascotas.models import Mascota
from citas.models import Cita
from tienda.models import Producto, Categoria, Orden
from django.contrib.auth.models import User

def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

@login_required
@staff_required(login_url='/admin/login/')
def dashboard(request):
    hoy = timezone.now().date()
    
    # ESTADÍSTICAS EXISTENTES
    total_clientes = Cliente.objects.count()
    total_mascotas = Mascota.objects.count()
    total_usuarios = User.objects.count()
    
    # Citas
    citas_hoy = Cita.objects.filter(
        fecha__date=hoy, 
        estado__in=['programada', 'confirmada']
    ).select_related('mascota__cliente__usuario').order_by('fecha')
    
    citas_mes = Cita.objects.filter(
        fecha__date__month=hoy.month,
        fecha__date__year=hoy.year
    ).count()
    
    citas_completadas_mes = Cita.objects.filter(
        fecha__date__month=hoy.month,
        fecha__date__year=hoy.year,
        estado='completada'
    ).count()
    
    # Clientes
    clientes_nuevos_mes = Cliente.objects.filter(
        fecha_registro__month=hoy.month,
        fecha_registro__year=hoy.year
    ).count()
    
    # Ingresos (asumiendo que tienes campo precio en Cita)
    try:
        ingresos_mes = Cita.objects.filter(
            fecha__date__month=hoy.month,
            fecha__date__year=hoy.year,
            estado='completada'
        ).aggregate(total=Sum('precio'))['total'] or 0
    except:
        ingresos_mes = 0
    
    # NUEVAS ESTADÍSTICAS DE LA TIENDA
    total_productos = Producto.objects.filter(activo=True).count()
    total_categorias = Categoria.objects.filter(activo=True).count()
    total_ordenes = Orden.objects.count()
    
    # Estadísticas de ventas de la tienda
    try:
        ventas_mes_tienda = Orden.objects.filter(
            fecha_creacion__month=hoy.month,
            fecha_creacion__year=hoy.year,
            estado__in=['entregada', 'enviada', 'en_proceso']
        ).aggregate(total=Sum('total'))['total'] or 0
    except:
        ventas_mes_tienda = 0
    
    ordenes_pendientes = Orden.objects.filter(estado='pendiente').count()
    productos_stock_bajo = Producto.objects.filter(stock__lte=F('stock_minimo'), activo=True).count()
    
    # Órdenes recientes
    ordenes_recientes = Orden.objects.select_related('usuario').order_by('-fecha_creacion')[:5]
    
    # Productos destacados
    productos_destacados = Producto.objects.filter(destacado=True, activo=True)[:5]
    
    # Productos con stock bajo
    productos_bajo_stock = Producto.objects.filter(
        stock__lte=F('stock_minimo'), 
        activo=True
    ).order_by('stock')[:5]
    
    # DATOS PARA GRÁFICOS EXISTENTES
    # Citas por estado
    citas_por_estado = list(Cita.objects.values('estado').annotate(
        total=Count('id')
    ).order_by('-total'))
    
    # Mascotas por tipo
    mascotas_por_tipo = list(Mascota.objects.values('tipo').annotate(
        total=Count('id')
    ).order_by('-total'))
    
    # Citas últimos 7 días
    citas_ultimos_7_dias = []
    for i in range(6, -1, -1):
        dia = hoy - timedelta(days=i)
        count = Cita.objects.filter(fecha__date=dia).count()
        citas_ultimos_7_dias.append({
            'dia': dia.strftime('%d/%m'),
            'total': count
        })
    
    # NUEVOS DATOS PARA GRÁFICOS DE TIENDA
    # Productos por categoría
    productos_por_categoria = list(Producto.objects.filter(activo=True).values(
        'categoria__nombre'
    ).annotate(
        total=Count('id')
    ).order_by('-total'))
    
    # Órdenes por estado
    ordenes_por_estado = list(Orden.objects.values('estado').annotate(
        total=Count('id')
    ).order_by('-total'))
    
    # Ventas últimos 7 días (tienda)
    ventas_ultimos_7_dias = []
    for i in range(6, -1, -1):
        dia = hoy - timedelta(days=i)
        ventas_dia = Orden.objects.filter(
            fecha_creacion__date=dia,
            estado__in=['entregada', 'enviada', 'en_proceso']
        ).aggregate(total=Sum('total'))['total'] or 0
        ventas_ultimos_7_dias.append({
            'dia': dia.strftime('%d/%m'),
            'total': float(ventas_dia)
        })
    
    # Próximas citas
    proximas_citas = Cita.objects.filter(
        fecha__date__gte=hoy,
        estado__in=['programada', 'confirmada']
    ).select_related('mascota__cliente__usuario').order_by('fecha')[:10]
    
    # Citas urgentes
    citas_urgentes = Cita.objects.filter(
        fecha__date=hoy,
        tipo='urgencia',
        estado__in=['programada', 'confirmada']
    ).count()

    context = {
        # ESTADÍSTICAS EXISTENTES
        'total_clientes': total_clientes,
        'total_mascotas': total_mascotas,
        'total_usuarios': total_usuarios,
        'citas_mes': citas_mes,
        'citas_completadas_mes': citas_completadas_mes,
        'clientes_nuevos_mes': clientes_nuevos_mes,
        'ingresos_mes': ingresos_mes,
        'citas_urgentes': citas_urgentes,
        
        # NUEVAS ESTADÍSTICAS TIENDA
        'total_productos': total_productos,
        'total_categorias': total_categorias,
        'total_ordenes': total_ordenes,
        'ventas_mes_tienda': ventas_mes_tienda,
        'ordenes_pendientes': ordenes_pendientes,
        'productos_stock_bajo': productos_stock_bajo,
        'ordenes_recientes': ordenes_recientes,
        'productos_destacados': productos_destacados,
        'productos_bajo_stock': productos_bajo_stock,
        
        # LISTAS EXISTENTES
        'citas_hoy': citas_hoy,
        'proximas_citas': proximas_citas,
        
        # DATOS PARA GRÁFICOS EXISTENTES
        'citas_por_estado_json': json.dumps(citas_por_estado, cls=DjangoJSONEncoder),
        'mascotas_por_tipo_json': json.dumps(mascotas_por_tipo, cls=DjangoJSONEncoder),
        'citas_ultimos_7_dias_json': json.dumps(citas_ultimos_7_dias, cls=DjangoJSONEncoder),
        
        # NUEVOS DATOS PARA GRÁFICOS DE TIENDA
        'productos_por_categoria_json': json.dumps(productos_por_categoria, cls=DjangoJSONEncoder),
        'ordenes_por_estado_json': json.dumps(ordenes_por_estado, cls=DjangoJSONEncoder),
        'ventas_ultimos_7_dias_json': json.dumps(ventas_ultimos_7_dias, cls=DjangoJSONEncoder),
        
        # FECHAS EXISTENTES
        'hoy': hoy,
        'mes_actual': hoy.strftime('%B %Y'),
    }
    
    return render(request, 'administracion/dashboard.html', context)

@login_required
@staff_required(login_url='/admin/login/')
def exportar_datos(request):
    if request.method == 'POST':
        # Crear respuesta Excel (CSV con formato mejorado)
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="reporte_admin_{date.today().strftime("%Y%m%d")}.csv"'
        
        response.write('\ufeff')  # BOM para UTF-8 en Excel
        writer = csv.writer(response, delimiter=';')
        
        # Encabezado del reporte
        writer.writerow(['Reporte de Administración - Veterinaria Vet Love'])
        writer.writerow(['Fecha de generación:', datetime.now().strftime("%d/%m/%Y %H:%M:%S")])
        writer.writerow(['Generado por:', request.user.get_full_name() or request.user.username])
        writer.writerow([])
        
        # Estadísticas generales
        writer.writerow(['ESTADÍSTICAS GENERALES'])
        writer.writerow(['Métrica', 'Valor'])
        writer.writerow(['Total de Clientes', Cliente.objects.count()])
        writer.writerow(['Total de Mascotas', Mascota.objects.count()])
        writer.writerow(['Total de Usuarios', User.objects.count()])
        writer.writerow(['Total de Productos', Producto.objects.filter(activo=True).count()])
        writer.writerow(['Total de Categorías', Categoria.objects.filter(activo=True).count()])
        writer.writerow(['Total de Órdenes', Orden.objects.count()])
        writer.writerow([])
        
        # Estadísticas del mes
        hoy = timezone.now().date()
        writer.writerow(['ESTADÍSTICAS DEL MES ACTUAL'])
        writer.writerow(['Métrica', 'Valor'])
        writer.writerow(['Citas este mes', Cita.objects.filter(
            fecha__date__month=hoy.month, fecha__date__year=hoy.year).count()])
        writer.writerow(['Citas completadas', Cita.objects.filter(
            fecha__date__month=hoy.month, fecha__date__year=hoy.year, estado='completada').count()])
        writer.writerow(['Clientes nuevos', Cliente.objects.filter(
            fecha_registro__month=hoy.month, fecha_registro__year=hoy.year).count()])
        
        # Estadísticas de tienda del mes
        ventas_mes = Orden.objects.filter(
            fecha_creacion__month=hoy.month, 
            fecha_creacion__year=hoy.year
        ).aggregate(total=Sum('total'))['total'] or 0
        writer.writerow(['Ventas tienda', ventas_mes])
        writer.writerow(['Órdenes tienda', Orden.objects.filter(
            fecha_creacion__month=hoy.month, fecha_creacion__year=hoy.year).count()])
        writer.writerow([])
        
        # Citas por estado
        writer.writerow(['CITAS POR ESTADO'])
        writer.writerow(['Estado', 'Cantidad'])
        for estado in Cita.objects.values('estado').annotate(total=Count('id')):
            writer.writerow([estado['estado'], estado['total']])
        writer.writerow([])
        
        # Mascotas por tipo
        writer.writerow(['MASCOTAS POR TIPO'])
        writer.writerow(['Tipo', 'Cantidad'])
        for tipo in Mascota.objects.values('tipo').annotate(total=Count('id')):
            writer.writerow([tipo['tipo'], tipo['total']])
        writer.writerow([])
        
        # Productos por categoría
        writer.writerow(['PRODUCTOS POR CATEGORÍA'])
        writer.writerow(['Categoría', 'Cantidad'])
        for cat in Producto.objects.filter(activo=True).values('categoria__nombre').annotate(total=Count('id')):
            writer.writerow([cat['categoria__nombre'], cat['total']])
        writer.writerow([])
        
        # Órdenes por estado
        writer.writerow(['ÓRDENES POR ESTADO'])
        writer.writerow(['Estado', 'Cantidad'])
        for estado in Orden.objects.values('estado').annotate(total=Count('id')):
            writer.writerow([estado['estado'], estado['total']])
        writer.writerow([])
        
        # Productos con stock bajo
        productos_bajo_stock = Producto.objects.filter(stock__lte=F('stock_minimo'), activo=True)
        writer.writerow(['PRODUCTOS CON STOCK BAJO'])
        writer.writerow(['Producto', 'Stock Actual', 'Stock Mínimo'])
        for producto in productos_bajo_stock:
            writer.writerow([producto.nombre, producto.stock, producto.stock_minimo])
        writer.writerow([])
        
        # Citas de hoy
        writer.writerow(['CITAS PARA HOY'])
        writer.writerow(['Hora', 'Mascota', 'Dueño', 'Tipo', 'Estado'])
        for cita in Cita.objects.filter(fecha__date=hoy).select_related('mascota__cliente__usuario'):
            writer.writerow([
                cita.fecha.strftime("%H:%M"),
                cita.mascota.nombre,
                cita.mascota.cliente.usuario.get_full_name() or cita.mascota.cliente.usuario.username,
                cita.tipo,
                cita.estado
            ])
        writer.writerow([])
        
        # Órdenes pendientes
        writer.writerow(['ÓRDENES PENDIENTES'])
        writer.writerow(['Número Orden', 'Cliente', 'Total', 'Fecha'])
        for orden in Orden.objects.filter(estado='pendiente').select_related('usuario'):
            writer.writerow([
                orden.numero_orden,
                orden.usuario.get_full_name() or orden.usuario.username,
                orden.total,
                orden.fecha_creacion.strftime("%d/%m/%Y")
            ])
        writer.writerow([])
        
        # Productos destacados
        writer.writerow(['PRODUCTOS DESTACADOS'])
        writer.writerow(['Producto', 'Precio', 'Stock', 'Categoría'])
        for producto in Producto.objects.filter(destacado=True, activo=True):
            writer.writerow([
                producto.nombre,
                producto.precio,
                producto.stock,
                producto.categoria.nombre
            ])
        
        return response
    
    return redirect('administracion:dashboard_admin')

@login_required
@staff_required(login_url='/admin/login/')
def estadisticas_api(request):
    if request.method == 'GET':
        hoy = timezone.now().date()
        
        # Citas por día de la semana (últimas 4 semanas)
        datos_semana = []
        dias_semana = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
        
        for i in range(7):
            # Promedio de las últimas 4 semanas para este día
            citas_dia = Cita.objects.filter(
                fecha__week_day=i+2,  # Django: 2=Lunes, 3=Martes, etc.
                fecha__date__gte=hoy - timedelta(weeks=4)
            ).count()
            promedio = citas_dia / 4
            
            datos_semana.append({
                'dia': dias_semana[i],
                'promedio': round(promedio, 1)
            })
        
        # Citas últimos 30 días
        citas_30_dias = []
        for i in range(29, -1, -1):
            fecha = hoy - timedelta(days=i)
            count = Cita.objects.filter(fecha__date=fecha).count()
            citas_30_dias.append({
                'fecha': fecha.strftime('%d/%m'),
                'total': count
            })
        
        # Ventas últimos 30 días (tienda)
        ventas_30_dias = []
        for i in range(29, -1, -1):
            fecha = hoy - timedelta(days=i)
            ventas_dia = Orden.objects.filter(
                fecha_creacion__date=fecha,
                estado__in=['entregada', 'enviada', 'en_proceso']
            ).aggregate(total=Sum('total'))['total'] or 0
            ventas_30_dias.append({
                'fecha': fecha.strftime('%d/%m'),
                'total': float(ventas_dia)
            })
        
        return JsonResponse({
            'citas_semana': datos_semana,
            'citas_30_dias': citas_30_dias,
            'ventas_30_dias': ventas_30_dias,
            'mascotas_tipo': list(Mascota.objects.values('tipo').annotate(total=Count('id'))),
            'citas_estado': list(Cita.objects.values('estado').annotate(total=Count('id'))),
            'productos_categoria': list(Producto.objects.filter(activo=True).values('categoria__nombre').annotate(total=Count('id'))),
            'ordenes_estado': list(Orden.objects.values('estado').annotate(total=Count('id')))
        })