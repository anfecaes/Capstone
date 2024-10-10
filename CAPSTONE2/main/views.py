from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import json
from .models import Funeraria  # Asegúrate de tener un modelo para las funerarias
from geopy.distance import great_circle
from xhtml2pdf import pisa  # Importa xhtml2pdf para generar PDFs

# Asegúrate de que tu clave API de OpenAI esté configurada correctamente
openai.api_key = 'sk-O9sWoqxgcMdmfAkNGaxsUkHuQUbjoXyrU4vg0xjfFrT3BlbkFJj8hcIwvbjq_G_hPL71QtQDXkjqeFBWA9C1f237-YQA'

def homepage(request):
    return render(request, 'main/index.html')

def mascotas(request):
    return render(request, 'main/mascotas.html')  # Asegúrate de que la ruta sea correcta

@csrf_exempt
def ask(request):
    if request.method == 'POST':
        user_message = json.loads(request.body).get('message').strip()

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

        # Comprobar si el usuario cancela el proceso
        if user_message.lower() == "cancelar":
            request.session.flush()  # Limpiar la sesión
            bot_message = "Has cancelado el proceso de generación del PDF. ¿En qué más puedo ayudarte?"
            return JsonResponse({'message': bot_message})

        # Comprobar si el usuario quiere volver a la pregunta anterior
        if user_message.lower() == "volver":
            step = request.session.get('step')
            if step == 'notas':
                request.session['step'] = 'ubicacion'
                bot_message = "Por favor, ¿cuál es la ubicación? "
            elif step == 'ubicacion':
                request.session['step'] = 'fecha_servicio'
                bot_message = "¿Cuál es la fecha del servicio? "
            elif step == 'fecha_servicio':
                request.session['step'] = 'tipo_servicio'
                bot_message = "¿Qué tipo de servicio deseas? "
            elif step == 'tipo_servicio':
                request.session['step'] = 'nombre'
                bot_message = "¿Cuál es tu nombre? "
            else:
                bot_message = "No hay preguntas anteriores para volver."
            return JsonResponse({'message': bot_message})

        # Verificar si el usuario quiere generar un PDF
        if "pdf" in user_message.lower() or "generar pdf" in user_message.lower() or "crea pdf" in user_message.lower():
            bot_message = (
                "Entiendo que necesitas un documento. Primero, permíteme hacerte algunas preguntas para recopilar la información necesaria. "
                "¿Cuál es tu nombre? "
            )
            request.session['step'] = 'nombre'
            return JsonResponse({'message': bot_message})

        # Si el chatbot está en medio del flujo de preguntas para el PDF
        step = request.session.get('step')

        if step == 'nombre':
            request.session['nombre_cliente'] = user_message
            bot_message = (
                "Gracias. ¿Qué tipo de servicio deseas? "
            )
            request.session['step'] = 'tipo_servicio'
        elif step == 'tipo_servicio':
            request.session['tipo_servicio'] = user_message
            bot_message = (
                "Perfecto. ¿Cuál es la fecha del servicio? "
            )
            request.session['step'] = 'fecha_servicio'
        elif step == 'fecha_servicio':
            request.session['fecha_servicio'] = user_message
            bot_message = (
                "¿Dónde será el servicio? (ubicación) "
            )
            request.session['step'] = 'ubicacion'
        elif step == 'ubicacion':
            request.session['ubicacion'] = user_message
            bot_message = (
                "¿Tienes alguna nota adicional que agregar? "
            )
            request.session['step'] = 'notas'
        elif step == 'notas':
            request.session['notas'] = user_message
            bot_message = "Gracias. Ahora procederé a generar el PDF. Puedes descargarlo <a href='/generar_pdf/' download>Descargar PDF</a>."
            request.session['step'] = 'finalizado'
        else:
            # Llamada a la API de OpenAI para respuesta normal
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_message}],
                max_tokens=150
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

# Nueva vista para generar el PDF
@csrf_exempt
def generar_pdf(request):
    if request.method == 'GET':
        # Usar los datos proporcionados por el usuario
        context = {
            'nombre_cliente': request.session.get('nombre_cliente', 'No proporcionado'),
            'tipo_servicio': request.session.get('tipo_servicio', 'No proporcionado'),
            'fecha_servicio': request.session.get('fecha_servicio', 'No proporcionado'),
            'ubicacion': request.session.get('ubicacion', 'No proporcionado'),
            'notas': request.session.get('notas', 'No proporcionado'),
        }
        
        # Renderizar el HTML
        template_path = 'main/solicitud_pdf.html'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="solicitud.pdf"'
        
        # Renderizar el template en HTML
        html = render(request, template_path, context).content.decode('utf-8')
        pisa_status = pisa.CreatePDF(html, dest=response)

        # Verificar si hubo errores al generar el PDF
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=400)

        return response

    return HttpResponse('Método no permitido.', status=405)
