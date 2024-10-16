from django import forms
from .models import Mascota

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'foto', 'descripcion', 'edad', 'vacunas_al_dia', 'documento_vacunas', 'motivo', 'contacto']
        widgets = {
            'foto': forms.ClearableFileInput(attrs={'accept': 'image/png, image/jpeg'}),
            'documento_vacunas': forms.ClearableFileInput(attrs={'accept': 'image/png, image/jpeg'}),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'motivo': forms.Textarea(attrs={'rows': 4}),
            'contacto': forms.TextInput(attrs={'placeholder': 'Teléfono, Facebook, etc.'}),
        }

