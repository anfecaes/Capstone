#archivo url portalfunerapp
from django.urls import path
from .views import home, get_funeral_services

urlpatterns = [
    path('', home, name='home'),
# url que peritira cominicarse con la vista de la api
    path('', get_funeral_services, name='home'), 
]