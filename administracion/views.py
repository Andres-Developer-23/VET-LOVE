from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q
from django.contrib import messages
from django.http import HttpResponse
import csv
from datetime import datetime

from clientes.models import Cliente
from mascotas.models import Mascota
from citas.models import Cita

def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

@login_required
@staff_required(login_url='/admin/login/')
def dashboard(request):
    # Estadísticas generales
    total_clientes = Cliente.objects.count()
    total_mascotas = Mascota.objects.count()
    
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
    
    context = {
        'total_clientes': total_clientes,
        'total_mascotas': total_mascotas,
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
    }
    
    return render(request, 'administracion/dashboard.html', context)

# views.py - Vista mejorada para exportar a Excel
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

@login_required
@staff_required(login_url='/admin/login/')
def exportar_datos(request):
    if request.method == 'POST':
        # Crear libro de trabajo de Excel
        wb = Workbook()
        
        # Obtener la hoja activa (por defecto se crea una)
        ws = wb.active
        ws.title = "Resumen"
        
        # Estilos
        title_font = Font(bold=True, size=14)
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        centered_alignment = Alignment(horizontal='center')
        
        # Título
        ws['A1'] = 'Dashboard de Administración - Exportación'
        ws['A1'].font = title_font
        ws.merge_cells('A1:B1')
        
        # Fecha de exportación
        ws['A2'] = 'Fecha de exportación:'
        ws['B2'] = timezone.now().strftime("%d/%m/%Y %H:%M")
        
        # Espacio
        ws.append([])
        
        # Estadísticas generales
        ws.append(['Métrica', 'Valor'])
        ws['A4'].font = header_font
        ws['A4'].fill = header_fill
        ws['B4'].font = header_font
        ws['B4'].fill = header_fill
        
        hoy = timezone.now().date()
        
        # Datos de las tarjetas
        datos_estadisticas = [
            ('Total Clientes', Cliente.objects.count()),
            ('Total Mascotas', Mascota.objects.count()),
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
        ]
        
        for idx, (metrica, valor) in enumerate(datos_estadisticas, start=5):
            ws[f'A{idx}'] = metrica
            ws[f'B{idx}'] = valor
        
        # Ajustar anchos de columna
        ws.column_dimensions['A'].width = 30
        ws.column_dimensions['B'].width = 15
        
        # Hoja de citas de hoy
        ws_hoy = wb.create_sheet("Citas Hoy")
        
        ws_hoy.append(['Citas para Hoy'])
        ws_hoy.merge_cells('A1:E1')
        ws_hoy['A1'].font = title_font
        ws_hoy['A1'].alignment = centered_alignment
        
        ws_hoy.append(['Hora', 'Mascota', 'Dueño', 'Tipo', 'Estado'])
        for col in range(1, 6):
            ws_hoy.cell(row=2, column=col).font = header_font
            ws_hoy.cell(row=2, column=col).fill = header_fill
            ws_hoy.cell(row=2, column=col).alignment = centered_alignment
        
        citas_hoy = Cita.objects.filter(
            fecha__date=hoy, 
            estado__in=['programada', 'confirmada']
        ).order_by('fecha')
        
        for cita in citas_hoy:
            ws_hoy.append([
                cita.fecha.time().strftime("%H:%M"),
                cita.mascota.nombre,
                cita.mascota.cliente.usuario.get_full_name(),
                cita.get_tipo_display(),
                cita.get_estado_display()
            ])
        
        # Ajustar anchos de columna para hoja de hoy
        for col in range(1, 6):
            ws_hoy.column_dimensions[get_column_letter(col)].width = 20
        
        # Hoja de próximas citas
        ws_proximas = wb.create_sheet("Próximas Citas")
        
        ws_proximas.append(['Próximas Citas (7 días)'])
        ws_proximas.merge_cells('A1:D1')
        ws_proximas['A1'].font = title_font
        ws_proximas['A1'].alignment = centered_alignment
        
        ws_proximas.append(['Fecha', 'Hora', 'Mascota', 'Tipo', 'Estado'])
        for col in range(1, 6):
            ws_proximas.cell(row=2, column=col).font = header_font
            ws_proximas.cell(row=2, column=col).fill = header_fill
            ws_proximas.cell(row=2, column=col).alignment = centered_alignment
        
        proximas_citas = Cita.objects.filter(
            fecha__date__range=[hoy, hoy + timedelta(days=7)],
            estado__in=['programada', 'confirmada']
        ).order_by('fecha')[:10]
        
        for cita in proximas_citas:
            ws_proximas.append([
                cita.fecha.date().strftime("%d/%m/%Y"),
                cita.fecha.time().strftime("%H:%M"),
                cita.mascota.nombre,
                cita.get_tipo_display(),
                cita.get_estado_display()
            ])
        
        # Ajustar anchos de columna para hoja de próximas citas
        for col in range(1, 6):
            ws_proximas.column_dimensions[get_column_letter(col)].width = 20
        
        # Preparar respuesta
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="dashboard_export_{datetime.now().strftime("%Y%m%d_%H%M")}.xlsx"'
        
        wb.save(response)
        return response
    
    return redirect('administracion:dashboard_admin')