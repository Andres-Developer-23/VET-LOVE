from django import forms
from django.contrib.auth.models import User
from .models import Cliente

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico'
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['telefono', 'direccion', 'preferencias_comunicacion', 'foto_perfil']
        labels = {
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'preferencias_comunicacion': 'Preferencia de comunicación',
            'foto_perfil': 'Foto de perfil'
        }
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3}),
            'telefono': forms.TextInput(attrs={'placeholder': '+34 123 456 789'})
        }
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        # Validación básica de teléfono
        if not telefono.replace(' ', '').replace('+', '').isdigit():
            raise forms.ValidationError("Ingrese un número de teléfono válido.")
        return telefono