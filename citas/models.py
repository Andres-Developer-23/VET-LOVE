from django.db import models
from mascotas.models import Mascota
from django.utils import timezone

class Cita(models.Model):
    ESTADO_CHOICES = [
        ('programada', 'Programada'),
        ('confirmada', 'Confirmada'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
        ('reprogramada', 'Reprogramada'),
    ]
    
    TIPO_CHOICES = [
        ('consulta_general', 'Consulta General'),
        ('vacunacion', 'Vacunación'),
        ('desparasitacion', 'Desparasitación'),
        ('urgencia', 'Urgencia'),
        ('cirugia', 'Cirugía'),
        ('estetica', 'Estética/Baño'),
        ('odontologia', 'Odontología'),
        ('analisis', 'Análisis Clínicos'),
        ('radiologia', 'Radiología'),
        ('ecografia', 'Ecografía'),
        ('control', 'Control de Peso'),
        ('comportamiento', 'Consulta de Comportamiento'),
        ('nutricion', 'Consulta Nutricional'),
    ]
    
    PRIORIDAD_CHOICES = [
        ('normal', 'Normal'),
        ('urgente', 'Urgente'),
        ('emergencia', 'Emergencia'),
    ]

   
   
   ##BD
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='citas')
    fecha = models.DateTimeField(verbose_name="Fecha y Hora")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo de Cita")
    prioridad = models.CharField(max_length=15, choices=PRIORIDAD_CHOICES, default='normal', verbose_name="Prioridad")
    motivo = models.TextField(verbose_name="Motivo de la Consulta")
    sintomas = models.TextField(blank=True, verbose_name="Síntomas Presentados")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='programada', verbose_name="Estado")
    veterinario = models.CharField(max_length=100, blank=True, verbose_name="Veterinario Asignado")
    duracion_estimada = models.PositiveIntegerField(default=30, verbose_name="Duración Estimada (minutos)")
    sala = models.CharField(max_length=50, blank=True, verbose_name="Sala/Consultorio")
    notas = models.TextField(blank=True, verbose_name="Notas Adicionales")
    antecedentes = models.TextField(blank=True, verbose_name="Antecedentes Relevantes")
    medicamentos_actuales = models.TextField(blank=True, verbose_name="Medicamentos Actuales")
    alergias = models.TextField(blank=True, verbose_name="Alergias Conocidas")
    recordatorio_enviado = models.BooleanField(default=False, verbose_name="Recordatorio Enviado")
    confirmada_por_cliente = models.BooleanField(default=False, verbose_name="Confirmada por Cliente")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        ordering = ['fecha']
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        indexes = [
            models.Index(fields=['fecha', 'estado']),
            models.Index(fields=['mascota', 'fecha']),
        ]
    
    def __str__(self):
        return f"{self.mascota.nombre} - {self.fecha.strftime('%d/%m/%Y %H:%M')} - {self.get_tipo_display()}"
    
    def puede_ser_cancelada(self):
        return self.estado in ['programada', 'confirmada']