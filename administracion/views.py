from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import Count, Q, Sum
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import csv
from datetime import datetime

from clientes.models import Cliente
from mascotas.models import Mascota
from citas.models import Cita
from django.contrib.auth.models import User

def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

@login_required
@staff_required(login_url='/admin/login/')
def dashboard(request):
    # Estadísticas generales
    total_clientes = Cliente.objects.count()
    total_mascotas = Mascota.objects.count()
    total_usuarios = User.objects.count()
    
    # Citas de hoy
    hoy = timezone.now().date()
    citas_hoy = Cita.objects.filter(
        fecha__date=hoy, 
        estado__in=['programada', 'confirmada']
    ).order_by('fecha')
    
    # Citas de la semana
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    fin_semana = inicio_semana + timedelta(days=6)
    citas_semana_count = Cita.objects.filter(
        fecha__date__range=[inicio_semana, fin_semana]
    ).count()
    
    # Próximas citas (próximos 7 días)
    proximas_citas = Cita.objects.filter(
        fecha__date__range=[hoy, hoy + timedelta(days=7)],
        estado__in=['programada', 'confirmada']
    ).order_by('fecha')[:10]
    
    # Citas por estado
    citas_por_estado = Cita.objects.values('estado').annotate(total=Count('id'))
    
    # Mascotas por tipo
    mascotas_por_tipo = Mascota.objects.values('tipo').annotate(total=Count('id'))
    
    # Clientes recientes (últimos 7 días)
    clientes_recientes = Cliente.objects.filter(
        fecha_registro__date__gte=hoy - timedelta(days=7)
    ).count()
    
    # Citas urgentes (hoy y mañana)
    citas_urgentes = Cita.objects.filter(
        fecha__date__range=[hoy, hoy + timedelta(days=1)],
        estado__in=['programada', 'confirmada'],
        tipo='urgencia'
    ).count()
    
    # Usuarios activos hoy
    usuarios_activos_hoy = User.objects.filter(
        last_login__date=hoy
    ).count()
    
    # Citas pendientes
    citas_pendientes = Cita.objects.filter(
        estado='programada',
        fecha__date__gte=hoy
    ).count()
    
    # Estadísticas mensuales
    primer_dia_mes = hoy.replace(day=1)
    citas_este_mes = Cita.objects.filter(
        fecha__date__gte=primer_dia_mes
    ).count()
    
    clientes_este_mes = Cliente.objects.filter(
        fecha_registro__date__gte=primer_dia_mes
    ).count()

    context = {
        'total_clientes': total_clientes,
        'total_mascotas': total_mascotas,
        'total_usuarios': total_usuarios,
        'citas_hoy': citas_hoy,
        'citas_semana_count': citas_semana_count,
        'proximas_citas': proximas_citas,
        'citas_por_estado': citas_por_estado,
        'mascotas_por_tipo': mascotas_por_tipo,
        'clientes_recientes': clientes_recientes,
        'citas_urgentes': citas_urgentes,
        'hoy': hoy,
        'inicio_semana': inicio_semana,
        'fin_semana': fin_semana,
        'usuarios_activos_hoy': usuarios_activos_hoy,
        'citas_pendientes': citas_pendientes,
        'citas_este_mes': citas_este_mes,
        'clientes_este_mes': clientes_este_mes,
    }
    
    return render(request, 'administracion/dashboard.html', context)

@login_required
@staff_required(login_url='/admin/login/')
def exportar_datos(request):
    if request.method == 'POST':
        # Crear respuesta CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="dashboard_export_{}.csv"'.format(
            datetime.now().strftime("%Y%m%d_%H%M")
        )
        
        writer = csv.writer(response)
        
        # Escribir encabezados
        writer.writerow(['Dashboard de Administración - Exportación'])
        writer.writerow(['Fecha de exportación:', datetime.now().strftime("%d/%m/%Y %H:%M")])
        writer.writerow([])
        writer.writerow(['Métrica', 'Valor'])
        
        # Obtener datos
        hoy = timezone.now().date()
        
        datos_estadisticas = [
            ('Total Clientes', Cliente.objects.count()),
            ('Total Mascotas', Mascota.objects.count()),
            ('Total Usuarios', User.objects.count()),
            ('Citas Hoy', Cita.objects.filter(fecha__date=hoy, estado__in=['programada', 'confirmada']).count()),
            ('Citas Esta Semana', Cita.objects.filter(
                fecha__date__range=[hoy - timedelta(days=hoy.weekday()), hoy + timedelta(days=6 - hoy.weekday())]
            ).count()),
            ('Clientes Recientes (7 días)', Cliente.objects.filter(fecha_registro__date__gte=hoy - timedelta(days=7)).count()),
            ('Citas Urgentes', Cita.objects.filter(
                fecha__date__range=[hoy, hoy + timedelta(days=1)],
                estado__in=['programada', 'confirmada'],
                tipo='urgencia'
            ).count()),
            ('Usuarios Activos Hoy', User.objects.filter(last_login__date=hoy).count()),
            ('Citas Pendientes', Cita.objects.filter(estado='programada', fecha__date__gte=hoy).count()),
        ]
        
        # Escribir datos
        for metrica, valor in datos_estadisticas:
            writer.writerow([metrica, valor])
        
        return response
    
    return redirect('administracion:dashboard_admin')

@login_required
@staff_required(login_url='/admin/login/')
def estadisticas_api(request):
    # API para gráficos y estadísticas
    if request.method == 'GET':
        # Datos para gráfico de citas por día de la semana
        hoy = timezone.now().date()
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        
        citas_por_dia = []
        for i in range(7):
            dia = inicio_semana + timedelta(days=i)
            count = Cita.objects.filter(fecha__date=dia).count()
            citas_por_dia.append({
                'dia': dia.strftime('%A'),
                'count': count
            })
        
        # Datos para gráfico de mascotas por tipo
        mascotas_tipo = Mascota.objects.values('tipo').annotate(total=Count('id'))
        
        return JsonResponse({
            'citas_por_dia': citas_por_dia,
            'mascotas_tipo': list(mascotas_tipo)
        })