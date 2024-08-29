
from django.shortcuts import render, requests

def home(request):
    return render(request, 'home.html')
# Create your views here.

def get_funeral_services(request):
    api_url = "https://api.funeralmarket.cl/funeral_services"  # URL de la API (ejemplo)
    headers = {
        'Authorization': 'Bearer tu_clave_de_api'
    }
    
    response = requests.get(api_url, headers=headers)
    services = []
    
    if response.status_code == 200:
        services = response.json()  # Asume que la respuesta es un JSON
    
    context = {
        'services': services
    }
    
    return render(request, 'portalfunerapp/home.html', context)