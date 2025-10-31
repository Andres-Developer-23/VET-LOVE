from django.db import models
from django.contrib.auth.models import User

class Veterinario(models.Model):
    """Modelo para veterinarios del sistema"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_veterinario')
    nombre_completo = models.CharField(max_length=200, verbose_name="Nombre Completo")
    especialidad = models.CharField(max_length=100, blank=True, verbose_name="Especialidad")
    numero_colegiado = models.CharField(max_length=50, blank=True, verbose_name="Número de Colegiado")
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Veterinario"
        verbose_name_plural = "Veterinarios"
        ordering = ['nombre_completo']

    def __str__(self):
        return f"Dr. {self.nombre_completo}"

    def save(self, *args, **kwargs):
        # Agregar automáticamente al grupo Veterinarios
        super().save(*args, **kwargs)
        from django.contrib.auth.models import Group
        grupo_veterinarios = Group.objects.get(name='Veterinarios')
        self.usuario.groups.add(grupo_veterinarios)