from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta, datetime, date
from django.db.models import Count, Q, Sum, F, Value
from django.db.models.functions import Coalesce, Concat
from django.db.models import Value
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django import forms
import csv
import json
from django.core.serializers.json import DjangoJSONEncoder
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side, NamedStyle
from openpyxl.utils import get_column_letter

from clientes.models import Cliente
from mascotas.models import Mascota, HistorialMedico, Vacuna
from citas.models import Cita
from tienda.models import Producto, Categoria, Orden
from django.contrib.auth.models import User
from notificaciones.models import Notificacion, Recordatorio

def veterinario_required(login_url=None):
    return user_passes_test(lambda u: u.groups.filter(name='Veterinarios').exists() or u.is_staff, login_url=login_url)

@login_required
@veterinario_required(login_url='/admin/login/')
def dashboard_veterinario(request):
    """
    Panel principal para veterinarios - vista especializada para gestión veterinaria
    """
    hoy = timezone.now().date()
    veterinario = getattr(request.user, 'perfil_veterinario_app', None)

    # Verificar que el veterinario existe
    if veterinario is None:
        messages.error(request, 'No se encontró un perfil de veterinario para este usuario. Contacte al administrador.')
        return redirect('admin:index')

    # Filtrar solo mascotas asignadas al veterinario
    mascotas_asignadas = Mascota.objects.filter(veterinario_asignado=veterinario)

    # Estadísticas específicas para veterinarios (solo mascotas asignadas)
    total_mascotas = mascotas_asignadas.count()
    citas_hoy = Cita.objects.filter(
        fecha__date=hoy,
        estado__in=['programada', 'confirmada']
    ).filter(
        Q(mascota__veterinario_asignado=veterinario) | Q(veterinario_asignado=veterinario)
    ).select_related('mascota__cliente__usuario').order_by('fecha')

    citas_pendientes = Cita.objects.filter(
        estado__in=['programada', 'confirmada']
    ).filter(
        Q(mascota__veterinario_asignado=veterinario) | Q(veterinario_asignado=veterinario)
    ).count()

    # Mascotas activas asignadas (todas las asignadas se consideran activas)
    mascotas_activas = mascotas_asignadas.count()

    # Historial médico reciente (solo de mascotas asignadas)
    historial_reciente = HistorialMedico.objects.filter(
        mascota__veterinario_asignado=veterinario
    ).select_related('mascota__cliente__usuario').order_by('-fecha')[:10]

    # Vacunas próximas a vencer (solo de mascotas asignadas)
    from datetime import timedelta
    fecha_limite = hoy + timedelta(days=30)
    proximas_vacunas = Vacuna.objects.filter(
        mascota__veterinario_asignado=veterinario,
        fecha_proxima__lte=fecha_limite,
        fecha_proxima__gte=hoy
    ).select_related('mascota__cliente__usuario').order_by('fecha_proxima')[:10]

    # Citas urgentes (mascotas asignadas o citas asignadas)
    citas_urgentes = Cita.objects.filter(
            fecha__date=hoy,
            tipo='urgencia',
            estado__in=['programada', 'confirmada']
        ).filter(
            Q(mascota__veterinario_asignado=veterinario) | Q(veterinario_asignado=veterinario)
        ).count()

    # Próximas citas (de mascotas asignadas o citas asignadas directamente al veterinario)
    proximas_citas = Cita.objects.filter(
        fecha__date__gt=hoy,
        estado__in=['programada', 'confirmada']
    ).filter(
        Q(mascota__veterinario_asignado=veterinario) | Q(veterinario_asignado=veterinario)
    ).select_related('mascota__cliente__usuario').order_by('fecha')[:10]

    # Notificaciones para el veterinario
    notificaciones_pendientes = Notificacion.objects.filter(
        veterinario=veterinario,
        leida=False
    ).order_by('-fecha_creacion')[:5]

    # Estadísticas del mes (mascotas asignadas o citas asignadas)
    citas_mes = Cita.objects.filter(
        fecha__date__month=hoy.month,
        fecha__date__year=hoy.year
    ).filter(
        Q(mascota__veterinario_asignado=veterinario) | Q(veterinario_asignado=veterinario)
    ).count()

    citas_completadas_mes = Cita.objects.filter(
        fecha__date__month=hoy.month,
        fecha__date__year=hoy.year,
        estado='completada'
    ).filter(
        Q(mascota__veterinario_asignado=veterinario) | Q(veterinario_asignado=veterinario)
    ).count()


    # Filtros para gestión de citas (solo mascotas asignadas)
    cita_busqueda = request.GET.get('cita_busqueda', '')
    cita_estado = request.GET.get('cita_estado', '')
    cita_tipo = request.GET.get('cita_tipo', '')
    cita_periodo = request.GET.get('cita_periodo', 'hoy')

    # Base query para citas (mascotas asignadas o citas asignadas)
    citas_query = Cita.objects.filter(
        Q(mascota__veterinario_asignado=veterinario) | Q(veterinario_asignado=veterinario)
    ).select_related('mascota__cliente__usuario')

    # Aplicar filtros de período
    if cita_periodo == 'hoy':
        citas_query = citas_query.filter(fecha__date=hoy)
    elif cita_periodo == 'semana':
        semana_inicio = hoy - timedelta(days=hoy.weekday())
        semana_fin = semana_inicio + timedelta(days=6)
        citas_query = citas_query.filter(fecha__date__range=[semana_inicio, semana_fin])
    elif cita_periodo == 'mes':
        citas_query = citas_query.filter(fecha__date__month=hoy.month, fecha__date__year=hoy.year)

    # Filtro por estado
    if cita_estado:
        citas_query = citas_query.filter(estado=cita_estado)

    # Filtro por tipo
    if cita_tipo:
        citas_query = citas_query.filter(tipo=cita_tipo)

    # Filtro por búsqueda
    if cita_busqueda:
        citas_query = citas_query.filter(
            Q(mascota__nombre__icontains=cita_busqueda) |
            Q(mascota__cliente__usuario__first_name__icontains=cita_busqueda) |
            Q(mascota__cliente__usuario__last_name__icontains=cita_busqueda) |
            Q(mascota__cliente__usuario__username__icontains=cita_busqueda) |
            Q(tipo__icontains=cita_busqueda)
        )

    # Citas filtradas para gestión
    citas_gestion = citas_query.order_by('fecha')[:50]

    # Obtener lista de mascotas asignadas para mostrar
    mascotas_asignadas_lista = mascotas_asignadas.select_related('cliente__usuario').order_by('nombre')[:20]

    context = {
        # Estadísticas principales
        'total_mascotas': total_mascotas,
        'citas_hoy': citas_hoy,
        'citas_pendientes': citas_pendientes,
        'mascotas_activas': mascotas_activas,
        'historial_reciente': historial_reciente,
        'proximas_vacunas': proximas_vacunas,
        'citas_urgentes': citas_urgentes,
        'citas_mes': citas_mes,
        'citas_completadas_mes': citas_completadas_mes,

        # Lista de mascotas asignadas
        'mascotas_asignadas': mascotas_asignadas_lista,

        # Próximas citas
        'proximas_citas': proximas_citas,

        # Filtros de citas
        'citas_gestion': citas_gestion,
        'cita_busqueda': cita_busqueda,
        'cita_estado': cita_estado,
        'cita_tipo': cita_tipo,
        'cita_periodo': cita_periodo,

        # Información del veterinario
        'veterinario': getattr(request.user, 'perfil_veterinario_app', None),
        'hoy': hoy,
        'mes_actual': hoy.strftime('%B %Y'),

        # Notificaciones
        'notificaciones_pendientes': notificaciones_pendientes,
    }

    return render(request, 'veterinario/dashboard_veterinario.html', context)

@login_required
@veterinario_required(login_url='/admin/login/')
def gestion_mascotas_veterinario(request):
    """
    Vista para que veterinarios gestionen mascotas
    """
    # Filtros
    tipo_filtro = request.GET.get('tipo', '')
    cliente_filtro = request.GET.get('cliente', '')
    busqueda = request.GET.get('busqueda', '')
    estado_filtro = request.GET.get('estado', 'activas')  # activas/inactivas/todas

    # Base query
    mascotas_query = Mascota.objects.select_related('cliente__usuario')

    # Aplicar filtros
    if tipo_filtro:
        mascotas_query = mascotas_query.filter(tipo=tipo_filtro)

    if cliente_filtro:
        mascotas_query = mascotas_query.filter(
            Q(cliente__usuario__username__icontains=cliente_filtro) |
            Q(cliente__usuario__first_name__icontains=cliente_filtro) |
            Q(cliente__usuario__last_name__icontains=cliente_filtro)
        )

    if estado_filtro == 'activas':
        mascotas_query = mascotas_query.filter(activo=True)
    elif estado_filtro == 'inactivas':
        mascotas_query = mascotas_query.filter(activo=False)

    if busqueda:
        mascotas_query = mascotas_query.filter(
            Q(nombre__icontains=busqueda) |
            Q(raza__icontains=busqueda) |
            Q(color__icontains=busqueda)
        )

    # Ordenar y limitar
    mascotas = mascotas_query.order_by('-fecha_registro')[:100]

    context = {
        'mascotas': mascotas,
        'tipo_filtro': tipo_filtro,
        'cliente_filtro': cliente_filtro,
        'busqueda': busqueda,
        'estado_filtro': estado_filtro,
        'tipos_mascota': Mascota.TIPO_CHOICES,
    }

    return render(request, 'veterinario/gestion_mascotas_veterinario.html', context)

@login_required
@veterinario_required(login_url='/admin/login/')
def gestion_citas_veterinario(request):
    """
    Vista para que veterinarios gestionen citas
    """
    hoy = timezone.now().date()

    # Filtros
    cita_busqueda = request.GET.get('cita_busqueda', '')
    cita_estado = request.GET.get('cita_estado', '')
    cita_tipo = request.GET.get('cita_tipo', '')
    cita_periodo = request.GET.get('cita_periodo', 'hoy')

    # Base query para citas
    citas_query = Cita.objects.select_related('mascota__cliente__usuario')

    # Aplicar filtros de período
    if cita_periodo == 'hoy':
        citas_query = citas_query.filter(fecha__date=hoy)
    elif cita_periodo == 'semana':
        semana_inicio = hoy - timedelta(days=hoy.weekday())
        semana_fin = semana_inicio + timedelta(days=6)
        citas_query = citas_query.filter(fecha__date__range=[semana_inicio, semana_fin])
    elif cita_periodo == 'mes':
        citas_query = citas_query.filter(fecha__date__month=hoy.month, fecha__date__year=hoy.year)

    # Filtro por estado
    if cita_estado:
        citas_query = citas_query.filter(estado=cita_estado)

    # Filtro por tipo
    if cita_tipo:
        citas_query = citas_query.filter(tipo=cita_tipo)

    # Filtro por búsqueda
    if cita_busqueda:
        citas_query = citas_query.filter(
            Q(mascota__nombre__icontains=cita_busqueda) |
            Q(mascota__cliente__usuario__first_name__icontains=cita_busqueda) |
            Q(mascota__cliente__usuario__last_name__icontains=cita_busqueda) |
            Q(mascota__cliente__usuario__username__icontains=cita_busqueda) |
            Q(tipo__icontains=cita_busqueda)
        )

    # Citas para gestión
    citas = citas_query.order_by('fecha')[:100]

    context = {
        'citas': citas,
        'cita_busqueda': cita_busqueda,
        'cita_estado': cita_estado,
        'cita_tipo': cita_tipo,
        'cita_periodo': cita_periodo,
        'hoy': hoy,
    }

    return render(request, 'veterinario/gestion_citas_veterinario.html', context)

@login_required
@veterinario_required(login_url='/admin/login/')
def historial_medico_veterinario(request, mascota_id):
    """
    Vista para que veterinarios vean y gestionen el historial médico de una mascota
    """
    try:
        mascota = Mascota.objects.select_related('cliente__usuario').get(id=mascota_id)
    except Mascota.DoesNotExist:
        messages.error(request, 'Mascota no encontrada.')
        return redirect('veterinario:gestion_mascotas_veterinario')

    # Historial médico
    historial = HistorialMedico.objects.filter(mascota=mascota).order_by('-fecha')

    # Vacunas de la mascota
    vacunas = Vacuna.objects.filter(mascota=mascota).order_by('-fecha_aplicacion')

    # Citas de la mascota
    citas_mascota = Cita.objects.filter(mascota=mascota).order_by('-fecha')

    context = {
        'mascota': mascota,
        'historial': historial,
        'vacunas': vacunas,
        'citas_mascota': citas_mascota,
    }

    return render(request, 'veterinario/historial_medico_veterinario.html', context)
