from django.contrib import admin
from django.urls import path
from main import views  # Importa tus vistas de la aplicación "main"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),  # Ruta para la página principal
]
