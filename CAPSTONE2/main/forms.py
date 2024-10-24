# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Homenaje, Condolencia, TipoServicio, ServicioAdicional, Ubicacion, Beneficio, Mascota


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Asegúrate de que el email sea obligatorio
    rut = forms.CharField(max_length=12)  # Agrega el campo rut
    telefono = forms.CharField(max_length=15)  # Agrega el campo telefono
    class Meta:
        model = Usuario  # Usa el modelo de usuario personalizado
        fields = ('username', 'rut', 'telefono', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.rut = self.cleaned_data['rut']
        user.telefono = self.cleaned_data['telefono']
        if commit:
            user.save()
        return user

class HomenajeForm(forms.ModelForm):
    class Meta:
        model = Homenaje
        fields = ['titulo', 'mensaje', 'es_para_mascota', 'imagen', 'video', 'invitados']
        widgets = {
            'invitados': forms.CheckboxSelectMultiple,  # Para seleccionar múltiples invitados
        }

class CondolenciaForm(forms.ModelForm):
    class Meta:
        model = Condolencia
        fields = ['mensaje']  # Solo se solicitará el mensaje
        widgets = {
            'mensaje': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe aquí tu condolencia...',
                'rows': 3,
                'style': 'resize: none;'
            }),
        }
        labels = {
            'mensaje': 'Mensaje de Condolencia'
        }
        
# implementación calculadora

class CotizacionForm(forms.Form):
    tipo_servicio = forms.ModelChoiceField(
        queryset=TipoServicio.objects.all(),
        label="Tipo de Servicio",
        empty_label="Seleccione un servicio"
    )
    ubicacion = forms.ModelChoiceField(
        queryset=Ubicacion.objects.all(),
        label="Ubicación",
        empty_label="Seleccione una ubicación"
    )
    servicios_adicionales = forms.ModelMultipleChoiceField(
        queryset=ServicioAdicional.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Servicios Adicionales",
        required=False
    )
    beneficio = forms.ModelChoiceField(
        queryset=Beneficio.objects.all(),
        label="Beneficio",
        required=False,
        empty_label="Sin beneficio"
    )


#Mascota
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