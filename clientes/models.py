from django.db import models
from django.contrib.auth.models import User
import os

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")
    direccion = models.TextField(verbose_name="Dirección")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    preferencias_comunicacion = models.CharField(
        max_length=20, 
        choices=[
            ('email', 'Email'),
            ('sms', 'SMS'),
            ('whatsapp', 'WhatsApp')
        ], 
        default='email',
        verbose_name="Preferencias de comunicación"
    )
    # Nuevo campo para la foto de perfil
    foto_perfil = models.ImageField(
        upload_to='clientes/fotos_perfil/',
        null=True,
        blank=True,
        verbose_name="Foto de perfil",
        default='clientes/fotos_perfil/default.png'
    )
    
    def __str__(self):
        nombre_completo = f"{self.usuario.first_name} {self.usuario.last_name}".strip()
        return nombre_completo if nombre_completo else self.usuario.username

    def delete(self, *args, **kwargs):
        # Eliminar la foto de perfil al eliminar el cliente
        if self.foto_perfil and os.path.isfile(self.foto_perfil.path):
            os.remove(self.foto_perfil.path)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"