from django.db import models
from clientes.models import Cliente

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
    
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name="Tipo")
    raza = models.CharField(max_length=100, blank=True, verbose_name="Raza")
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES, verbose_name="Sexo")
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de nacimiento")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='mascotas', verbose_name="Cliente")
    foto = models.ImageField(upload_to='mascotas/', null=True, blank=True, verbose_name="Foto")
    caracteristicas = models.TextField(blank=True, verbose_name="Características")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    
    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"
    
    def edad(self):
        from datetime import date
        if self.fecha_nacimiento:
            today = date.today()
            return today.year - self.fecha_nacimiento.year - (
                (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
        return None
    
    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"
        ordering = ['nombre']

class HistorialMedico(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='historial_medico', verbose_name="Mascota")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    veterinario = models.CharField(max_length=100, verbose_name="Veterinario")
    diagnostico = models.TextField(verbose_name="Diagnóstico")
    tratamiento = models.TextField(blank=True, verbose_name="Tratamiento")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Peso (kg)")
    
    class Meta:
        verbose_name = "Historial Médico"
        verbose_name_plural = "Historiales Médicos"
        ordering = ['-fecha']

class Vacuna(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='vacunas', verbose_name="Mascota")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    fecha_aplicacion = models.DateField(verbose_name="Fecha de aplicación")
    fecha_proxima = models.DateField(verbose_name="Próxima aplicación")
    aplicada = models.BooleanField(default=True, verbose_name="Aplicada")
    
    def __str__(self):
        return f"{self.nombre} - {self.mascota.nombre}"
    
    class Meta:
        verbose_name = "Vacuna"
        verbose_name_plural = "Vacunas"
        ordering = ['-fecha_aplicacion']