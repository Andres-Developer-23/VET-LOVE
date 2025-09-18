from django.db import models
from mascotas.models import Mascota

class Cita(models.Model):
    ESTADO_CHOICES = [
        ('programada', 'Programada'),
        ('confirmada', 'Confirmada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    TIPO_CHOICES = [
        ('consulta', 'Consulta General'),
        ('vacunacion', 'Vacunación'),
        ('urgencia', 'Urgencia'),
        ('cirugia', 'Cirugía'),
        ('estetica', 'Estética'),
    ]
    
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='citas')
    fecha = models.DateTimeField(verbose_name="Fecha y Hora")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo de Cita")
    motivo = models.TextField(verbose_name="Motivo de la Consulta")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='programada', verbose_name="Estado")
    veterinario = models.CharField(max_length=100, blank=True, verbose_name="Veterinario")
    notas = models.TextField(blank=True, verbose_name="Notas")
    recordatorio_enviado = models.BooleanField(default=False, verbose_name="Recordatorio Enviado")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    
    class Meta:
        ordering = ['fecha']
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
    
    def __str__(self):
        return f"{self.mascota.nombre} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"
    
    def puede_ser_cancelada(self):
        return self.estado in ['programada', 'confirmada']  