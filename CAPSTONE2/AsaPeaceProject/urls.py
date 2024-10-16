from django.contrib import admin
from django.urls import path
from main import views  # Importa tus vistas de la aplicación "main"
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('mascotas/', views.mascotas, name='mascotas'),  # Asegúrate de agregar la barra diagonal
    path('ask', views.ask, name='ask'),  # Asegúrate de agregar la barra diagonal
    path('ubicacion/', views.encontrar_funeraria_cercana, name='ubicacion'),  # Nueva ruta
    path('generar_pdf/', views.generar_pdf, name='generar_pdf'),  # Ruta para generar el PDF
    path('agregar_mascota/', views.agregar_mascota, name='agregar_mascota'),
    path('lista_mascotas/', views.lista_mascotas, name='lista_mascotas'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)