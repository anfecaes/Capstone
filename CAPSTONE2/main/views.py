from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import json
from .models import Funeraria  # Asegúrate de tener un modelo para las funerarias
from geopy.distance import great_circle
from xhtml2pdf import pisa  # Importa xhtml2pdf para generar PDFs
import requests
from .models import Mascota
from .forms import MascotaForm  # Asegúrate de importar tu formulario
from django.contrib import messages  # Para mostrar mensajes de éxito

# Asegúrate de que tu clave API de OpenAI esté configurada correctamente
openai.api_key = 'sk-BSh4SZ8ofi0WdABDJae1leDsVuXCLHEal91v7OtznrT3BlbkFJe_tu6WtWprhwE96WIinS9J53EzSokUiCI9Fw06zncA'

def homepage(request):
    return render(request, 'main/index.html')

def mascotas(request):
    mascotas = Mascota.objects.all()[:4]
    return render(request, 'main/mascotas.html', {'mascotas': mascotas})  # Asegúrate de que la ruta sea correcta

def lista_mascotas(request):
    # Obtener todas las mascotas de la base de datos
    mascotas = Mascota.objects.all()
    return render(request, 'main/lista_mascotas.html', {'mascotas': mascotas})

def agregar_mascota(request):
    if request.method == 'POST':
        # Crear una instancia del formulario con los datos enviados
        form = MascotaForm(request.POST, request.FILES)  
        if form.is_valid():  # Validar el formulario
            form.save()  # Guardar la instancia en la base de datos
            messages.success(request, '¡Mascota agregada exitosamente!')  # Mensaje de éxito
            return redirect('lista_mascotas')  # Redirigir a la lista de mascotas
        else:
            # Si el formulario no es válido, mostrar un mensaje de error
            messages.error(request, 'Error al agregar la mascota. Por favor, verifica los datos ingresados.')
    else:
        form = MascotaForm()  # Crear un formulario vacío para la solicitud GET

    return render(request, 'main/agregar_mascota.html', {'form': form})  # Pasar el formulario al contexto

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
            previous_steps = {
                'notas': 'opcion_cremacion_sepultura',
                'opcion_cremacion_sepultura': 'donacion',
                'donacion': 'certificado_defuncion',
                'certificado_defuncion': 'ubicacion',
                'ubicacion': 'fecha_servicio',
                'fecha_servicio': 'tipo_servicio',
                'tipo_servicio': 'nombre',
            }

            if step in previous_steps:
                request.session['step'] = previous_steps[step]
                step = request.session['step']

                if step == 'nombre':
                    bot_message = "¿Cuál es tu nombre?"
                elif step == 'tipo_servicio':
                    bot_message = "¿Qué tipo de servicio deseas?"
                elif step == 'fecha_servicio':
                    bot_message = "¿Cuál es la fecha del servicio?"
                elif step == 'ubicacion':
                    bot_message = "¿Dónde será el servicio? (ubicación)"
                elif step == 'certificado_defuncion':
                    bot_message = (
                        "¿Ya tiene el certificado de defunción entregado por el médico de defunción para el fallecido? "
                        "¿Ya inscribió el certificado de defunción en el Registro Civil? Responde 'sí' o 'no'."
                    )
                elif step == 'donacion':
                    bot_message = (
                        "Según la Ley N° 19.451, las personas mayores de 18 años son donantes automáticos. "
                        "¿Estás de acuerdo con esto? Responde 'sí' o 'no'."
                    )
                elif step == 'opcion_cremacion_sepultura':
                    bot_message = "¿Deseas optar por cremación o sepultura?"
                elif step == 'notas':
                    bot_message = "¿Tienes alguna nota adicional que agregar?"
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
            bot_message = "Gracias. ¿Qué tipo de servicio deseas? "
            request.session['step'] = 'tipo_servicio'
        elif step == 'tipo_servicio':
            request.session['tipo_servicio'] = user_message
            bot_message = "Perfecto. ¿Cuál es la fecha del servicio? "
            request.session['step'] = 'fecha_servicio'
        elif step == 'fecha_servicio':
            request.session['fecha_servicio'] = user_message
            bot_message = "¿Dónde será el servicio? (ubicación) "
            request.session['step'] = 'ubicacion'
        elif step == 'ubicacion':
            request.session['ubicacion'] = user_message
            bot_message = (
                "¿Ya tiene el certificado de defunción entregado por el médico de defunción para el fallecido? "
                "¿Ya inscribió el certificado de defunción en el Registro Civil? Responde 'sí' o 'no'."
            )
            request.session['step'] = 'certificado_defuncion'
        elif step == 'certificado_defuncion':
            if user_message.lower() == "no":
                bot_message = (
                    "Debes de llevar este documento impreso a la oficina del Registro Civil. "
                    "Es importante que lo hagas. Puedes ir a la sección de defunción en el siguiente enlace: "
                    "<a href='https://www.registrocivil.cl/' target='_blank'>Registro Civil</a> para obtener tu certificado."
                )
                request.session['step'] = 'finalizado'
            else:
                bot_message = (
                    "Ten en cuenta que las deudas de una persona fallecida pueden pasar a sus herederos legales. "
                    "Para evitarlo, puedes renunciar a la herencia o aceptarla con 'beneficio de inventario', "
                    "lo que limita tu responsabilidad a los bienes heredados. En algunos casos, las deudas pueden estar "
                    "cubiertas por un seguro de desgravamen, que cancela el saldo en caso de fallecimiento del titular. "
                    "Por favor, escribe 'ok' o 'continuar' para seguir con la siguiente pregunta."
                )
                request.session['step'] = 'esperando_confirmacion_deudas'  # Cambiamos el paso
        elif step == 'esperando_confirmacion_deudas':
            if user_message.lower() in ["ok", "continuar"]:
                bot_message = (
                    "Según la Ley N° 19.451, las personas mayores de 18 años son donantes automáticos. "
                    "¿Estás de acuerdo con esto? Responde 'sí' o 'no'."
                )
                request.session['step'] = 'donacion'
            else:
                bot_message = "Por favor, escribe 'ok' o 'continuar' para seguir."
        elif step == 'donacion':
            affirmative_responses = ["sí", "si", "sí", "sì", "ye", "yes", "yup", "por supuesto", "claro"]
            if any(resp in user_message.lower() for resp in affirmative_responses):
                bot_message = "Gracias por tu respuesta. ¿Deseas optar por cremación o sepultura? "
                request.session['step'] = 'opcion_cremacion_sepultura'
            elif user_message.lower() == 'no':
                bot_message = (
                    "De acuerdo con la Ley N° 19.451, las personas mayores de 18 años "
                    "son donantes automáticos. Sin embargo, si no estás de acuerdo, "
                    "debes informarlo en el Registro Nacional de No Donantes, o asegurarte de "
                    "que tu familiar haya dejado un testamento o expresión clara de su deseo de no donar. "
                    "¿Deseas optar por cremación o sepultura?"
                )
                request.session['step'] = 'opcion_cremacion_sepultura'
            else:
                bot_message = "Lo siento, no entendí tu respuesta. Por favor responde con 'sí' o 'no'."
        elif step == 'opcion_cremacion_sepultura':
            cremation_responses = ["cremación", "crema", "cremar", "incineración", "cremacion"]
            burial_responses = ["sepultura", "tumba", "entierro", "inhumación", "inhumacion"]

            if any(resp in user_message.lower() for resp in burial_responses):
                bot_message = (
                    "Okey, si no tienes dinero para la sepultura, puedes solicitar una entrevista con el asistente social de la municipalidad "
                    "para evaluar si puedes optar a una sepultura gratuita. "
                    "¿Tienes alguna nota adicional que agregar?"
                )
                request.session['step'] = 'notas'
            elif any(resp in user_message.lower() for resp in cremation_responses):
                bot_message = (
                    "Para la cremación, necesitas: "
                    "1. Autorización previa del Director General del Servicio Nacional de Salud o su delegado. "
                    "2. Existencia de una declaración escrita hecha previamente por el difunto en una Notaría o una solicitud del cónyuge sobreviviente o de la mayoría de los hijos que autoricen la cremación ante notario. "
                    "¿Tienes alguna nota adicional que agregar?"
                )
                request.session['step'] = 'notas'
            else:
                bot_message = "Lo siento, no entendí tu respuesta. Por favor responde con 'cremación' o 'sepultura'."
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
