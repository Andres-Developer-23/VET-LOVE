from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
from PIL import Image as PILImage
import os
from .models import Mascota, HistorialMedico, Vacuna
from .forms import MascotaForm, HistorialMedicoForm, VacunaForm
from datetime import date, timedelta

def lista_mascotas(request):
    """
    Lista todas las mascotas del cliente autenticado.
    Los administradores pueden ver todas las mascotas o solo las suyas si tienen perfil.

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse: Rendered template with mascotas list
    """
    es_admin = request.user.is_staff or request.user.is_superuser
    
    if es_admin:
        # Administradores ven todas las mascotas
        mascotas = Mascota.objects.all().select_related('cliente__usuario')
        es_cliente = False
    else:
        # Clientes solo ven sus mascotas
        cliente = request.user.cliente
        mascotas = Mascota.objects.filter(cliente=cliente).select_related('cliente')
        es_cliente = True
    
    return render(request, 'mascotas/lista_mascotas.html', {
        'mascotas': mascotas,
        'es_cliente': es_cliente,
        'es_admin': es_admin
    })

def agregar_mascota(request):
    # Verificar que el usuario tenga perfil de cliente
    if not hasattr(request.user, 'cliente'):
        messages.warning(request, 'Debes completar tu perfil de cliente antes de agregar mascotas.')
        return redirect('clientes:crear_perfil_cliente')
    
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.cliente = request.user.cliente
            mascota.save()
            messages.success(request, f'{mascota.nombre} ha sido registrado(a) correctamente en el sistema veterinario.')
            return redirect('mascotas:lista_mascotas')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = MascotaForm()
    
    return render(request, 'mascotas/agregar_mascota.html', {
        'form': form,
        'titulo': 'Registro de Nueva Mascota'
    })

def detalle_mascota(request, mascota_id):
    """
    Muestra el detalle completo de una mascota incluyendo historial médico,
    vacunas y citas programadas.

    Args:
        request: HttpRequest object
        mascota_id: ID de la mascota

    Returns:
        HttpResponse: Rendered template with mascota details
    """
    mascota = get_object_or_404(
        Mascota.objects.select_related('cliente'),
        id=mascota_id
    )

    # Verificar permisos: administradores pueden ver todas, clientes solo las suyas
    es_admin = request.user.is_staff or request.user.is_superuser
    if not es_admin:
        if not hasattr(request.user, 'cliente') or mascota.cliente != request.user.cliente:
            return HttpResponseForbidden("No tienes permiso para ver esta mascota")

    # Usar prefetch_related para optimizar consultas
    mascota = Mascota.objects.prefetch_related(
        'historial_medico',
        'vacunas',
        'citas'
    ).get(id=mascota_id)

    # Calcular fechas del carnet
    fecha_expedicion = timezone.now()
    fecha_vencimiento = fecha_expedicion + timedelta(days=730)

    return render(request, 'mascotas/detalle_mascota.html', {
        'mascota': mascota,
        'historial': mascota.historial_medico.all(),
        'vacunas': mascota.vacunas.all(),
        'citas': getattr(mascota, 'citas', None).all() if hasattr(mascota, 'citas') else [],
        'fecha_expedicion': fecha_expedicion.strftime('%d/%m/%Y'),
        'fecha_vencimiento': fecha_vencimiento.strftime('%d/%m/%Y'),
        'es_admin': es_admin
    })

def editar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)

    # Verificar permisos: administradores pueden editar todas, clientes solo las suyas
    es_admin = request.user.is_staff or request.user.is_superuser
    if not es_admin:
        if not hasattr(request.user, 'cliente') or mascota.cliente != request.user.cliente:
            return HttpResponseForbidden("No tienes permiso para editar esta mascota")

    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES, instance=mascota)
        if form.is_valid():
            form.save()
            messages.success(request, f'La información de {mascota.nombre} ha sido actualizada en el sistema.')
            return redirect('mascotas:detalle_mascota', mascota_id=mascota.id)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = MascotaForm(instance=mascota)

    return render(request, 'mascotas/editar_mascota.html', {
        'form': form,
        'mascota': mascota,
        'titulo': 'Editar Información de Mascota'
    })

def eliminar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)

    # Verificar permisos: administradores pueden eliminar todas, clientes solo las suyas
    es_admin = request.user.is_staff or request.user.is_superuser
    if not es_admin:
        if not hasattr(request.user, 'cliente') or mascota.cliente != request.user.cliente:
            return HttpResponseForbidden("No tienes permiso para eliminar esta mascota")

    if request.method == 'POST':
        nombre = mascota.nombre
        mascota.delete()
        messages.success(request, f'{nombre} ha sido eliminado(a) del sistema veterinario.')
        return redirect('mascotas:lista_mascotas')

    return render(request, 'mascotas/eliminar_mascota.html', {'mascota': mascota})

def agregar_historial(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)

    # Verificar permisos: administradores pueden agregar a todas, clientes solo a las suyas
    es_admin = request.user.is_staff or request.user.is_superuser
    if not es_admin:
        if not hasattr(request.user, 'cliente') or mascota.cliente != request.user.cliente:
            return HttpResponseForbidden("No tienes permiso para agregar historial a esta mascota")

    if request.method == 'POST':
        form = HistorialMedicoForm(request.POST)
        if form.is_valid():
            historial = form.save(commit=False)
            historial.mascota = mascota
            historial.save()
            messages.success(request, 'El historial médico ha sido registrado correctamente.')
            return redirect('mascotas:detalle_mascota', mascota_id=mascota.id)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = HistorialMedicoForm()

    return render(request, 'mascotas/agregar_historial.html', {
        'form': form,
        'mascota': mascota,
        'titulo': 'Nuevo Registro Médico'
    })

def agregar_vacuna(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)

    # Verificar permisos: administradores pueden agregar a todas, clientes solo a las suyas
    es_admin = request.user.is_staff or request.user.is_superuser
    if not es_admin:
        if not hasattr(request.user, 'cliente') or mascota.cliente != request.user.cliente:
            return HttpResponseForbidden("No tienes permiso para agregar vacunas a esta mascota")

    if request.method == 'POST':
        form = VacunaForm(request.POST)
        if form.is_valid():
            vacuna = form.save(commit=False)
            vacuna.mascota = mascota
            vacuna.save()
            messages.success(request, 'La vacuna ha sido registrada correctamente en el cartón de vacunación.')
            return redirect('mascotas:detalle_mascota', mascota_id=mascota.id)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = VacunaForm()

    return render(request, 'mascotas/agregar_vacuna.html', {
        'form': form,
        'mascota': mascota,
        'titulo': 'Registrar Nueva Vacuna'
    })

def calendario_vacunas(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)

    # Verificar permisos: administradores pueden ver todas, clientes solo las suyas
    es_admin = request.user.is_staff or request.user.is_superuser
    if not es_admin:
        if not hasattr(request.user, 'cliente') or mascota.cliente != request.user.cliente:
            return JsonResponse({'error': 'No autorizado'}, status=403)

    eventos = []
    hoy = date.today()

    for v in mascota.vacunas.all():
        # Evento de aplicación (pasado o presente)
        if v.fecha_aplicacion:
            eventos.append({
                'title': f'Aplicación: {v.nombre}',
                'start': v.fecha_aplicacion.isoformat(),
                'allDay': True,
                'color': '#198754' if v.aplicada else '#6c757d'
            })
        # Evento de próxima dosis (futuro o vencido)
        if v.fecha_proxima:
            color = '#fd7e14'  # naranja por defecto
            if v.fecha_proxima < hoy:
                color = '#dc3545'  # rojo si vencida
            eventos.append({
                'title': f'Próxima dosis: {v.nombre}',
                'start': v.fecha_proxima.isoformat(),
                'allDay': True,
                'color': color
            })

    return JsonResponse(eventos, safe=False)

def descargar_carnet_pdf(request, mascota_id):
    """
    Genera y descarga el carnet de vacunación como PDF usando ReportLab
    con el estilo visual del carnet oficial
    """
    mascota = get_object_or_404(Mascota, id=mascota_id)

    # Verificar permisos
    es_admin = request.user.is_staff or request.user.is_superuser
    if not es_admin:
        if not hasattr(request.user, 'cliente') or mascota.cliente != request.user.cliente:
            return HttpResponseForbidden("No tienes permiso para descargar este carnet")

    # Crear buffer para el PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    width, height = A4
    elements = []

    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1,  # Centrado
        textColor=colors.black
    )

    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=15,
        textColor=colors.black
    )

    normal_style = styles['Normal']
    normal_style.fontSize = 10

    # Título principal
    title = Paragraph("CARNET DE VACUNACIÓN", title_style)
    elements.append(title)

    # Información de la mascota
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("DATOS DEL ANIMAL", section_style))

    # Crear tabla de información de la mascota
    mascota_data = [
        ['Nombre:', mascota.nombre.upper()],
        ['Especie:', mascota.get_tipo_display().upper()],
        ['Raza:', (mascota.raza or 'MESTIZO').upper()],
        ['Sexo:', mascota.get_sexo_display().upper()],
        ['Color:', (mascota.color or 'NO ESPECIFICADO').upper()],
        ['Fecha Nacimiento:', mascota.fecha_nacimiento.strftime('%d/%m/%Y') if mascota.fecha_nacimiento else 'NO REGISTRA'],
    ]

    mascota_table = Table(mascota_data, colWidths=[120, 200])
    mascota_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(mascota_table)

    # Información del propietario
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("DATOS DEL PROPIETARIO", section_style))

    propietario_data = [
        ['Nombre:', (mascota.cliente.usuario.get_full_name() or mascota.cliente.usuario.username).upper()],
        ['Documento:', 'NO REGISTRA'],
        ['Dirección:', (mascota.cliente.direccion or 'NO REGISTRA').upper()],
        ['Teléfono:', (mascota.cliente.telefono or 'NO REGISTRA')],
    ]

    propietario_table = Table(propietario_data, colWidths=[120, 200])
    propietario_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(propietario_table)

    # Tabla de vacunas
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("REGISTRO DE VACUNACIÓN", section_style))

    # Encabezados de la tabla de vacunas
    vaccine_headers = ['Vacuna', 'Fecha Aplicación', 'Próxima Dosis', 'Lote', 'Laboratorio', 'Estado']

    # Datos de vacunas existentes
    vaccine_data = [vaccine_headers]

    for vacuna in mascota.vacunas.all():
        vaccine_data.append([
            vacuna.nombre,
            vacuna.fecha_aplicacion.strftime('%d/%m/%Y') if vacuna.fecha_aplicacion else '-',
            vacuna.fecha_proxima.strftime('%d/%m/%Y') if vacuna.fecha_proxima else '-',
            vacuna.lote or '-',
            vacuna.laboratorio or '-',
            'Aplicada' if vacuna.aplicada else 'Pendiente'
        ])

    # Agregar filas vacías para llenado manual
    for i in range(10):
        vaccine_data.append(['______________________________', '____/____/______', '____/____/______', '________________', '________________', 'Pendiente'])

    # Crear tabla de vacunas
    vaccine_table = Table(vaccine_data, colWidths=[80, 70, 70, 60, 70, 60])

    # Estilo de tabla Excel-like
    vaccine_table.setStyle(TableStyle([
        # Encabezado
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.8, 0.8, 0.8)),  # Gris claro
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),

        # Filas de datos
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),

        # Bordes de toda la tabla
        ('GRID', (0, 0), (-1, -1), 1, colors.black),

        # Filas alternas
        ('BACKGROUND', (0, 2), (-1, 2), colors.Color(0.95, 0.95, 0.95)),
        ('BACKGROUND', (0, 4), (-1, 4), colors.Color(0.95, 0.95, 0.95)),
        ('BACKGROUND', (0, 6), (-1, 6), colors.Color(0.95, 0.95, 0.95)),
        ('BACKGROUND', (0, 8), (-1, 8), colors.Color(0.95, 0.95, 0.95)),
        ('BACKGROUND', (0, 10), (-1, 10), colors.Color(0.95, 0.95, 0.95)),
    ]))

    elements.append(vaccine_table)

    # Información de expedición
    elements.append(Spacer(1, 30))

    expedicion_data = [
        ['Fecha de Expedición:', timezone.now().strftime('%d/%m/%Y')],
        ['Fecha de Vencimiento:', (timezone.now() + timedelta(days=730)).strftime('%d/%m/%Y')],
        ['Expedido por:', 'VETERINARIA VET LOVE'],
        ['Registro:', 'LOCAL DE MASCOTAS'],
    ]

    expedicion_table = Table(expedicion_data, colWidths=[120, 200])
    expedicion_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(expedicion_table)

    # Pie de página
    elements.append(Spacer(1, 20))
    footer_text = f"Documento oficial - ID: {mascota.id:08d} - Emitido: {timezone.now().strftime('%d/%m/%Y %H:%M')}"
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=1
    )
    elements.append(Paragraph(footer_text, footer_style))

    # Generar PDF
    doc.build(elements)

    # Preparar respuesta
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Carnet_Vacunacion_{mascota.nombre}.pdf"'

    return response


def descargar_plantilla_carnet_pdf(request, mascota_id):
    """
    Genera y descarga una plantilla del carnet de vacunación con celdas vacías
    para llenado físico usando ReportLab
    """
    mascota = get_object_or_404(Mascota, id=mascota_id)

    # Verificar permisos (solo administradores)
    es_admin = request.user.is_staff or request.user.is_superuser
    if not es_admin:
        return HttpResponseForbidden("Solo los administradores pueden descargar plantillas")

    # Crear buffer para el PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    width, height = A4
    elements = []

    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1,  # Centrado
        textColor=colors.black
    )

    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=15,
        textColor=colors.black
    )

    normal_style = styles['Normal']
    normal_style.fontSize = 10

    # Título principal
    title = Paragraph("PLANTILLA - CARNET DE VACUNACIÓN", title_style)
    elements.append(title)

    # Información de la mascota
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("DATOS DEL ANIMAL", section_style))

    # Crear tabla de información de la mascota
    mascota_data = [
        ['Nombre:', mascota.nombre.upper()],
        ['Especie:', mascota.get_tipo_display().upper()],
        ['Raza:', (mascota.raza or 'MESTIZO').upper()],
        ['Sexo:', mascota.get_sexo_display().upper()],
        ['Color:', (mascota.color or 'NO ESPECIFICADO').upper()],
        ['Fecha Nacimiento:', mascota.fecha_nacimiento.strftime('%d/%m/%Y') if mascota.fecha_nacimiento else 'NO REGISTRA'],
    ]

    mascota_table = Table(mascota_data, colWidths=[120, 200])
    mascota_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(mascota_table)

    # Información del propietario
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("DATOS DEL PROPIETARIO", section_style))

    propietario_data = [
        ['Nombre:', (mascota.cliente.usuario.get_full_name() or mascota.cliente.usuario.username).upper()],
        ['Documento:', '____________________'],
        ['Dirección:', (mascota.cliente.direccion or '____________________').upper()],
        ['Teléfono:', (mascota.cliente.telefono or '____________________')],
    ]

    propietario_table = Table(propietario_data, colWidths=[120, 200])
    propietario_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(propietario_table)

    # Tabla de vacunas VACÍA para llenado manual
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("REGISTRO DE VACUNACIÓN - LLENAR MANUALMENTE", section_style))

    # Encabezados de la tabla de vacunas
    vaccine_headers = ['Vacuna', 'Fecha Aplicación', 'Próxima Dosis', 'Lote', 'Laboratorio', 'Estado']

    # SOLO filas vacías para llenado manual
    vaccine_data = [vaccine_headers]

    # Generar más filas vacías (20 filas para llenado físico)
    for i in range(20):
        vaccine_data.append([
            '______________________________',
            '____/____/______',
            '____/____/______',
            '________________',
            '________________',
            '☐ Aplicada ☐ Pendiente'
        ])

    # Crear tabla de vacunas
    vaccine_table = Table(vaccine_data, colWidths=[80, 70, 70, 60, 70, 60])

    # Estilo de tabla Excel-like con líneas más gruesas para fácil llenado
    vaccine_table.setStyle(TableStyle([
        # Encabezado
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.8, 0.8, 0.8)),  # Gris claro
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),

        # Filas vacías para llenado manual
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 12),  # Más espacio para escritura

        # Bordes más gruesos para fácil identificación
        ('GRID', (0, 0), (-1, -1), 1.5, colors.black),

        # Líneas internas más visibles
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    elements.append(vaccine_table)

    # Instrucciones para llenado manual
    elements.append(Spacer(1, 15))
    instrucciones_style = ParagraphStyle(
        'Instrucciones',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.black,
        spaceAfter=15
    )

    instrucciones = """
    <b>INSTRUCCIONES PARA LLENADO MANUAL:</b><br/>
    • Complete cada fila con la información de cada vacuna aplicada<br/>
    • Use bolígrafo negro o azul para mejor legibilidad<br/>
    • Marque ✓ en "Estado" cuando la vacuna sea aplicada<br/>
    • Complete lote y laboratorio con la información del fabricante<br/>
    • Este documento es oficial y debe conservarse en lugar fresco y seco
    """

    elements.append(Paragraph(instrucciones, instrucciones_style))

    # Información de expedición
    elements.append(Spacer(1, 20))

    expedicion_data = [
        ['Fecha de Expedición:', '____/____/________'],
        ['Fecha de Vencimiento:', '____/____/________'],
        ['Expedido por:', 'VETERINARIA VET LOVE'],
        ['Registro:', 'LOCAL DE MASCOTAS'],
    ]

    expedicion_table = Table(expedicion_data, colWidths=[120, 200])
    expedicion_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(expedicion_table)

    # Espacio para firma y sello
    elements.append(Spacer(1, 30))

    firma_data = [
        ['Firma del Veterinario:', '_______________________________', 'Sello Profesional:', '_______________'],
        ['', '', '', ''],
        ['Fecha:', '____/____/________', 'Registro Vet:', '_______________'],
    ]

    firma_table = Table(firma_data, colWidths=[80, 120, 80, 120])
    firma_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(firma_table)

    # Pie de página
    elements.append(Spacer(1, 20))
    footer_text = f"PLANTILLA OFICIAL - ID: {mascota.id:08d} - Generada: {timezone.now().strftime('%d/%m/%Y %H:%M')} - VET LOVE"
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=1
    )
    elements.append(Paragraph(footer_text, footer_style))

    # Generar PDF
    doc.build(elements)

    # Preparar respuesta
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Plantilla_Carnet_Vacunacion_{mascota.nombre}.pdf"'

    return response


def descargar_carnet_identificacion_pdf(request, mascota_id):
    """
    Genera y descarga el carnet de identificación de mascota como PDF usando ReportLab
    con diseño oficial colombiano
    """
    mascota = get_object_or_404(Mascota, id=mascota_id)

    # Verificar permisos
    es_admin = request.user.is_staff or request.user.is_superuser
    if not es_admin:
        if not hasattr(request.user, 'cliente') or mascota.cliente != request.user.cliente:
            return HttpResponseForbidden("No tienes permiso para descargar este carnet")

    # Crear buffer para el PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    width, height = A4
    elements = []

    # Estilos
    styles = getSampleStyleSheet()

    # Título principal
    title_style = ParagraphStyle(
        'RepublicTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=10,
        alignment=1,
        textColor=colors.black
    )

    ministry_style = ParagraphStyle(
        'MinistryTitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=5,
        alignment=1,
        textColor=colors.black
    )

    cert_style = ParagraphStyle(
        'CertTitle',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=20,
        alignment=1,
        textColor=colors.black
    )

    # Títulos oficiales
    elements.append(Paragraph("REPÚBLICA DE COLOMBIA", title_style))
    elements.append(Paragraph("REGISTRO DE MASCOTAS", ministry_style))
    elements.append(Paragraph("CERTIFICADO DE IDENTIFICACIÓN", cert_style))

    # Número de identificación
    id_style = ParagraphStyle(
        'IDNumber',
        parent=styles['Normal'],
        fontSize=14,
        alignment=2,  # Derecha
        spaceAfter=20
    )
    elements.append(Paragraph(f"No. {mascota.id:08d}", id_style))

    # Información de la mascota
    elements.append(Spacer(1, 10))

    # Crear tabla de datos del animal
    animal_data = [
        ['DATOS DEL ANIMAL', ''],
        ['NOMBRE:', mascota.nombre.upper()],
        ['ESPECIE:', mascota.get_tipo_display().upper()],
        ['RAZA:', (mascota.raza or 'MESTIZO').upper()],
        ['SEXO:', mascota.get_sexo_display().upper()],
        ['COLOR:', (mascota.color or 'NO ESPECIFICADO').upper()],
        ['F. NACIMIENTO:', mascota.fecha_nacimiento.strftime('%d/%m/%Y') if mascota.fecha_nacimiento else 'NO REGISTRA'],
    ]

    animal_table = Table(animal_data, colWidths=[120, 200])
    animal_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.Color(0.11, 0.25, 0.36)),  # Azul oficial
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (1, 0), 12),
        ('SPAN', (0, 0), (1, 0)),  # Unir celdas del título

        ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(animal_table)

    # Información del propietario
    elements.append(Spacer(1, 15))

    propietario_data = [
        ['DATOS DEL PROPIETARIO', ''],
        ['NOMBRE:', (mascota.cliente.usuario.get_full_name() or mascota.cliente.usuario.username).upper()],
        ['DOCUMENTO:', 'NO REGISTRA'],
        ['DIRECCIÓN:', (mascota.cliente.direccion or 'NO REGISTRA').upper()],
        ['TELÉFONO:', (mascota.cliente.telefono or 'NO REGISTRA')],
    ]

    propietario_table = Table(propietario_data, colWidths=[120, 200])
    propietario_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.Color(0.11, 0.25, 0.36)),  # Azul oficial
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (1, 0), 12),
        ('SPAN', (0, 0), (1, 0)),  # Unir celdas del título

        ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(propietario_table)

    # Información médica básica
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("INFORMACIÓN MÉDICA", section_style))

    medica_data = [
        ['Estado Vacunación:', mascota.get_estado_vacunacion_display or 'NO REGISTRA'],
        ['Última Vacuna:', mascota.fecha_ultima_vacuna.strftime('%d/%m/%Y') if mascota.fecha_ultima_vacuna else 'NO REGISTRA'],
        ['Desparasitación:', mascota.get_desparasitacion_display or 'NO REGISTRA'],
        ['Microchip:', mascota.microchip or 'NO REGISTRA'],
        ['Registro:', 'PLATAFORMA LOCAL'],
    ]

    medica_table = Table(medica_data, colWidths=[120, 200])
    medica_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(medica_table)

    # Información de expedición
    elements.append(Spacer(1, 30))

    expedicion_data = [
        ['Fecha de Expedición:', timezone.now().strftime('%d/%m/%Y')],
        ['Fecha de Vencimiento:', (timezone.now() + timedelta(days=730)).strftime('%d/%m/%Y')],
        ['Expedido por:', 'VETERINARIA VET LOVE'],
        ['Registro:', 'LOCAL DE MASCOTAS'],
        ['Contacto Emergencia:', (mascota.telefono_emergencia or mascota.cliente.telefono or 'NO REGISTRA')],
    ]

    expedicion_table = Table(expedicion_data, colWidths=[120, 200])
    expedicion_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(expedicion_table)

    # Pie de página
    elements.append(Spacer(1, 20))
    footer_text = f"Documento oficial colombiano - ID: {mascota.id:08d} - Emitido: {timezone.now().strftime('%d/%m/%Y %H:%M')}"
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=1
    )
    elements.append(Paragraph(footer_text, footer_style))

    # Generar PDF
    doc.build(elements)

    # Preparar respuesta
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Carnet_Identificacion_{mascota.nombre}.pdf"'

    return response



