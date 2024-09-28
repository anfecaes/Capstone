from django.shortcuts import render
from .models import Funeraria, Cementerio, Mascota

def homepage(request):
    funerarias = Funeraria.objects.all()
    cementerios = Cementerio.objects.all()
    mascotas = Mascota.objects.all()
    
    return render(request, 'main/index.html', {
        'funerarias': funerarias,
        'cementerios': cementerios,
        'mascotas': mascotas
    })
   
