from django import forms
from .models import Cita
from mascotas.models import Mascota
from django.utils import timezone
from datetime import time, datetime
import re

class CitaForm(forms.ModelForm):
    mascota = forms.ModelChoiceField(
        queryset=Mascota.objects.none(),
        empty_label="Selecciona una mascota",
        label="Mascota Paciente",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    telefono_contacto = forms.CharField(
        max_length=15,
        required=True,
        label="Teléfono de Contacto",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+34 123 456 789'
        })
    )
    
    email_contacto = forms.EmailField(
        required=True,
        label="Email de Contacto",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@email.com'
        })
    )
    
    class Meta:
        model = Cita
        fields = [
            'mascota', 'fecha', 'tipo', 'prioridad', 'motivo', 'sintomas',
            'antecedentes', 'medicamentos_actuales', 'alergias', 'telefono_contacto',
            'email_contacto'
        ]
        widgets = {
            'fecha': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 
                'class': 'form-control',
                'min': datetime.now().strftime('%Y-%m-%dT%H:%M')
            }),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
            'motivo': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'form-control',
                'placeholder': 'Describa el motivo principal de la consulta...'
            }),
            'sintomas': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'form-control',
                'placeholder': 'Describa los síntomas que presenta la mascota...'
            }),
            'antecedentes': forms.Textarea(attrs={
                'rows': 2, 
                'class': 'form-control',
                'placeholder': 'Enfermedades previas, cirugías, condiciones crónicas...'
            }),
            'medicamentos_actuales': forms.Textarea(attrs={
                'rows': 2, 
                'class': 'form-control',
                'placeholder': 'Medicamentos, suplementos o tratamientos actuales...'
            }),
            'alergias': forms.Textarea(attrs={
                'rows': 2, 
                'class': 'form-control',
                'placeholder': 'Alergias a medicamentos, alimentos, etc...'
            }),
        }
        labels = {
            'fecha': 'Fecha y Hora Preferidas',
            'tipo': 'Tipo de Consulta',
            'prioridad': 'Nivel de Urgencia',
            'motivo': 'Motivo Principal de la Consulta',
            'sintomas': 'Síntomas Presentados',
            'antecedentes': 'Antecedentes Médicos Relevantes',
            'medicamentos_actuales': 'Medicamentos y Tratamientos Actuales',
            'alergias': 'Alergias Conocidas',
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user and hasattr(self.user, 'cliente'):
            self.fields['mascota'].queryset = Mascota.objects.filter(cliente=self.user.cliente)
            
            # Pre-cargar información del cliente
            if self.user.cliente.telefono:
                self.fields['telefono_contacto'].initial = self.user.cliente.telefono
            if self.user.email:
                self.fields['email_contacto'].initial = self.user.email
    
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        
        if fecha:
            # No permitir citas en el pasado
            if fecha < timezone.now():
                raise forms.ValidationError("No puedes agendar una cita en el pasado.")
            
            # Validar horario de atención (8am a 8pm)
            hora = fecha.time()
            if hora < time(8, 0) or hora > time(20, 0):
                raise forms.ValidationError("El horario de atención es de 8:00 am a 8:00 pm.")
            
            # Validar que no sea domingo
            if fecha.weekday() == 6:  # Domingo
                raise forms.ValidationError("No atendemos los domingos.")
            
            # Validar que no sea en más de 30 días
            if fecha > timezone.now() + timezone.timedelta(days=30):
                raise forms.ValidationError("No se pueden agendar citas con más de 30 días de anticipación.")
        
        return fecha
    
    def clean_telefono_contacto(self):
        telefono = self.cleaned_data.get('telefono_contacto')
        if telefono:
            # Validar formato básico de teléfono
            patron = r'^[\+]?[0-9\s\-\(\)]{9,15}$'
            if not re.match(patron, telefono):
                raise forms.ValidationError("Por favor ingresa un número de teléfono válido.")
        return telefono
    
    def clean(self):
        cleaned_data = super().clean()
        prioridad = cleaned_data.get('prioridad')
        sintomas = cleaned_data.get('sintomas', '')
        mascota = cleaned_data.get('mascota')
        
        # Si es urgente o emergencia, requerir descripción de síntomas
        if prioridad in ['urgente', 'emergencia'] and not sintomas.strip():
            self.add_error('sintomas', 'Para citas urgentes o de emergencia, es obligatorio describir los síntomas.')
        
        # Validar que la mascota tenga información de edad si es relevante
        if mascota:
            tiene_edad = False
            if hasattr(mascota, 'fecha_nacimiento') and mascota.fecha_nacimiento:
                tiene_edad = True
            if hasattr(mascota, 'edad_aproximada') and mascota.edad_aproximada:
                tiene_edad = True
                
            if not tiene_edad:
                self.add_error('mascota', 'Esta mascota no tiene información de edad. Por favor actualiza su perfil en la sección de mascotas.')
        
        return cleaned_data

class CitaAdminForm(forms.ModelForm):
    """Formulario para el panel de administración con campos adicionales"""
    
    class Meta:
        model = Cita
        fields = '__all__'
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'duracion_estimada': forms.NumberInput(attrs={'min': 15, 'max': 240, 'step': 15}),
        }