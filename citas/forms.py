from django import forms
from .models import Cita
from mascotas.models import Mascota
from django.utils import timezone
from datetime import time

class CitaForm(forms.ModelForm):
    mascota = forms.ModelChoiceField(
        queryset=Mascota.objects.none(),
        empty_label="Selecciona una mascota",
        label="Mascota",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = Cita
        fields = ['mascota', 'fecha', 'tipo', 'motivo']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'motivo': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
        labels = {
            'fecha': 'Fecha y Hora',
            'tipo': 'Tipo de Cita',
            'motivo': 'Motivo de la Consulta'
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user and hasattr(self.user, 'cliente'):
            self.fields['mascota'].queryset = Mascota.objects.filter(cliente=self.user.cliente)
    
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        
        if fecha:
            # No permitir citas en el pasado
            if fecha < timezone.now():
                raise forms.ValidationError("No puedes agendar una cita en el pasado.")
            
            # Validar horario de atención (ejemplo: 8am a 6pm)
            hora = fecha.time()
            if hora < time(8, 0) or hora > time(18, 0):
                raise forms.ValidationError("El horario de atención es de 8:00 am a 6:00 pm.")
            
            # Validar que no sea domingo
            if fecha.weekday() == 6:  # Domingo
                raise forms.ValidationError("No atendemos los domingos.")
        
        return fecha