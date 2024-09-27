from django.shortcuts import render


# Create your views here.
from .models import Funeraria, Cementerio, Mascota

def index(request):
    funerarias = Funeraria.objects.all()
    cementerios = Cementerio.objects.all()
    mascotas = Mascota.objects.all()
    
    return render(request, 'index.html', {
        'funerarias': funerarias,
        'cementerios': cementerios,
        'mascotas': mascotas
    })