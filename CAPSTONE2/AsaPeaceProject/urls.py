from django.contrib import admin
from django.urls import path
from main import views  # Importa tus vistas de la aplicación "main"
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from main.views import cotizacion_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('ask', views.ask, name='ask'),  
    path('ubicacion/', views.encontrar_funeraria_cercana, name='ubicacion'),  # Nueva ruta

    path('registro/', views.registro, name='registro'),
    
    path('login/', views.login_view, name='login'),  # Vista de login
    path('logout/', auth_views.LogoutView.as_view(next_page='homepage'), name='logout'),

    
    # homenajes
    
    path('crear-homenaje/', views.crear_homenaje, name='crear_homenaje'),
    path('homenaje/<slug:slug>/', views.ver_homenaje, name='ver_homenaje'),
    path('homenaje-compartido/<slug:slug>/', views.homenaje_compartido, name='homenaje_compartido'),
    path('historial-homenajes/', views.historial_homenajes, name='historial_homenajes'),
    # Recuperar contraseña
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='main/password_reset.html'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='main/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset_complete.html'), 
         name='password_reset_complete'),
#     calculadora
     path('cotizacion/', cotizacion_view, name='cotizacion'),
#     Mascotas
     path('mascotas/', views.mascotas, name='mascotas'),
     path('mascotas/agregar/', views.agregar_mascota, name='agregar_mascota'),
     path('mascotas/listar/', views.lista_mascotas, name='listar_mascotas'),
     
     #calificacion
     path('calificar/<int:content_type_id>/<int:object_id>/', views.agregar_calificacion, name='agregar_calificacion'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
