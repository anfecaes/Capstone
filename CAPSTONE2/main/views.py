from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import json
from .models import Funeraria, Cementerio, ServiciosMascotas, Homenaje
import base64
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
from .forms import HomenajeForm
# Asegúrate de que tu clave API de OpenAI esté configurada correctamente
openai.api_key = 'sk-21wt4qXy2s5A0GeKO2eaAMqLGspJYEHOMkHGsN8Kq6T3BlbkFJ9-0Nq8gklx147Q_rACJzHSnZirJo0MMtugciMPmhQA'


def homepage(request):
    funerarias = Funeraria.objects.all()
    cementerios = Cementerio.objects.all()
    mascotas = ServiciosMascotas.objects.all()
    
    # Convertir las imágenes a base64 para cada funeraria
    for funeraria in funerarias:
        if funeraria.imagen:
            funeraria.imagen_base64 = base64.b64encode(funeraria.imagen).decode('utf-8')

    # Convertir las imágenes a base64 para cada cementerio
    for cementerio in cementerios:
        if cementerio.imagen:
            cementerio.imagen_base64 = base64.b64encode(cementerio.imagen).decode('utf-8')

    # Convertir las imágenes a base64 para cada servicio de mascotas
    for mascota in mascotas:
        if mascota.imagen:
            mascota.imagen_base64 = base64.b64encode(mascota.imagen).decode('utf-8')

    return render(request, 'main/index.html', {
        'funerarias': funerarias,
        'cementerios': cementerios,
        'mascotas': mascotas
    })
    
    
    
#muro de homenajes
def crear_homenaje(request):
    if request.method == 'POST':
        form = HomenajeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('homenajes_list')  # Redirigir a una página que liste los homenajes
    else:
        form = HomenajeForm()
    return render(request, 'main/crear_homenaje.html', {'form': form})
    # return render(request, 'main/index.html', {'form': form})

#boton para reaccionar a plubicación
def agregar_condolencia(request, id_homenaje):
    homenaje = Homenaje.objects.get(id=id_homenaje)
    homenaje.condolencias += 1
    homenaje.save()
    return JsonResponse({'condolencias': homenaje.condolencias})

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