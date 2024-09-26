from django.shortcuts import render


# Create your views here.
from .models import Funeraria, Cementerio

def index(request):
    funerarias = Funeraria.objects.all()  # Obtén todos los registros de la tabla Funeraria
    return render(request, 'index.html', {'funerarias': funerarias})

def cementerio(request):
    cementerio = Cementerio.objects.all()
    return render(request, 'index.html', {'cementerio': cementerio})