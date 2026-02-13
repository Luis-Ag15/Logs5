from django import forms
from .models import Paciente



class PacienteForm(forms.ModelForm):
    foto_perfil = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )
    foto_resultado = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )


    class Meta:
        model = Paciente
        fields = [
            'id',
            'nombre',
            'edad',
            'sexo',
            # 'email', # REMOVIDO
            'telefono',
            'datos_medico',
            'informacion_clinica',
            'resultado_prueba',
            'foto_perfil',
            'foto_resultado',
        ]

        widgets = {
            'id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código alfanumérico'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'edad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Edad'
            }),
            'sexo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '55-2478-5578'
            }),
            'datos_medico': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Datos del médico...'
            }),
            'informacion_clinica': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Información clínica...'
            }),
            'resultado_prueba': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Resultado de la prueba...'
            }),
        }
