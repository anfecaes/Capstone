from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import json
from .models import Funeraria, Cementerio, ServiciosMascotas, Homenaje
import base64
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
# homenajes
# from django.core.mail import send_mail
# from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
#importaciones para loguear
from .forms import HomenajeForm, RegistroForm, CondolenciaForm, CotizacionForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


# Asegúrate de que tu clave API de OpenAI esté configurada correctamente
openai.api_key = 'sk-BSh4SZ8ofi0WdABDJae1leDsVuXCLHEal91v7OtznrT3BlbkFJe_tu6WtWprhwE96WIinS9J53EzSokUiCI9Fw06zncA'


@login_required
def homepage(request):
    try:
        # Obtener homenajes creados e invitados
        homenajes_creados = Homenaje.objects.filter(autor=request.user).order_by('-fecha_publicacion')
        homenajes_invitados = Homenaje.objects.filter(invitados=request.user).order_by('-fecha_publicacion')

        # Combinar ambos conjuntos
        homenajes = homenajes_creados | homenajes_invitados

        print(f"Homenajes encontrados: {homenajes}")

        # Obtener todas las funerarias, cementerios y servicios de mascotas
        funerarias = Funeraria.objects.all()
        cementerios = Cementerio.objects.all()
        mascotas = ServiciosMascotas.objects.all()

        # Convertir imágenes de funerarias a Base64
        for funeraria in funerarias:
            if funeraria.imagen:
                funeraria.imagen_base64 = base64.b64encode(funeraria.imagen).decode('utf-8')

        # Convertir imágenes de cementerios a Base64
        for cementerio in cementerios:
            if cementerio.imagen:
                cementerio.imagen_base64 = base64.b64encode(cementerio.imagen).decode('utf-8')

        # Convertir imágenes de servicios para mascotas a Base64
        for mascota in mascotas:
            if mascota.imagen:
                mascota.imagen_base64 = base64.b64encode(mascota.imagen).decode('utf-8')

        # Procesar el formulario de homenaje
        if request.method == 'POST':
            form = HomenajeForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('homepage')  # Redirigir tras guardar
        else:
            form = HomenajeForm()

        # Renderizar la plantilla con todos los datos
        return render(request, 'main/index.html', {
            'funerarias': funerarias,
            'cementerios': cementerios,
            'mascotas': mascotas,
            'homenajes': homenajes,
            'form': form
        })

    except Exception as e:
        print(f"Error en la vista homepage: {e}")
        return render(request, 'main/error.html', {'error': str(e)})

# def homepage(request):
#     funerarias = Funeraria.objects.all()
#     cementerios = Cementerio.objects.all()
#     mascotas = ServiciosMascotas.objects.all()

#     # Obtener los homenajes creados por el usuario autenticado
#     homenajes = Homenaje.objects.filter(autor=request.user).order_by('-fecha_publicacion')

#     # Convertir las imágenes a base64 para cada funeraria
#     for funeraria in funerarias:
#         if funeraria.imagen:
#             funeraria.imagen_base64 = base64.b64encode(funeraria.imagen).decode('utf-8')

#     # Convertir las imágenes a base64 para cada cementerio
#     for cementerio in cementerios:
#         if cementerio.imagen:
#             cementerio.imagen_base64 = base64.b64encode(cementerio.imagen).decode('utf-8')

#     # Convertir las imágenes a base64 para cada servicio de mascotas
#     for mascota in mascotas:
#         if mascota.imagen:
#             mascota.imagen_base64 = base64.b64encode(mascota.imagen).decode('utf-8')

#     # Procesar el formulario de homenaje si es necesario (en este caso, es solo ilustrativo)
#     if request.method == 'POST':
#         form = HomenajeForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('homepage')  # Redirigir a la misma página tras crear el homenaje
#     else:
#         form = HomenajeForm()

#     # Renderizar la plantilla con los datos procesados
#     return render(request, 'main/index.html', {
#         'funerarias': funerarias,
#         'cementerios': cementerios,
#         'mascotas': mascotas,
#         'homenajes': homenajes,  # Incluir los homenajes del usuario en el contexto
#         'form': form
#     })


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
    # Obtener el homenaje correspondiente al slug
    homenaje = get_object_or_404(Homenaje, slug=slug)

    # Verificar permisos
    if request.user != homenaje.autor and request.user not in homenaje.invitados.all():
        return HttpResponseForbidden("No tienes permiso para acceder a este homenaje.")

    # Inicializar el formulario de condolencias vacío
    form = CondolenciaForm()

    if request.method == 'POST':
        print(f"Datos del POST: {request.POST}")  # Depurar el contenido del POST

        if 'vela' in request.POST:
            homenaje.velas += 1
            homenaje.save()
        elif 'paloma' in request.POST:
            homenaje.palomas += 1
            homenaje.save()
        elif 'condolencia' in request.POST:
            form = CondolenciaForm(request.POST)
            if form.is_valid():
                condolencia = form.save(commit=False)
                condolencia.homenaje = homenaje  # Relacionar la condolencia con el homenaje
                condolencia.autor = request.user  # Asociar al usuario actual como autor
                condolencia.save()
                print(f"Condolencia guardada: {condolencia}")

                return redirect(homenaje.get_absolute_url())  # Redirigir tras guardar
            else:
                print(f"Errores del formulario: {form.errors}")

    # Renderizar la plantilla con el formulario vacío
    return render(
        request,
        'main/ver_homenaje.html',
        {'homenaje': homenaje, 'form': form}
    )




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
    total = None  # Inicializar el total como None

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

    return render(request, 'main/cotizacion.html', {'form': form, 'total': total})