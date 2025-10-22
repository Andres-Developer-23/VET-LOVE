from django import forms
from .models import Orden, Comentario

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

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['calificacion', 'comentario']
        widgets = {
            'calificacion': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'comentario': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Comparte tu experiencia con este producto...',
                'class': 'form-control'
            })
        }
        labels = {
            'calificacion': 'Calificación',
            'comentario': 'Comentario'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que el campo de calificación sea requerido
        self.fields['calificacion'].required = True
        self.fields['comentario'].required = True