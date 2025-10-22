from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta, date
from citas.models import Cita
from mascotas.models import Vacuna, Mascota
from .models import Recordatorio, Notificacion

@receiver(post_save, sender=Cita)
def crear_recordatorio_cita(sender, instance, created, **kwargs):
    """Crear recordatorio automático cuando se crea una cita programada"""
    if created and instance.estado == 'programada':
        # Crear recordatorio 1 día antes
        Recordatorio.objects.create(
            cliente=instance.mascota.cliente,
            tipo='cita',
            titulo=f'Recordatorio: Cita de {instance.mascota.nombre}',
            mensaje=f'Tienes una cita programada para {instance.mascota.nombre} el {instance.fecha.strftime("%d/%m/%Y a las %H:%M")}. Tipo: {instance.get_tipo_display()}.',
            fecha_recordatorio=instance.fecha,
            dias_anticipacion=1,
            objeto_relacionado_id=instance.id,
            objeto_relacionado_tipo='cita'
        )

        # Determinar prioridad según el tipo de cita
        prioridad = 'normal'
        if instance.prioridad == 'urgente':
            prioridad = 'alta'
        elif instance.prioridad == 'emergencia':
            prioridad = 'urgente'

        # Crear notificación inmediata
        Notificacion.objects.create(
            cliente=instance.mascota.cliente,
            tipo='cita',
            titulo=f'Cita programada para {instance.mascota.nombre}',
            mensaje=f'Se ha programado una cita para {instance.mascota.nombre} el {instance.fecha.strftime("%d/%m/%Y a las %H:%M")}. Tipo: {instance.get_tipo_display()}.',
            url_relacionada=f'/citas/mis-citas/',
            prioridad=prioridad
        )

@receiver(post_save, sender=Vacuna)
def crear_recordatorio_vacuna(sender, instance, created, **kwargs):
    """Crear recordatorio automático para la próxima vacuna"""
    if created and instance.fecha_proxima:
        # Crear recordatorio 7 días antes (o menos si la fecha próxima es muy cercana)
        dias_anticipacion = min(7, (instance.fecha_proxima - timezone.now().date()).days - 1)
        if dias_anticipacion > 0:
            Recordatorio.objects.create(
                cliente=instance.mascota.cliente,
                tipo='vacuna',
                titulo=f'Recordatorio: Vacuna de {instance.mascota.nombre}',
                mensaje=f'La próxima vacuna de {instance.mascota.nombre} ({instance.nombre}) está programada para el {instance.fecha_proxima.strftime("%d/%m/%Y")}.',
                fecha_recordatorio=timezone.datetime.combine(instance.fecha_proxima, timezone.datetime.min.time()),
                dias_anticipacion=dias_anticipacion,
                objeto_relacionado_id=instance.id,
                objeto_relacionado_tipo='vacuna'
            )

            # Las vacunas tienen prioridad alta por defecto
            Notificacion.objects.create(
                cliente=instance.mascota.cliente,
                tipo='vacuna',
                titulo=f'Vacuna registrada para {instance.mascota.nombre}',
                mensaje=f'Se ha registrado la vacuna "{instance.nombre}" para {instance.mascota.nombre}. Próxima dosis: {instance.fecha_proxima.strftime("%d/%m/%Y")}.',
                url_relacionada=f'/mascotas/{instance.mascota.id}/',
                prioridad='alta'
            )

@receiver(post_save, sender=Cita)
def notificar_cambio_estado_cita(sender, instance, created, **kwargs):
    """Notificar cambios de estado de citas"""
    if not created:
        # Solo notificar si el estado cambió
        if hasattr(instance, '_original_estado'):
            if instance._original_estado != instance.estado:
                prioridad = 'normal'
                if instance.estado == 'cancelada':
                    prioridad = 'alta'
                    titulo = f'Cita cancelada para {instance.mascota.nombre}'
                    mensaje = f'La cita programada para {instance.mascota.nombre} el {instance.fecha.strftime("%d/%m/%Y a las %H:%M")} ha sido cancelada.'
                elif instance.estado == 'reprogramada':
                    prioridad = 'alta'
                    titulo = f'Cita reprogramada para {instance.mascota.nombre}'
                    mensaje = f'La cita de {instance.mascota.nombre} ha sido reprogramada. Nueva fecha: {instance.fecha.strftime("%d/%m/%Y a las %H:%M")}.'
                elif instance.estado == 'confirmada':
                    titulo = f'Cita confirmada para {instance.mascota.nombre}'
                    mensaje = f'Su cita para {instance.mascota.nombre} el {instance.fecha.strftime("%d/%m/%Y a las %H:%M")} ha sido confirmada.'
                elif instance.estado == 'completada':
                    titulo = f'Cita completada para {instance.mascota.nombre}'
                    mensaje = f'La cita de {instance.mascota.nombre} del {instance.fecha.strftime("%d/%m/%Y")} ha sido completada exitosamente.'
                else:
                    return  # No notificar otros cambios de estado

                Notificacion.objects.create(
                    cliente=instance.mascota.cliente,
                    tipo='cita',
                    titulo=titulo,
                    mensaje=mensaje,
                    url_relacionada='/citas/mis-citas/',
                    prioridad=prioridad
                )

@receiver(pre_save, sender=Cita)
def guardar_estado_original_cita(sender, instance, **kwargs):
    """Guardar el estado original antes de cambios para detectar modificaciones"""
    if instance.pk:
        try:
            instance._original_estado = Cita.objects.get(pk=instance.pk).estado
        except Cita.DoesNotExist:
            instance._original_estado = None
    else:
        instance._original_estado = None

@receiver(post_save, sender=Mascota)
def crear_recordatorio_cumpleanos(sender, instance, created, **kwargs):
    """Crear recordatorio automático para cumpleaños de mascotas"""
    if created and instance.fecha_nacimiento:
        # Crear recordatorio anual para el cumpleaños
        hoy = timezone.now().date()
        fecha_cumple = instance.fecha_nacimiento.replace(year=hoy.year)

        # Si el cumpleaños ya pasó este año, programar para el próximo año
        if fecha_cumple < hoy:
            fecha_cumple = fecha_cumple.replace(year=hoy.year + 1)

        Recordatorio.objects.create(
            cliente=instance.cliente,
            tipo='cumpleanos',
            titulo=f'¡Feliz cumpleaños {instance.nombre}!',
            mensaje=f'Hoy {instance.nombre} cumple {instance.edad() + 1 if instance.edad() else "años"}. ¡No olvides felicitarlo!',
            fecha_recordatorio=timezone.datetime.combine(fecha_cumple, timezone.datetime.min.time()),
            dias_anticipacion=0,  # El mismo día
            objeto_relacionado_id=instance.id,
            objeto_relacionado_tipo='mascota'
        )

        # Notificación inmediata de registro
        Notificacion.objects.create(
            cliente=instance.cliente,
            tipo='sistema',
            titulo=f'Mascota registrada: {instance.nombre}',
            mensaje=f'Se ha registrado exitosamente a {instance.nombre} en el sistema veterinario.',
            url_relacionada=f'/mascotas/{instance.id}/',
            prioridad='normal'
        )