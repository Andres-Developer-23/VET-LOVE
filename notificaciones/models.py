from django.db import models
from clientes.models import Cliente
from django.utils import timezone

class Notificacion(models.Model):
    TIPO_CHOICES = [
        ('general', 'General'),
        ('cita', 'Cita'),
        ('vacuna', 'Vacuna'),
        ('desparasitacion', 'Desparasitación'),
        ('medicamento', 'Medicamento'),
        ('emergencia', 'Emergencia'),
        ('sistema', 'Sistema'),
    ]

    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('normal', 'Normal'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='notificaciones', null=True, blank=True)
    veterinario = models.ForeignKey('veterinario.Veterinario', on_delete=models.CASCADE, related_name='notificaciones', null=True, blank=True)
    para_admin = models.BooleanField(default=False, verbose_name="Para Administrador")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='general')
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    enviada_por_email = models.BooleanField(default=False)
    url_relacionada = models.URLField(blank=True, null=True)  # Para enlazar a la página relevante
    prioridad = models.CharField(
        max_length=10,
        choices=PRIORIDAD_CHOICES,
        default='normal',
        verbose_name="Prioridad"
    )
    fecha_lectura = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de lectura")

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'

    def __str__(self):
        if self.para_admin:
            return f"{self.titulo} - Administrador"
        elif self.cliente:
            return f"{self.titulo} - {self.cliente}"
        elif self.veterinario:
            return f"{self.titulo} - {self.veterinario}"
        else:
            return f"{self.titulo} - Todos los usuarios"

    def marcar_como_leida(self):
        from django.utils import timezone
        self.leida = True
        self.fecha_lectura = timezone.now()
        self.save()


class Recordatorio(models.Model):
    TIPO_CHOICES = [
        ('cita', 'Cita Programada'),
        ('vacuna', 'Vacuna Próxima'),
        ('desparasitacion', 'Desparasitación'),
        ('medicamento', 'Medicamento'),
        ('control', 'Control Médico'),
        ('cumpleanos', 'Cumpleaños Mascota'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='recordatorios')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha_recordatorio = models.DateTimeField()  # Fecha y hora del evento
    dias_anticipacion = models.PositiveIntegerField(default=1)  # Días antes de enviar
    enviado = models.BooleanField(default=False)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    objeto_relacionado_id = models.PositiveIntegerField(null=True, blank=True)  # ID del objeto relacionado (cita, vacuna, etc.)
    objeto_relacionado_tipo = models.CharField(max_length=50, blank=True)  # Tipo del objeto (cita, vacuna, etc.)

    class Meta:
        ordering = ['fecha_recordatorio']
        verbose_name = 'Recordatorio'
        verbose_name_plural = 'Recordatorios'

    def __str__(self):
        return f"{self.titulo} - {self.fecha_recordatorio.strftime('%d/%m/%Y %H:%M')}"

    def debe_enviarse(self):
        """Verifica si el recordatorio debe enviarse hoy"""
        if not self.activo or self.enviado:
            return False

        ahora = timezone.now()
        fecha_envio_calculada = self.fecha_recordatorio - timezone.timedelta(days=self.dias_anticipacion)

        # Enviar si es el día calculado y no ha pasado la hora del evento
        return (fecha_envio_calculada.date() <= ahora.date() <= self.fecha_recordatorio.date() and
                not self.enviado)

    def marcar_enviado(self):
        self.enviado = True
        self.fecha_envio = timezone.now()
        self.save()
