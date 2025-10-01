from django import forms
from .models import Orden

class OrdenForm(forms.Form):
    direccion_envio = forms.CharField(
        label='Dirección de envío',
        widget=forms.Textarea(attrs={
            'rows': 3, 
            'placeholder': 'Ingresa tu dirección completa para el envío',
            'class': 'form-control'
        }),
        required=True
    )
    notas = forms.CharField(
        label='Notas adicionales (opcional)',
        widget=forms.Textarea(attrs={
            'rows': 2, 
            'placeholder': 'Instrucciones especiales o comentarios',
            'class': 'form-control'
        }),
        required=False
    )