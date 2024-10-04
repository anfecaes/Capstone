from django import forms
from .models import Homenaje

class HomenajeForm(forms.ModelForm):
    class Meta:
        model = Homenaje
        fields = ['nombre_persona', 'mensaje_homenaje', 'imagen_persona']
        widgets = {
            'mensaje_homenaje': forms.Textarea(attrs={'rows': 4}),
        }
