from django.db import models
from clientes.models import Cliente
from veterinario.models import Veterinario
from datetime import date
from decimal import Decimal

class Mascota(models.Model):
    TIPO_CHOICES = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('ave', 'Ave'),
        ('roedor', 'Roedor'),
        ('reptil', 'Reptil'),
        ('otro', 'Otro'),
    ]
    
    SEXO_CHOICES = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra'),
    ]
    
    ESTERILIZADO_CHOICES = [
        ('si', 'Sí'),
        ('no', 'No'),
        ('desconocido', 'Desconocido'),
    ]
    
    ESTADO_VACUNACION_CHOICES = [
        ('completo', 'Vacunación Completa y Actualizada'),
        ('parcial', 'Algunas Vacunas Pendientes'),
        ('desconocido', 'Desconocido/No hay Registros'),
        ('ninguna', 'Sin Vacunación'),
    ]
    
    DESPARASITACION_CHOICES = [
        ('actualizado', 'Desparasitación Actualizada'),
        ('pendiente', 'Desparasitación Pendiente'),
        ('desconocido', 'Estado Desconocido'),
    ]
    
    COMPORTAMIENTO_CONSULTA_CHOICES = [
        ('tranquilo', 'Tranquilo y Cooperativo'),
        ('nervioso', 'Nervioso pero Manejable'),
        ('asustadizo', 'Muy Asustadizo/Difícil de Examinar'),
        ('agresivo', 'Puede ser Agresivo/Morder'),
        ('solo_dueno', 'Solo Permite Manejo del Dueño'),
        ('requiere_sedacion', 'Requiere Sedación para Procedimientos'),
    ]
    
    # Información básica
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name="Especie")
    raza = models.CharField(max_length=100, verbose_name="Raza")
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES, verbose_name="Sexo")
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de nacimiento")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='mascotas', verbose_name="Cliente")
    
    # Identificación
    microchip = models.CharField(max_length=15, blank=True, verbose_name="Microchip")
    foto = models.ImageField(upload_to='mascotas/', null=True, blank=True, verbose_name="Foto")
    
    # Información médica inicial
    alergias_conocidas = models.TextField(blank=True, verbose_name="Alergias conocidas")
    alergias_tipo = models.CharField(max_length=200, blank=True, verbose_name="Tipos de alergias")
    enfermedades_cronicas = models.TextField(blank=True, verbose_name="Enfermedades crónicas")
    enfermedades_tipo = models.CharField(max_length=200, blank=True, verbose_name="Tipos de enfermedades")
    esterilizado = models.CharField(max_length=15, choices=ESTERILIZADO_CHOICES, default='desconocido', verbose_name="Esterilizado")
    fecha_esterilizacion = models.DateField(null=True, blank=True, verbose_name="Fecha de esterilización")
    
    # Información médica crítica (NUEVOS CAMPOS)
    peso_actual = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name="Peso actual (kg)"
    )
    medicacion_actual = models.TextField(blank=True, verbose_name="Medicación actual")
    comportamiento_consulta = models.CharField(
        max_length=20, choices=COMPORTAMIENTO_CONSULTA_CHOICES, 
        default='tranquilo', verbose_name="Comportamiento en consulta"
    )
    veterinario_habitual = models.CharField(max_length=200, blank=True, verbose_name="Veterinario habitual")
    telefono_emergencia = models.CharField(max_length=20, blank=True, verbose_name="Teléfono emergencia")
    
    # Vacunación y prevención
    estado_vacunacion = models.CharField(
        max_length=20, choices=ESTADO_VACUNACION_CHOICES, 
        default='desconocido', verbose_name="Estado de vacunación"
    )
    fecha_ultima_vacuna = models.DateField(null=True, blank=True, verbose_name="Fecha última vacuna")
    desparasitacion = models.CharField(
        max_length=20, choices=DESPARASITACION_CHOICES, 
        default='desconocido', verbose_name="Estado de desparasitación"
    )
    fecha_ultima_desparasitacion = models.DateField(null=True, blank=True, verbose_name="Fecha última desparasitación")
    
    # Historial quirúrgico
    cirugias_previas = models.CharField(max_length=200, blank=True, verbose_name="Cirugías previas")
    fecha_ultima_cirugia = models.DateField(null=True, blank=True, verbose_name="Fecha última cirugía")
    
    # Alimentación y comportamiento
    tipo_alimentacion = models.CharField(max_length=20, blank=True, verbose_name="Tipo de alimentación")
    frecuencia_alimentacion = models.CharField(max_length=100, blank=True, verbose_name="Frecuencia de alimentación")
    comportamiento = models.CharField(max_length=200, blank=True, verbose_name="Comportamiento")
    permite_manejo = models.CharField(max_length=50, blank=True, verbose_name="Permitividad al manejo")
    cartilla_vacunacion = models.CharField(max_length=20, blank=True, verbose_name="Estado de vacunación")
    observaciones_comportamiento = models.TextField(blank=True, verbose_name="Observaciones de comportamiento")
    
    # Características físicas
    caracteristicas = models.TextField(blank=True, verbose_name="Señas particulares")
    color = models.CharField(max_length=50, blank=True, verbose_name="Color principal")
    
    # Asignación de veterinario
    veterinario_asignado = models.ForeignKey(
        Veterinario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mascotas_asignadas',
        verbose_name="Veterinario Asignado"
    )

    # Metadata
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    
    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"
    
    def edad(self):
        if self.fecha_nacimiento:
            today = date.today()
            return today.year - self.fecha_nacimiento.year - (
                (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
        return None
    
    def necesita_vacuna(self):
        """Verifica si la mascota necesita vacunación"""
        if self.estado_vacunacion in ['parcial', 'ninguna', 'desconocido']:
            return True
        return False
    
    def necesita_desparasitacion(self):
        """Verifica si la mascota necesita desparasitación"""
        return self.desparasitacion in ['pendiente', 'desconocido']
    
    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"
        ordering = ['nombre']

class HistorialMedico(models.Model):
    CONDICION_CORPORAL_CHOICES = [
        (1, '1 - Muy delgado'),
        (2, '2 - Delgado'),
        (3, '3 - Ideal'),
        (4, '4 - Sobrepeso'),
        (5, '5 - Obeso'),
    ]
    
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='historial_medico', verbose_name="Mascota")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    veterinario = models.CharField(max_length=100, verbose_name="Veterinario")
    
    # Signos vitales
    peso = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        verbose_name="Peso (kg)",
        default=0.00
    )
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="Temperatura (°C)")
    frecuencia_cardiaca = models.IntegerField(null=True, blank=True, verbose_name="Frecuencia cardíaca (lpm)")
    frecuencia_respiratoria = models.IntegerField(null=True, blank=True, verbose_name="Frecuencia respiratoria (rpm)")
    condicion_corporal = models.IntegerField(choices=CONDICION_CORPORAL_CHOICES, null=True, blank=True, verbose_name="Condición corporal")
    
    # Diagnóstico y tratamiento
    motivo_consulta = models.TextField(
        verbose_name="Motivo de la consulta",
        default="Consulta general"
    )
    diagnostico = models.TextField(verbose_name="Diagnóstico")
    tratamiento = models.TextField(verbose_name="Tratamiento prescrito")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    
    # Información adicional
    vacunas_aplicadas = models.TextField(blank=True, verbose_name="Vacunas aplicadas")
    proxima_cita = models.DateField(null=True, blank=True, verbose_name="Próxima cita")
    
    class Meta:
        verbose_name = "Historial Médico"
        verbose_name_plural = "Historiales Médicos"
        ordering = ['-fecha']

class Vacuna(models.Model):
    VIA_APLICACION_CHOICES = [
        ('subcutanea', 'Subcutánea'),
        ('intramuscular', 'Intramuscular'),
        ('intranasal', 'Intranasal'),
    ]
    
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='vacunas', verbose_name="Mascota")
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la vacuna")
    fecha_aplicacion = models.DateField(verbose_name="Fecha de aplicación")
    fecha_proxima = models.DateField(verbose_name="Próxima aplicación")
    aplicada = models.BooleanField(default=True, verbose_name="Aplicada")
    
    # Información adicional
    lote = models.CharField(
        max_length=20, 
        verbose_name="Número de lote",
        default="Lote no especificado"
    )
    laboratorio = models.CharField(
        max_length=100, 
        verbose_name="Laboratorio fabricante",
        default="Laboratorio no especificado"
    )
    via_aplicacion = models.CharField(max_length=15, choices=VIA_APLICACION_CHOICES, default='subcutanea', verbose_name="Vía de aplicación")
    sitio_aplicacion = models.CharField(max_length=100, blank=True, verbose_name="Sitio de aplicación")
    reacciones_adversas = models.TextField(blank=True, verbose_name="Reacciones adversas")
    
    def __str__(self):
        return f"{self.nombre} - {self.mascota.nombre}"
    
    class Meta:
        verbose_name = "Vacuna"
        verbose_name_plural = "Vacunas"
        ordering = ['-fecha_aplicacion']