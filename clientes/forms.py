from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente
from django.core.exceptions import ValidationError
import re

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    first_name = forms.CharField(required=True, label="Nombre")
    last_name = forms.CharField(required=True, label="Apellidos")
    
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")
        labels = {
            'username': 'Nombre de usuario',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }
        help_texts = {
            'username': 'Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.',
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[\w.@+-]+$', username):
            raise ValidationError("El nombre de usuario solo puede contener letras, números y los caracteres @/./+/-/_.")
        return username

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
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cedula', 'telefono', 'direccion', 'preferencias_comunicacion', 'foto_perfil']
        labels = {
            'cedula': 'Cédula',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'preferencias_comunicacion': 'Preferencia de comunicación',
            'foto_perfil': 'Foto de perfil'
        }
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ingresa tu dirección completa'}),
            'telefono': forms.TextInput(attrs={'placeholder': '+34 123 456 789'}),
            'cedula': forms.TextInput(attrs={'placeholder': 'Ingresa tu número de cédula'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cedula'].required = False
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        # Validación básica de teléfono
        if telefono and not re.match(r'^[\d\s\+\(\)\-]+$', telefono):
            raise ValidationError("Ingrese un número de teléfono válido.")
        return telefono

class RegistroClienteForm(forms.ModelForm):
    acepto_terminos = forms.BooleanField(required=True, label="Acepto los términos y condiciones")

    class Meta:
        model = Cliente
        fields = ['cedula', 'telefono', 'direccion', 'preferencias_comunicacion']
        labels = {
            'cedula': 'Cédula',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'preferencias_comunicacion': 'Preferencia de comunicación'
        }
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ingresa tu dirección completa'}),
            'telefono': forms.TextInput(attrs={'placeholder': '+34 123 456 789'}),
            'cedula': forms.TextInput(attrs={'placeholder': 'Ingresa tu número de cédula'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cedula'].required = False
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        # Validación básica de teléfono
        if not re.match(r'^[\d\s\+\(\)\-]+$', telefono):
            raise ValidationError("Ingrese un número de teléfono válido.")
        return telefono