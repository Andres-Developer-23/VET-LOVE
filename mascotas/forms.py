from django import forms
from .models import Mascota, HistorialMedico, Vacuna
from datetime import date

class MascotaForm(forms.ModelForm):
    # INFORMACIÓN VITAL PARA EMERGENCIAS (CAMPOS NUEVOS)
    peso_actual = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=True,
        label='<i class="fas fa-weight-scale me-2"></i>Peso Actual (kg) *',
        help_text='Peso exacto en kilogramos para dosificación precisa de medicamentos',
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'step': '0.01',
            'min': '0.1',
            'placeholder': 'Ej: 5.25'
        })
    )
    
    # INFORMACIÓN MÉDICA URGENTE
    URGENCIA_ALERGIAS = [
        ('ninguna', 'No se conocen alergias'),
        ('medicamentos', 'Alergias a Medicamentos'),
        ('alimentos', 'Alergias Alimentarias'),
        ('picaduras', 'Alergias a Picaduras'),
        ('multiple', 'Múltiples Alergias'),
    ]
    
    alergias_urgentes = forms.MultipleChoiceField(
        choices=URGENCIA_ALERGIAS,
        required=False,
        label='<i class="fas fa-allergies me-2"></i>Alergias Conocidas',
        help_text='Seleccione TODAS las alergias conocidas - información vital para emergencias',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    
    alergias_detalle = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'Especifique medicamentos, alimentos específicos, síntomas de reacción y gravedad...'
        }),
        required=False,
        label='Detalle de Alergias',
        help_text='Describa síntomas específicos y protocolo de emergencia si se conoce'
    )
    
    # ENFERMEDADES CRÓNICAS Y CONDICIONES
    ENFERMEDADES_CRONICAS = [
        ('cardiacas', 'Problemas Cardiacos'),
        ('renales', 'Enfermedad Renal'),
        ('hepaticas', 'Problemas Hepáticos'),
        ('diabetes', 'Diabetes'),
        ('epilepsia', 'Epilepsia/Convulsiones'),
        ('artritis', 'Artritis o Problemas Articulares'),
        ('tiroides', 'Problemas de Tiroides'),
        ('respiratorios', 'Problemas Respiratorios'),
        ('ninguna', 'Ninguna enfermedad crónica conocida'),
    ]
    
    enfermedades_cronicas = forms.MultipleChoiceField(
        choices=ENFERMEDADES_CRONICAS,
        required=False,
        label='<i class="fas fa-file-medical me-2"></i>Condiciones Médicas Preexistentes',
        help_text='Seleccione todas las condiciones médicas conocidas para historial completo',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    
    enfermedades_detalle = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'Detalle tratamientos actuales, medicación, dosis, frecuencia y veterinario tratante...'
        }),
        required=False,
        label='Detalle de Tratamientos',
        help_text='Incluya medicación actual, dosis, frecuencia y especialista responsable'
    )
    
    # HISTORIAL QUIRÚRGICO
    CIRUGIAS_PREVIAS = [
        ('esterilizacion', 'Esterilización/Castración'),
        ('fracturas', 'Cirugía por Fracturas'),
        ('tumores', 'Extracción de Tumores'),
        ('dentales', 'Cirugía Dental'),
        ('abdomen', 'Cirugía Abdominal'),
        ('ninguna', 'Ninguna cirugía previa'),
    ]
    
    cirugias_previas = forms.MultipleChoiceField(
        choices=CIRUGIAS_PREVIAS,
        required=False,
        label='<i class="fas fa-procedures me-2"></i>Historial Quirúrgico',
        help_text='Información crucial para anestesia y tratamientos futuros',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    
    fecha_ultima_cirugia = forms.DateField(
        required=False,
        label='Fecha de la Última Cirugía',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    # MEDICACIÓN ACTUAL
    medicacion_actual = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'Ej: Carprofeno 50mg - 1/2 tableta cada 12 horas para dolor articular...'
        }),
        required=True,
        label='<i class="fas fa-pills me-2"></i>Medicación Actual *',
        help_text='Liste TODOS los medicamentos, suplementos, dosis y frecuencia. Si no hay, escriba "Ninguna"'
    )
    
    # COMPORTAMIENTO EN CONSULTA VETERINARIA
    comportamiento_consulta = forms.ChoiceField(
        choices=Mascota.COMPORTAMIENTO_CONSULTA_CHOICES,
        required=True,
        label='<i class="fas fa-heart me-2"></i>Comportamiento en Consulta *',
        help_text='Comportamiento esperado durante exámenes y procedimientos médicos',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # INFORMACIÓN DE CONTACTO DE EMERGENCIA
    veterinario_habitual = forms.CharField(
        max_length=200,
        required=False,
        label='<i class="fas fa-hospital me-2"></i>Veterinario o Clínica Habitual',
        help_text='Nombre de su veterinario de confianza para coordinación de cuidados',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Clínica Veterinaria Central, Dr. García...'
        })
    )
    
    telefono_emergencia = forms.CharField(
        max_length=20,
        required=False,
        label='<i class="fas fa-phone-alt me-2"></i>Teléfono de Emergencias',
        help_text='Número adicional para contactar en situaciones de emergencia',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: +34 600 123 456'
        })
    )
    
    # VACUNACIÓN Y PREVENCIÓN
    estado_vacunacion = forms.ChoiceField(
        choices=Mascota.ESTADO_VACUNACION_CHOICES,
        required=True,
        label='<i class="fas fa-syringe me-2"></i>Estado de Vacunación *',
        help_text='Información crucial para prevención de enfermedades infecciosas',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    fecha_ultima_vacuna = forms.DateField(
        required=False,
        label='Fecha de Última Vacuna',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    # DESPARASITACIÓN
    desparasitacion = forms.ChoiceField(
        choices=Mascota.DESPARASITACION_CHOICES,
        required=True,
        label='<i class="fas fa-bug me-2"></i>Estado de Desparasitación *',
        help_text='Control de parásitos internos y externos para salud integral',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    fecha_ultima_desparasitacion = forms.DateField(
        required=False,
        label='Fecha de Última Desparasitación',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Mascota
        fields = [
            'nombre', 'tipo', 'raza', 'sexo', 'fecha_nacimiento', 
            'foto', 'color', 'caracteristicas', 'microchip'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Ej: Max, Luna, Thor...'
            }),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'raza': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Labrador Retriever, Siamés, Mestizo...'
            }),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'fecha_nacimiento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Negro, Blanco, Atigrado, Dorado...'
            }),
            'caracteristicas': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Marcas distintivas, cicatrices, características físicas únicas para identificación...'
            }),
            'microchip': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '15 dígitos (opcional)'
            }),
        }
        labels = {
            'nombre': '<i class="fas fa-paw me-2"></i>Nombre de la Mascota *',
            'tipo': '<i class="fas fa-dog me-2"></i>Especie *',
            'raza': '<i class="fas fa-dna me-2"></i>Raza o Cruce *',
            'sexo': '<i class="fas fa-venus-mars me-2"></i>Sexo *',
            'fecha_nacimiento': '<i class="fas fa-birthday-cake me-2"></i>Fecha de Nacimiento *',
            'foto': '<i class="fas fa-camera me-2"></i>Fotografía',
            'color': '<i class="fas fa-palette me-2"></i>Color Principal',
            'caracteristicas': '<i class="fas fa-search me-2"></i>Señas Particulares',
            'microchip': '<i class="fas fa-microchip me-2"></i>Número de Microchip',
        }
        help_texts = {
            'nombre': 'Nombre oficial para registros médicos y identificativos',
            'tipo': 'Seleccione la especie para protocolos médicos específicos',
            'raza': 'Raza pura o descripción del cruce (importante para predisposiciones genéticas)',
            'fecha_nacimiento': 'Fecha exacta o estimada (crítica para cálculo de dosis y edad)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Campos obligatorios para atención veterinaria
        required_fields = [
            'nombre', 'tipo', 'raza', 'sexo', 'fecha_nacimiento',
            'peso_actual', 'comportamiento_consulta', 'estado_vacunacion',
            'desparasitacion', 'medicacion_actual'
        ]
        
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({'required': 'required'})

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        if fecha_nacimiento and fecha_nacimiento > date.today():
            raise forms.ValidationError('La fecha de nacimiento no puede ser futura')
        return fecha_nacimiento

    def clean_peso_actual(self):
        peso = self.cleaned_data.get('peso_actual')
        if peso and peso <= 0:
            raise forms.ValidationError('El peso debe ser mayor a 0')
        if peso and peso > 200:
            raise forms.ValidationError('El peso parece ser incorrecto. Por favor verifique.')
        return peso

    def clean_medicacion_actual(self):
        medicacion = self.cleaned_data.get('medicacion_actual')
        if not medicacion or medicacion.strip() == '':
            raise forms.ValidationError(
                'Es crucial informar si la mascota está bajo algún tratamiento médico. '
                'Si no está medicada, escriba explícitamente "Ninguna"'
            )
        return medicacion

    def clean(self):
        cleaned_data = super().clean()
        
        # Validación de alergias
        alergias_urgentes = cleaned_data.get('alergias_urgentes', [])
        alergias_detalle = cleaned_data.get('alergias_detalle', '')
        
        if alergias_urgentes and 'ninguna' in alergias_urgentes and len(alergias_urgentes) > 1:
            self.add_error('alergias_urgentes', 
                          'No puede seleccionar "No se conocen alergias" junto con otros tipos de alergias')
        
        if alergias_urgentes and alergias_urgentes != ['ninguna'] and not alergias_detalle:
            self.add_error('alergias_detalle', 
                          'Por favor detalle las alergias específicas y sus reacciones para nuestro protocolo de seguridad')
        
        # Validación de enfermedades crónicas
        enfermedades = cleaned_data.get('enfermedades_cronicas', [])
        enfermedades_detalle = cleaned_data.get('enfermedades_detalle', '')
        
        if enfermedades and 'ninguna' in enfermedades and len(enfermedades) > 1:
            self.add_error('enfermedades_cronicas', 
                          'No puede seleccionar "Ninguna enfermedad crónica" junto con otras enfermedades')
        
        if enfermedades and enfermedades != ['ninguna'] and not enfermedades_detalle:
            self.add_error('enfermedades_detalle', 
                          'Por favor detalle los tratamientos y seguimiento médico para una atención integral')
        
        return cleaned_data

    def save(self, commit=True):
        mascota = super().save(commit=False)
        
        # Guardar campos adicionales en el modelo Mascota
        mascota.alergias_conocidas = self.cleaned_data.get('alergias_detalle', '')
        mascota.alergias_tipo = ', '.join(self.cleaned_data.get('alergias_urgentes', []))
        mascota.enfermedades_cronicas = self.cleaned_data.get('enfermedades_detalle', '')
        mascota.enfermedades_tipo = ', '.join(self.cleaned_data.get('enfermedades_cronicas', []))
        mascota.cirugias_previas = ', '.join(self.cleaned_data.get('cirugias_previas', []))
        
        # Guardar información adicional
        mascota.peso_actual = self.cleaned_data.get('peso_actual')
        mascota.medicacion_actual = self.cleaned_data.get('medicacion_actual', '')
        mascota.comportamiento_consulta = self.cleaned_data.get('comportamiento_consulta', '')
        mascota.veterinario_habitual = self.cleaned_data.get('veterinario_habitual', '')
        mascota.telefono_emergencia = self.cleaned_data.get('telefono_emergencia', '')
        mascota.estado_vacunacion = self.cleaned_data.get('estado_vacunacion', '')
        mascota.fecha_ultima_vacuna = self.cleaned_data.get('fecha_ultima_vacuna')
        mascota.desparasitacion = self.cleaned_data.get('desparasitacion', '')
        mascota.fecha_ultima_desparasitacion = self.cleaned_data.get('fecha_ultima_desparasitacion')
        mascota.fecha_ultima_cirugia = self.cleaned_data.get('fecha_ultima_cirugia')
        
        if commit:
            mascota.save()
        return mascota


class HistorialMedicoForm(forms.ModelForm):
    # Signos vitales
    temperatura = forms.DecimalField(
        max_digits=4, 
        decimal_places=1,
        required=False,
        min_value=35.0,
        max_value=42.0,
        label='<i class="fas fa-thermometer-half me-2"></i>Temperatura (°C)',
        help_text='Rango normal: 38.0-39.2°C (perros), 38.0-39.5°C (gatos)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'Ej: 38.5'
        })
    )
    
    frecuencia_cardiaca = forms.IntegerField(
        required=False,
        min_value=40,
        max_value=240,
        label='<i class="fas fa-heartbeat me-2"></i>Frecuencia Cardíaca (lpm)',
        help_text='Latidos por minuto - Rango normal: 60-140 (perros), 140-220 (gatos)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 120'
        })
    )
    
    frecuencia_respiratoria = forms.IntegerField(
        required=False,
        min_value=10,
        max_value=100,
        label='<i class="fas fa-wind me-2"></i>Frecuencia Respiratoria (rpm)',
        help_text='Respiraciones por minuto - Rango normal: 10-30',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 20'
        })
    )
    
    condicion_corporal = forms.ChoiceField(
        choices=HistorialMedico.CONDICION_CORPORAL_CHOICES,
        required=False,
        label='<i class="fas fa-weight me-2"></i>Condición Corporal',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Historial de la visita
    motivo_consulta = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'Describa los síntomas, duración, evolución del problema y cualquier cambio observado...'
        }),
        required=True,
        label='<i class="fas fa-stethoscope me-2"></i>Motivo de la Consulta *',
        help_text='Describa detalladamente los síntomas y duración del problema'
    )
    
    vacunas_aplicadas = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 2,
            'class': 'form-control',
            'placeholder': 'Nombre de la vacuna, número de lote, fecha de aplicación, sitio de aplicación...'
        }),
        required=False,
        label='<i class="fas fa-syringe me-2"></i>Vacunas Aplicadas',
        help_text='Vacunas administradas durante esta consulta'
    )
    
    proxima_cita = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label='<i class="fas fa-calendar-alt me-2"></i>Próxima Cita Programada'
    )

    class Meta:
        model = HistorialMedico
        fields = [
            'veterinario', 
            'diagnostico', 
            'tratamiento', 
            'observaciones', 
            'peso'
        ]
        widgets = {
            'veterinario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del veterinario responsable'
            }),
            'diagnostico': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Diagnóstico principal, diagnósticos diferenciales, hallazgos clínicos, pruebas realizadas...'
            }),
            'tratamiento': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Medicamentos prescritos, dosis exactas, frecuencia, duración, instrucciones específicas...'
            }),
            'observaciones': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Recomendaciones adicionales, cuidados en casa, observaciones del propietario, pronóstico...'
            }),
            'peso': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Peso en kilogramos'
            }),
        }
        labels = {
            'veterinario': '<i class="fas fa-user-md me-2"></i>Veterinario Responsable *',
            'diagnostico': '<i class="fas fa-diagnoses me-2"></i>Diagnóstico *',
            'tratamiento': '<i class="fas fa-prescription me-2"></i>Tratamiento Prescrito *',
            'observaciones': '<i class="fas fa-clipboard-list me-2"></i>Observaciones y Recomendaciones',
            'peso': '<i class="fas fa-weight-scale me-2"></i>Peso Actual (kg) *',
        }
        help_texts = {
            'peso': 'Peso actual en kilogramos con dos decimales para precisión médica',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = ['veterinario', 'diagnostico', 'tratamiento', 'peso', 'motivo_consulta']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({'required': 'required'})

    def clean_peso(self):
        peso = self.cleaned_data.get('peso')
        if peso and peso <= 0:
            raise forms.ValidationError('El peso debe ser mayor a 0')
        return peso

    def clean_temperatura(self):
        temperatura = self.cleaned_data.get('temperatura')
        if temperatura and (temperatura < 35.0 or temperatura > 42.0):
            raise forms.ValidationError('La temperatura debe estar entre 35.0°C y 42.0°C')
        return temperatura

    def save(self, commit=True):
        historial = super().save(commit=False)
        
        # Guardar campos adicionales
        historial.temperatura = self.cleaned_data.get('temperatura')
        historial.frecuencia_cardiaca = self.cleaned_data.get('frecuencia_cardiaca')
        historial.frecuencia_respiratoria = self.cleaned_data.get('frecuencia_respiratoria')
        historial.condicion_corporal = self.cleaned_data.get('condicion_corporal')
        historial.motivo_consulta = self.cleaned_data.get('motivo_consulta')
        historial.vacunas_aplicadas = self.cleaned_data.get('vacunas_aplicadas', '')
        historial.proxima_cita = self.cleaned_data.get('proxima_cita')
        
        if commit:
            historial.save()
        return historial


class VacunaForm(forms.ModelForm):
    # Información de la vacuna
    lote = forms.CharField(
        max_length=20,
        required=True,
        label='<i class="fas fa-barcode me-2"></i>Número de Lote *',
        help_text='Número de lote del fabricante para trazabilidad',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: A123B456C789'
        })
    )
    
    laboratorio = forms.CharField(
        max_length=100,
        required=True,
        label='<i class="fas fa-industry me-2"></i>Laboratorio Fabricante *',
        help_text='Empresa fabricante de la vacuna',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Zoetis, MSD, Virbac...'
        })
    )
    
    # Información de aplicación
    via_aplicacion = forms.ChoiceField(
        choices=Vacuna.VIA_APLICACION_CHOICES,
        initial='subcutanea',
        label='<i class="fas fa-tint me-2"></i>Vía de Aplicación',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    sitio_aplicacion = forms.CharField(
        max_length=100,
        required=False,
        label='<i class="fas fa-map-marker-alt me-2"></i>Sitio de Aplicación',
        help_text='Ej: Tercio posterior derecho, región escapular izquierda...',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Región escapular derecha'
        })
    )
    
    reacciones_adversas = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 2,
            'class': 'form-control',
            'placeholder': 'Describa cualquier reacción presentada post-vacunación (fiebre, edema, letargo, etc.)...'
        }),
        required=False,
        label='<i class="fas fa-exclamation-triangle me-2"></i>Reacciones Adversas',
        help_text='Describa cualquier reacción presentada post-vacunación'
    )

    class Meta:
        model = Vacuna
        fields = [
            'nombre', 
            'fecha_aplicacion', 
            'fecha_proxima', 
            'aplicada'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Vacuna Rabia, Polivalente Canina, Triple Felina...'
            }),
            'fecha_aplicacion': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'fecha_proxima': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'aplicada': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'nombre': '<i class="fas fa-syringe me-2"></i>Nombre de la Vacuna *',
            'fecha_aplicacion': '<i class="fas fa-calendar-day me-2"></i>Fecha de Aplicación *',
            'fecha_proxima': '<i class="fas fa-calendar-check me-2"></i>Fecha de Próxima Aplicación *',
            'aplicada': '<i class="fas fa-check-circle me-2"></i>¿Vacuna aplicada en esta visita?',
        }
        help_texts = {
            'nombre': 'Nombre comercial o técnico de la vacuna',
            'fecha_aplicacion': 'Fecha en que se administró la vacuna',
            'fecha_proxima': 'Fecha recomendada para la siguiente dosis según protocolo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = ['nombre', 'fecha_aplicacion', 'fecha_proxima', 'lote', 'laboratorio']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({'required': 'required'})

    def clean(self):
        cleaned_data = super().clean()
        fecha_aplicacion = cleaned_data.get('fecha_aplicacion')
        fecha_proxima = cleaned_data.get('fecha_proxima')

        if fecha_proxima and fecha_aplicacion and fecha_proxima <= fecha_aplicacion:
            raise forms.ValidationError({
                'fecha_proxima': 'La próxima aplicación debe ser posterior a la fecha de aplicación actual'
            })
        
        return cleaned_data

    def save(self, commit=True):
        vacuna = super().save(commit=False)
        
        # Guardar campos adicionales
        vacuna.lote = self.cleaned_data.get('lote')
        vacuna.laboratorio = self.cleaned_data.get('laboratorio')
        vacuna.via_aplicacion = self.cleaned_data.get('via_aplicacion')
        vacuna.sitio_aplicacion = self.cleaned_data.get('sitio_aplicacion', '')
        vacuna.reacciones_adversas = self.cleaned_data.get('reacciones_adversas', '')
        
        if commit:
            vacuna.save()
        return vacuna