from django.shortcuts import render
from .models import Funeraria, Cementerio, ServiciosMascotas
import base64

def homepage(request):
    funerarias = Funeraria.objects.all()
    cementerios = Cementerio.objects.all()
    mascotas = ServiciosMascotas.objects.all()
    
    # Convertir las imágenes a base64 para cada funeraria
    for funeraria in funerarias:
        if funeraria.imagen:
            funeraria.imagen_base64 = base64.b64encode(funeraria.imagen).decode('utf-8')

    # Convertir las imágenes a base64 para cada cementerio
    for cementerio in cementerios:
        if cementerio.imagen:
            cementerio.imagen_base64 = base64.b64encode(cementerio.imagen).decode('utf-8')

    # Convertir las imágenes a base64 para cada servicio de mascotas
    for mascota in mascotas:
        if mascota.imagen:
            mascota.imagen_base64 = base64.b64encode(mascota.imagen).decode('utf-8')

    return render(request, 'main/index.html', {
        'funerarias': funerarias,
        'cementerios': cementerios,
        'mascotas': mascotas
    })