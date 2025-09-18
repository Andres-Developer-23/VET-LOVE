from django import forms
from .models import Mascota, HistorialMedico, Vacuna

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'tipo', 'raza', 'sexo', 'fecha_nacimiento', 'foto', 'caracteristicas']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'caracteristicas': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'nombre': 'Nombre de la mascota',
            'tipo': 'Tipo de animal',
            'raza': 'Raza',
            'sexo': 'Sexo',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'foto': 'Foto',
            'caracteristicas': 'Características especiales',
        }

class HistorialMedicoForm(forms.ModelForm):
    class Meta:
        model = HistorialMedico
        fields = ['veterinario', 'diagnostico', 'tratamiento', 'observaciones', 'peso']
        widgets = {
            'diagnostico': forms.Textarea(attrs={'rows': 4}),
            'tratamiento': forms.Textarea(attrs={'rows': 3}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'veterinario': 'Veterinario que atendió',
            'diagnostico': 'Diagnóstico',
            'tratamiento': 'Tratamiento',
            'observaciones': 'Observaciones',
            'peso': 'Peso (kg)',
        }

class VacunaForm(forms.ModelForm):
    class Meta:
        model = Vacuna
        fields = ['nombre', 'fecha_aplicacion', 'fecha_proxima', 'aplicada']
        widgets = {
            'fecha_aplicacion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_proxima': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'nombre': 'Nombre de la vacuna',
            'fecha_aplicacion': 'Fecha de aplicación',
            'fecha_proxima': 'Próxima aplicación',
            'aplicada': '¿Ya fue aplicada?',
        }