from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from citas.models import Cita

class Command(BaseCommand):
    help = 'Envía recordatorios de citas por email'
    
    def handle(self, *args, **options):
        # Obtener citas programadas para las próximas 24 horas que no han recibido recordatorio
        ahora = timezone.now()
        mañana = ahora + timedelta(hours=24)
        
        citas = Cita.objects.filter(
            fecha__range=(ahora, mañana),
            estado__in=['programada', 'confirmada'],
            recordatorio_enviado=False
        )
        
        for cita in citas:
            # Enviar email de recordatorio
            subject = f'Recordatorio de cita para {cita.mascota.nombre}'
            
            context = {
                'cita': cita,
                'cliente': cita.mascota.cliente,
                'mascota': cita.mascota,
            }
            
            html_message = render_to_string('citas/emails/recordatorio_cita.html', context)
            plain_message = render_to_string('citas/emails/recordatorio_cita.txt', context)
            
            try:
                send_mail(
                    subject,
                    plain_message,
                    'veterinaria@mimascota.com',  # Remitente
                    [cita.mascota.cliente.usuario.email],  # Destinatario
                    html_message=html_message,
                    fail_silently=False,
                )
                
                # Marcar como recordatorio enviado
                cita.recordatorio_enviado = True
                cita.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f'Recordatorio enviado para cita de {cita.mascota.nombre}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error enviando recordatorio: {str(e)}')
                )