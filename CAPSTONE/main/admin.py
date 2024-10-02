from django import forms
from django.contrib import admin
from django.utils.html import format_html
from io import BytesIO
from PIL import Image
import base64
from .models import ServiciosMascotas, Funeraria, Cementerio

# Formulario personalizado para ServiciosMascotas
class ServiciosMascotasAdminForm(forms.ModelForm):
    imagen_upload = forms.ImageField(required=False, label="Cargar imagen")  # Campo de imagen

    class Meta:
        model = ServiciosMascotas
        fields = ['nombre', 'direccion', 'telefono', 'email', 'imagen_upload']

    def save(self, commit=True):
        instance = super(ServiciosMascotasAdminForm, self).save(commit=False)
        imagen_upload = self.cleaned_data.get('imagen_upload')
        if imagen_upload:
            image = Image.open(imagen_upload)
            img_bytes = BytesIO()
            image.save(img_bytes, format=image.format)
            instance.imagen = img_bytes.getvalue()

        if commit:
            instance.save()
        return instance

# Formulario personalizado para Funeraria
class FunerariaAdminForm(forms.ModelForm):
    imagen_upload = forms.ImageField(required=False, label="Cargar imagen")  # Campo de imagen

    class Meta:
        model = Funeraria
        fields = ['nombre', 'direccion', 'telefono', 'email', 'imagen_upload']

    def save(self, commit=True):
        instance = super(FunerariaAdminForm, self).save(commit=False)
        imagen_upload = self.cleaned_data.get('imagen_upload')
        if imagen_upload:
            image = Image.open(imagen_upload)
            img_bytes = BytesIO()
            image.save(img_bytes, format=image.format)
            instance.imagen = img_bytes.getvalue()

        if commit:
            instance.save()
        return instance

# Formulario personalizado para Cementerio
class CementerioAdminForm(forms.ModelForm):
    imagen_upload = forms.ImageField(required=False, label="Cargar imagen")  # Campo de imagen

    class Meta:
        model = Cementerio
        fields = ['nombre', 'direccion', 'telefono', 'imagen_upload']

    def save(self, commit=True):
        instance = super(CementerioAdminForm, self).save(commit=False)
        imagen_upload = self.cleaned_data.get('imagen_upload')
        if imagen_upload:
            image = Image.open(imagen_upload)
            img_bytes = BytesIO()
            image.save(img_bytes, format=image.format)
            instance.imagen = img_bytes.getvalue()

        if commit:
            instance.save()
        return instance

# Admin personalizado para ServiciosMascotas
@admin.register(ServiciosMascotas)
class ServiciosMascotasAdmin(admin.ModelAdmin):
    form = ServiciosMascotasAdminForm
    list_display = ('id_servi_mascota', 'nombre', 'direccion', 'telefono', 'email', 'imagen_tag')
    search_fields = ('nombre', 'direccion', 'telefono', 'email')

    def imagen_tag(self, obj):
        if obj.imagen:
            image_base64 = base64.b64encode(obj.imagen).decode('utf-8')
            return format_html('<img src="data:image/png;base64,{}" width="50" height="50" />'.format(image_base64))
        return "No image"
    imagen_tag.short_description = 'Imagen'

# Admin personalizado para Funeraria
@admin.register(Funeraria)
class FunerariaAdmin(admin.ModelAdmin):
    form = FunerariaAdminForm
    list_display = ('id_funeraria', 'nombre', 'direccion', 'telefono', 'email', 'imagen_tag')
    search_fields = ('nombre', 'direccion', 'telefono', 'email')

    def imagen_tag(self, obj):
        if obj.imagen:
            image_base64 = base64.b64encode(obj.imagen).decode('utf-8')
            return format_html('<img src="data:image/png;base64,{}" width="50" height="50" />'.format(image_base64))
        return "No image"
    imagen_tag.short_description = 'Imagen'

# Admin personalizado para Cementerio
@admin.register(Cementerio)
class CementerioAdmin(admin.ModelAdmin):
    form = CementerioAdminForm
    list_display = ('id_cementerio', 'nombre', 'direccion', 'telefono', 'imagen_tag')
    search_fields = ('nombre', 'direccion', 'telefono')

    def imagen_tag(self, obj):
        if obj.imagen:
            image_base64 = base64.b64encode(obj.imagen).decode('utf-8')
            return format_html('<img src="data:image/png;base64,{}" width="50" height="50" />'.format(image_base64))
        return "No image"
    imagen_tag.short_description = 'Imagen'
