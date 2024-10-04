from django.contrib import admin
from django.urls import path
from main import views  # Importa tus vistas de la aplicación "main"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('ask', views.ask, name='ask'),  
    path('ubicacion/', views.encontrar_funeraria_cercana, name='ubicacion'),  # Nueva ruta
    path('crear-homenaje/', views.crear_homenaje, name='crear_homenaje'),  #homenajes

]
