from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import json
from .models import Funeraria, Cementerio, ServiciosMascotas, Homenaje, Mascota
import base64
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
# homenajes
# from django.core.mail import send_mail
# from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
#importaciones para loguear
from .forms import HomenajeForm, RegistroForm, CondolenciaForm, CotizacionForm, MascotaForm, CalificacionForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
#Mascotas
from django.contrib import messages  # Para mostrar mensajes de éxito

import time
from django.core.files.uploadedfile import UploadedFile
#calificaciones
from django.core.exceptions import FieldError
from django.http import HttpResponseNotFound
from django.db.models import Avg

# Asegúrate de que tu clave API de OpenAI esté configurada correctamente
openai.api_key = 'api'

from django.contrib.auth.models import AnonymousUser

from django.contrib.contenttypes.models import ContentType

def homepage(request):
    try:
        # Verificar si el usuario está autenticado
        if request.user.is_authenticated:
            homenajes_creados = Homenaje.objects.filter(autor=request.user).order_by('-fecha_publicacion')
            homenajes_invitados = Homenaje.objects.filter(invitados=request.user).order_by('-fecha_publicacion')
            homenajes = homenajes_creados | homenajes_invitados
        else:
            homenajes = Homenaje.objects.none()

        # Obtener funerarias, cementerios y servicios de mascotas
        funerarias = Funeraria.objects.all()
        cementerios = Cementerio.objects.all()
        mascotas = ServiciosMascotas.objects.all()

        # Obtener ContentType para cada modelo
        funeraria_content_type = ContentType.objects.get_for_model(Funeraria)
        cementerio_content_type = ContentType.objects.get_for_model(Cementerio)
        mascota_content_type = ContentType.objects.get_for_model(ServiciosMascotas)

        # Convertir imágenes a Base64
        for funeraria in funerarias:
            if funeraria.imagen:
                funeraria.imagen_base64 = base64.b64encode(funeraria.imagen).decode('utf-8')

        for cementerio in cementerios:
            if cementerio.imagen:
                cementerio.imagen_base64 = base64.b64encode(cementerio.imagen).decode('utf-8')

        for mascota in mascotas:
            if mascota.imagen:
                mascota.imagen_base64 = base64.b64encode(mascota.imagen).decode('utf-8')

        # Procesar formulario de homenaje
        if request.method == 'POST' and request.user.is_authenticated:
            form = HomenajeForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('homepage')
        else:
            form = HomenajeForm()

        # Renderizar la plantilla con todos los datos
        return render(request, 'main/index.html', {
            'funerarias': funerarias,
            'cementerios': cementerios,
            'mascotas': mascotas,
            'homenajes': homenajes,
            'form': form if request.user.is_authenticated else None,
            'funeraria_content_type': funeraria_content_type,
            'cementerio_content_type': cementerio_content_type,
            'mascota_content_type': mascota_content_type,
        })

    except Exception as e:
        print(f"Error en la vista homepage: {e}")
        return render(request, 'main/error.html', {'error': str(e)})


# def homepage(request):
#     try:
#         # Verificar si el usuario está autenticado
#         if request.user.is_authenticated:
#             # Obtener homenajes creados e invitados para usuarios autenticados
#             homenajes_creados = Homenaje.objects.filter(autor=request.user).order_by('-fecha_publicacion')
#             homenajes_invitados = Homenaje.objects.filter(invitados=request.user).order_by('-fecha_publicacion')
#             # Combinar ambos conjuntos
#             homenajes = homenajes_creados | homenajes_invitados
#         else:
#             # Para usuarios no autenticados, no intentamos filtrar por `request.user`
#             homenajes = Homenaje.objects.none()  # Ningún homenaje será mostrado

#         # Obtener todas las funerarias, cementerios y servicios de mascotas
#         funerarias = Funeraria.objects.all()
#         cementerios = Cementerio.objects.all()
#         mascotas = ServiciosMascotas.objects.all()

#         # Convertir imágenes de funerarias a Base64
#         for funeraria in funerarias:
#             if funeraria.imagen:
#                 funeraria.imagen_base64 = base64.b64encode(funeraria.imagen).decode('utf-8')

#         # Convertir imágenes de cementerios a Base64
#         for cementerio in cementerios:
#             if cementerio.imagen:
#                 cementerio.imagen_base64 = base64.b64encode(cementerio.imagen).decode('utf-8')

#         # Convertir imágenes de servicios para mascotas a Base64
#         for mascota in mascotas:
#             if mascota.imagen:
#                 mascota.imagen_base64 = base64.b64encode(mascota.imagen).decode('utf-8')

#         # Procesar el formulario de homenaje
#         if request.method == 'POST' and request.user.is_authenticated:
#             form = HomenajeForm(request.POST, request.FILES)
#             if form.is_valid():
#                 form.save()
#                 return redirect('homepage')  # Redirigir tras guardar
#         else:
#             form = HomenajeForm()

#         # Renderizar la plantilla con todos los datos
#         return render(request, 'main/index.html', {
#             'funerarias': funerarias,
#             'cementerios': cementerios,
#             'mascotas': mascotas,
#             'homenajes': homenajes,
#             'form': form if request.user.is_authenticated else None
#         })

#     except Exception as e:
#         print(f"Error en la vista homepage: {e}")
#         return render(request, 'main/error.html', {'error': str(e)})



# Vista de registro
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige a la página de inicio de sesión
    else:
        form = RegistroForm()
    return render(request, 'main/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"Usuario: {username}, Contraseña: {password}")  # Imprimir para verificar
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')  # Redirige a la página principal después de iniciar sesión
            else:
                print("Autenticación fallida")
        else:
            print(form.errors)
            print("Formulario no válido")
        return render(request, 'main/login.html', {'form': form, 'error': 'Credenciales inválidas.'})
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})



@login_required
def crear_homenaje(request):
    if request.method == 'POST':
        form = HomenajeForm(request.POST, request.FILES)
        if form.is_valid():
            homenaje = form.save(commit=False)
            homenaje.autor = request.user  # Asociar el autor al usuario autenticado
            homenaje.save()
            form.save_m2m()  # Guardar los muchos-a-muchos
            # Redirigir a una página donde se muestre el enlace único
            return redirect('homenaje_compartido', slug=homenaje.slug)
    else:
        form = HomenajeForm()
    return render(request, 'main/crear_homenaje.html', {'form': form})

@login_required
def ver_homenaje(request, slug):
    homenaje = get_object_or_404(Homenaje, slug=slug)

    # Verificar permisos para acceder al homenaje
    if request.user != homenaje.autor and request.user not in homenaje.invitados.all():
        return HttpResponseForbidden("No tienes permiso para acceder a este homenaje.")

    form = CondolenciaForm()

    if request.method == 'POST':
        # Manejo de reacciones (vela y paloma)
        if 'vela' in request.POST:
            homenaje.velas += 1
            homenaje.save()
        elif 'paloma' in request.POST:
            homenaje.palomas += 1
            homenaje.save()
        # Manejo de creación de condolencia
        elif 'condolencia' in request.POST:
            form = CondolenciaForm(request.POST, request.FILES)
            if form.is_valid():
                condolencia = form.save(commit=False)
                condolencia.homenaje = homenaje
                condolencia.autor = request.user

                # Asignar archivos de video si están disponibles en request.FILES
                if 'video_subido' in request.FILES:
                    condolencia.video_subido = request.FILES['video_subido']
                if 'video_capturado' in request.FILES:
                    condolencia.video_capturado = request.FILES['video_capturado']

                condolencia.save()
                # Redirigir para evitar reenvío del formulario al recargar
                return redirect('ver_homenaje', slug=slug)

    # Obtener todas las condolencias asociadas al homenaje
    condolencias = homenaje.condolencias.all()

    return render(request, 'main/ver_homenaje.html', {
        'homenaje': homenaje,
        'form': form,
        'condolencias': condolencias
    })

# @login_required
# def ver_homenaje(request, slug):
#     homenaje = get_object_or_404(Homenaje, slug=slug)

#     # Verificar permisos
#     if request.user != homenaje.autor and request.user not in homenaje.invitados.all():
#         return HttpResponseForbidden("No tienes permiso para acceder a este homenaje.")

#     form = CondolenciaForm()

#     if request.method == 'POST':
#         print(f"Datos del POST: {request.POST}")

#         # Manejo de reacciones
#         if 'vela' in request.POST:
#             homenaje.velas += 1
#             homenaje.save()
#         elif 'paloma' in request.POST:
#             homenaje.palomas += 1
#             homenaje.save()
        
#         # Manejo de condolencias
#         elif 'condolencia' in request.POST:
#             form = CondolenciaForm(request.POST, request.FILES)
#             if form.is_valid():
#                 condolencia = form.save(commit=False)
#                 condolencia.homenaje = homenaje
#                 condolencia.autor = request.user

#                 # Asigna el video capturado automáticamente si está en los archivos
#                 if 'video_capturado' in request.FILES:
#                     condolencia.video_capturado = request.FILES['video_capturado']
#                 if 'video_subido' in request.FILES:
#                     condolencia.video_subido = request.FILES['video_subido']

#                 condolencia.save()
#                 print(f"Condolencia guardada: {condolencia}")

#                 return redirect(homenaje.get_absolute_url())
#             else:
#                 print(f"Errores del formulario: {form.errors}")

#     # Obtener todas las condolencias asociadas al homenaje para pasarlas al contexto
#     condolencias = homenaje.condolencias.all()

#     return render(request, 'main/ver_homenaje.html', {
#         'homenaje': homenaje,
#         'form': form,
#         'condolencias': condolencias  # Aseguramos de pasar las condolencias al contexto
#     })
# Vista para mostrar el enlace que el creador puede compartir
@login_required
def homenaje_compartido(request, slug):
    # Obtener el homenaje correspondiente al slug
    homenaje = get_object_or_404(Homenaje, slug=slug)

    # Verificar si el usuario está invitado o es el autor del homenaje
    if request.user not in homenaje.invitados.all() and request.user != homenaje.autor:
        return HttpResponseForbidden("No tienes permiso para acceder a esta invitación.")

    # Mostrar la invitación con un botón para acceder al homenaje completo
    return render(request, 'main/homenaje_compartido.html', {'homenaje': homenaje})



    
@login_required
def historial_homenajes(request):
    # Obtener todos los homenajes creados por el usuario autenticado
    homenajes = Homenaje.objects.filter(autor=request.user)
    
    return render(request, 'main/historial_homenajes.html', {'homenajes': homenajes})

# Instancia de Nominatim
geolocator = Nominatim(user_agent="funeraria_locator")    
    
@csrf_exempt
def ask(request):
    if request.method == 'POST':
        user_message = json.loads(request.body).get('message')

        # Crear un prompt que incluya contexto
        prompt = (
            f"Eres un asistente virtual para la página web AsaPeace. "
            f"Das respuestas cortas. Solo debes responder preguntas relacionadas con "
            f"los servicios funerarios para humanos y mascotas. Siempre mantén un tono "
            f"amable y comprensivo respecto al fallecimiento de un ser querido. Recuerda "
            f"que AsaPeace actúa como un comunicador entre los usuarios y las funerarias, "
            f"pero no realiza pagos directos. Además, ayudas a orientar con los temas "
            f"legales de Chile. Por favor, proporciona respuestas breves y concisas. "
            f"El usuario pregunta: {user_message} "
        )

        # Si el mensaje del usuario pregunta por la ubicación
        if "ubicación" in user_message.lower() or "sabes mi ubicación" in user_message.lower():
            bot_message = "Lo siento, como asistente virtual no tengo acceso a tu ubicación. Por favor, comparte tu ubicación para ayudarte mejor."
        else:
            # Llamada a la API de OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=250
            )
            bot_message = response['choices'][0]['message']['content'].strip()

        return JsonResponse({'message': bot_message})

    return JsonResponse({'error': 'Invalid request'}, status=400)
@csrf_exempt
def encontrar_funeraria_cercana(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            latitud_usuario = data.get('latitud')
            longitud_usuario = data.get('longitud')

            if latitud_usuario is None or longitud_usuario is None:
                return JsonResponse({'error': 'Latitud y longitud del usuario son requeridas.'}, status=400)

            # Lógica para encontrar la funeraria más cercana
            funerarias = Funeraria.objects.all()
            funeraria_cercana = None
            distancia_minima = float('inf')

            for funeraria in funerarias:
                if funeraria.direccion:
                    # Geocodificar la dirección de la funeraria
                    location = geolocator.geocode(funeraria.direccion)
                    if location:
                        latitud_funeraria = location.latitude
                        longitud_funeraria = location.longitude

                        # Calcular la distancia
                        distancia = great_circle(
                            (latitud_usuario, longitud_usuario),
                            (latitud_funeraria, longitud_funeraria)
                        ).kilometers

                        if distancia < distancia_minima:
                            distancia_minima = distancia
                            funeraria_cercana = funeraria

            if funeraria_cercana:
                return JsonResponse({
                    'nombre': funeraria_cercana.nombre,
                    'direccion': funeraria_cercana.direccion,
                    'telefono': funeraria_cercana.telefono,
                    'email': funeraria_cercana.email,
                    'distancia': distancia_minima
                })
            else:
                return JsonResponse({'error': 'No se encontraron funerarias cercanas.'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos de solicitud no válidos.'}, status=400)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)


# implementación calculadora
# def calcular_cotizacion(tipo_servicio, ubicacion, servicios_adicionales, beneficio):
#     total = tipo_servicio.precio_base * ubicacion.factor_precio
#     for servicio in servicios_adicionales:
#         total += servicio.precio
#     if beneficio:
#         total -= beneficio.monto
#     return max(total, 0)  # Asegurar que el total no sea negativo

def cotizacion_view(request):
    total = None

    if request.method == 'POST':
        print(f"Datos POST: {request.POST}")  # Verifica los datos enviados
        form = CotizacionForm(request.POST)

        if form.is_valid():
            tipo_servicio = form.cleaned_data['tipo_servicio']
            ubicacion = form.cleaned_data['ubicacion']
            servicios_adicionales = form.cleaned_data['servicios_adicionales']
            beneficio = form.cleaned_data.get('beneficio')

            print(f"Servicio: {tipo_servicio}, Ubicación: {ubicacion}, Servicios adicionales: {servicios_adicionales}, Beneficio: {beneficio}")

            # Calcular el total de la cotización
            total = tipo_servicio.precio_base * ubicacion.factor_precio
            for servicio in servicios_adicionales:
                total += servicio.precio
            if beneficio:
                total -= beneficio.monto

            total = max(total, 0)  # Asegurar que el total no sea negativo
        else:
            print(f"Errores del formulario: {form.errors}")  # Depurar errores
    else:
        form = CotizacionForm()

    # Depuración para verificar que el formulario se está cargando correctamente
    print(f"Formulario inicial: {form}")

    return render(request, 'main/cotizacion.html', {'form': form, 'total': total})



#Mascotas
def mascotas(request):
    mascotas = Mascota.objects.all()[:4]
    return render(request, 'main/mascotas.html', {'mascotas': mascotas})  # Asegúrate de que la ruta sea correcta



def agregar_mascota(request):
    if request.method == 'POST':
        # Crear una instancia del formulario con los datos enviados
        form = MascotaForm(request.POST, request.FILES)  
        if form.is_valid():  # Validar el formulario
            form.save()  # Guardar la instancia en la base de datos
            messages.success(request, '¡Mascota agregada exitosamente!')  # Mensaje de éxito
            return redirect('listar_mascotas')  # Redirigir a la lista de mascotas
        else:
            # Si el formulario no es válido, mostrar un mensaje de error
            messages.error(request, 'Error al agregar la mascota. Por favor, verifica los datos ingresados.')
    else:
        form = MascotaForm()  # Crear un formulario vacío para la solicitud GET

    return render(request, 'main/agregar_mascota.html', {'form': form})  # Pasar el formulario al contexto

def lista_mascotas(request):
    # Obtener todas las mascotas de la base de datos
    mascotas = Mascota.objects.all()
    return render(request, 'main/lista_mascotas.html', {'mascotas': mascotas})



#calificaciones
from django.contrib.contenttypes.models import ContentType

@login_required
def agregar_calificacion(request, content_type_id, object_id):
    # Obtener el ContentType para el modelo
    content_type = get_object_or_404(ContentType, id=content_type_id)
    modelo = content_type.model_class()
    
    # Buscar el objeto correcto, dependiendo del modelo
    try:
        if content_type.model == 'funeraria':
            objeto = modelo.objects.get(id_funeraria=object_id)
        elif content_type.model == 'cementerio':
            objeto = modelo.objects.get(id_cementerio=object_id)
        elif content_type.model == 'serviciosmascotas':
            objeto = modelo.objects.get(id_servi_mascota=object_id)
        else:
            raise FieldError("No se puede encontrar el campo adecuado para este modelo.")
    except modelo.DoesNotExist:
        return HttpResponseNotFound("El objeto solicitado no existe.")
    
    # Procesar el formulario de calificación
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.content_type = content_type
            calificacion.object_id = object_id
            calificacion.usuario = request.user
            calificacion.save()
            return redirect('homepage')
    else:
        form = CalificacionForm()
    
    # Renderizar la página de calificación con el formulario
    return render(request, 'main/agregar_calificacion.html', {'form': form, 'modelo': objeto})