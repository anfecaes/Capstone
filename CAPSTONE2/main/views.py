from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import json
from .models import Funeraria  # Asegúrate de tener un modelo para las funerarias
from geopy.distance import great_circle

# Asegúrate de que tu clave API de OpenAI esté configurada correctamente
openai.api_key = 'PONER API ACÁ'

def homepage(request):
    return render(request, 'main/index.html')  # Asegúrate de que la ruta sea correcta

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
        data = json.loads(request.body)
        latitud_usuario = data.get('latitud')
        longitud_usuario = data.get('longitud')

        # Lógica para encontrar la funeraria más cercana
        funerarias = Funeraria.objects.all()
        funeraria_cercana = None
        distancia_minima = float('inf')

        for funeraria in funerarias:
            distancia = great_circle(
                (latitud_usuario, longitud_usuario),
                (funeraria.latitud, funeraria.longitud)
            ).kilometers
            
            if distancia < distancia_minima:
                distancia_minima = distancia
                funeraria_cercana = funeraria

        if funeraria_cercana:
            return JsonResponse({
                'nombre': funeraria_cercana.nombre,
                'direccion': funeraria_cercana.direccion,
                'latitud': funeraria_cercana.latitud,
                'longitud': funeraria_cercana.longitud,
            })
        else:
            return JsonResponse({'error': 'No se encontraron funerarias cercanas.'}, status=404)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)
