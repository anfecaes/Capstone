from django.contrib import admin
from django.urls import path
from main import views  # Importa tus vistas de la aplicación "main"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('mascotas/', views.mascotas, name='mascotas'),  # Asegúrate de agregar la barra diagonal
    path('ask', views.ask, name='ask'),  # Asegúrate de agregar la barra diagonal
    path('ubicacion/', views.encontrar_funeraria_cercana, name='ubicacion'),  # Nueva ruta
    path('generar_pdf/', views.generar_pdf, name='generar_pdf'),  # Ruta para generar el PDF
]
