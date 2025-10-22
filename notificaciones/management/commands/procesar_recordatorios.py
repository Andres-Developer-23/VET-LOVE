from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from notificaciones.models import Recordatorio, Notificacion
from datetime import timedelta

class Command(BaseCommand):
    help = 'Procesa recordatorios pendientes y envía notificaciones'

    def handle(self, *args, **options):
        self.stdout.write('Procesando recordatorios...')

        # Obtener recordatorios que deben enviarse hoy
        recordatorios_pendientes = Recordatorio.objects.filter(
            activo=True,
            enviado=False
        )

        enviados = 0
        for recordatorio in recordatorios_pendientes:
            if recordatorio.debe_enviarse():
                # Crear notificación
                Notificacion.objects.create(
                    cliente=recordatorio.cliente,
                    tipo=recordatorio.tipo,
                    titulo=recordatorio.titulo,
                    mensaje=recordatorio.mensaje,
                    url_relacionada=self._get_url_relacionada(recordatorio)
                )

                # Enviar email si el cliente prefiere email
                if hasattr(recordatorio.cliente, 'preferencias_comunicacion') and recordatorio.cliente.preferencias_comunicacion == 'email':
                    self._enviar_email_recordatorio(recordatorio)

                # Marcar como enviado
                recordatorio.marcar_enviado()
                enviados += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Recordatorio enviado: {recordatorio.titulo} para {recordatorio.cliente}'
                    )
                )

        # Procesar recordatorios recurrentes (cumpleaños)
        self._procesar_recordatorios_recurrentes()

        if enviados == 0:
            self.stdout.write('No hay recordatorios pendientes para enviar.')
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Se enviaron {enviados} recordatorios.')
            )

    def _get_url_relacionada(self, recordatorio):
        """Obtener URL relacionada según el tipo de recordatorio"""
        if recordatorio.objeto_relacionado_tipo == 'cita':
            return '/citas/mis-citas/'
        elif recordatorio.objeto_relacionado_tipo == 'vacuna':
            return f'/mascotas/detalle/{recordatorio.objeto_relacionado_id}/'
        return None

    def _enviar_email_recordatorio(self, recordatorio):
        """Enviar email de recordatorio"""
        try:
            subject = f'Recordatorio: {recordatorio.titulo}'
            message = f"""
Hola {recordatorio.cliente.usuario.first_name},

{recordatorio.mensaje}

Atentamente,
Equipo de Veterinaria Vet Love
            """.strip()

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recordatorio.cliente.usuario.email],
                fail_silently=True
            )
            self.stdout.write(
                f'Email enviado a {recordatorio.cliente.usuario.email}'
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error enviando email: {e}')
            )

    def _procesar_recordatorios_recurrentes(self):
        """Procesar recordatorios recurrentes como cumpleaños"""
        from mascotas.models import Mascota

        hoy = timezone.now().date()
        mascotas_cumpleaneras = Mascota.objects.filter(
            fecha_nacimiento__month=hoy.month,
            fecha_nacimiento__day=hoy.day
        )

        for mascota in mascotas_cumpleaneras:
            # Verificar si ya se creó una notificación hoy para este cumpleaños
            notificaciones_hoy = Notificacion.objects.filter(
                cliente=mascota.cliente,
                tipo='cumpleanos',
                fecha_creacion__date=hoy,
                titulo__contains=mascota.nombre
            )

            if not notificaciones_hoy.exists():
                Notificacion.objects.create(
                    cliente=mascota.cliente,
                    tipo='cumpleanos',
                    titulo=f'¡Feliz cumpleaños {mascota.nombre}!',
                    mensaje=f'Hoy {mascota.nombre} cumple {mascota.edad()} años. ¡No olvides felicitarlo!',
                    url_relacionada=f'/mascotas/{mascota.id}/',
                    prioridad='normal'
                )

                # Enviar email si corresponde
                if hasattr(mascota.cliente, 'preferencias_comunicacion') and mascota.cliente.preferencias_comunicacion == 'email':
                    self._enviar_email_cumpleanos(mascota)

                self.stdout.write(
                    self.style.SUCCESS(f'Notificación de cumpleaños enviada para {mascota.nombre}')
                )

    def _enviar_email_cumpleanos(self, mascota):
        """Enviar email de felicitación por cumpleaños"""
        try:
            subject = f'¡Feliz cumpleaños {mascota.nombre}!'
            message = f"""
Hola {mascota.cliente.usuario.first_name},

¡Hoy es el cumpleaños de {mascota.nombre}!
Tu mascota cumple {mascota.edad()} años hoy.

¡Felicítalo y dale mucho cariño!

Atentamente,
Equipo de Veterinaria Vet Love
            """.strip()

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[mascota.cliente.usuario.email],
                fail_silently=True
            )
            self.stdout.write(
                f'Email de cumpleaños enviado a {mascota.cliente.usuario.email}'
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error enviando email de cumpleaños: {e}')
            )