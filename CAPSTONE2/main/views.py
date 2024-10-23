from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import json
from .models import Funeraria  # Asegúrate de tener un modelo para las funerarias
from .models import OrdenPago  # Asegúrate de que esta línea esté presente
from geopy.distance import great_circle
from xhtml2pdf import pisa  # Importa xhtml2pdf para generar PDFs
import requests
from .models import Mascota
from .forms import MascotaForm  # Asegúrate de importar tu formulario
from django.contrib import messages  # Para mostrar mensajes de éxito
import hashlib
import time
from django.conf import settings

# Asegúrate de que tu clave API de OpenAI esté configurada correctamente
openai.api_key = 'Poner Api aqui'

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

# FLOW Webpay
def callback_pago(request):
    numero_orden = request.POST.get('commerceOrder')
    estado_pago = request.POST.get('status')

    try:
        orden_pago = OrdenPago.objects.get(numero_orden=numero_orden)
        orden_pago.estado = estado_pago
        
        if estado_pago == 'ERROR':  # Si el estado es de error, registrar el error
            orden_pago.error = request.POST.get('errorMessage', 'Error desconocido')
        
        orden_pago.save()

        # Renderizar el HTML de callback después de actualizar el estado
        return render(request, 'main/callback.html', {'numero_orden': numero_orden, 'estado_pago': estado_pago})
    except OrdenPago.DoesNotExist:
        return render(request, 'main/error.html', {'message': 'Orden no encontrada'}, status=404)

def pago_completado(request):
    return render(request, 'main/gracias.html', {'mensaje': 'Gracias por tu compra de prueba!'})

def crear_pago_prueba(request):
    print("Función crear_pago_prueba llamada.")  # Línea de depuración
    numero_orden = f'ORD-{int(time.time())}'
    monto = 10000  # Monto en pesos chilenos

    # Parámetros para la orden de pago
    params = {
        'apiKey': 'ak_test_1234567890',  # API Key de prueba
        'commerceOrder': numero_orden,
        'subject': 'Producto de prueba',
        'currency': 'CLP',
        'amount': monto,  # Monto en pesos chilenos
        'email': '23plutopro@gmail.com',  # Cambia a un correo válido
        'urlConfirmation': request.build_absolute_uri('/callback/'),
        'urlReturn': request.build_absolute_uri('/gracias/'),
        'buyOrder': numero_orden,  # Agregado para referencia del pedido
        'sessionId': 'session-123456'  # Agregado para referencia de sesión
    }

    # Generar la firma (hash) con los parámetros y la secret key
    params['s'] = create_signature(params, 'sk_test_0987654321')

    print("Parámetros enviados a Flow:", params)  # Línea de depuración

    # Enviar solicitud POST al endpoint de pruebas de Flow
    response = requests.post('https://sandbox.flow.cl/api/payment/create', data=params)

    if response.status_code == 200:
        pago_data = response.json()
        # Guardar la orden en la base de datos antes de redirigir
        OrdenPago.objects.create(numero_orden=numero_orden, monto=monto)
        # Redirigir al usuario a la página de pago de Flow
        return redirect(pago_data['url'])
    else:
        print("Error al generar el pago de prueba:", response.status_code, response.text)  # Línea de depuración
        return render(request, 'main/error.html', {'message': 'Error al generar el pago de prueba.'})

def create_signature(params, secret_key):
    # Ordenar los parámetros y generar el hash SHA256
    sorted_params = ''.join([str(params[key]) for key in sorted(params.keys())])
    return hashlib.sha256((sorted_params + secret_key).encode('utf-8')).hexdigest()

def error_pago(request):
    return render(request, 'main/error.html', {'message': 'Ha ocurrido un error en el procesamiento del pago.'})
    

# Bot ChatGPT ASAPeace
@csrf_exempt
def ask(request):
    if request.method == 'POST':
        user_message = json.loads(request.body).get('message').strip().lower()

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
        if user_message == "cancelar":
            request.session.flush()  # Limpiar la sesión
            bot_message = "Has cancelado el proceso de generación del PDF. ¿En qué más puedo ayudarte?"
            return JsonResponse({'message': bot_message})

        # Comprobar si el usuario quiere volver a la pregunta anterior
        if user_message == "volver":
            step = request.session.get('step')
            previous_steps = {
                'notas': 'opcion_cremacion_sepultura',
                'opcion_cremacion_sepultura': 'donacion',
                'donacion': 'certificado_defuncion',
                'certificado_defuncion': 'rut',
                'rut': 'nombre',
            }

            if step in previous_steps:
                request.session['step'] = previous_steps[step]
                step = request.session['step']

                if step == 'nombre':
                    bot_message = "¿Cuál es tu nombre?"
                elif step == 'rut':
                    bot_message = "Por favor, proporciona tu RUT."
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
        if "pdf" in user_message or "generar pdf" in user_message or "crea pdf" in user_message:
            bot_message = (
                "Entiendo que necesitas un documento. Primero, permíteme hacerte algunas preguntas para recopilar la información necesaria. "
                "¿Cuál es tu nombre? "
            )
            request.session['step'] = 'nombre'
            return JsonResponse({'message': bot_message})

        # Si el chatbot está en medio del flujo de preguntas para el PDF
        step = request.session.get('step')

        if step == 'nombre':
            request.session['nombre_cliente'] = user_message.upper()
            bot_message = "Gracias. Por favor, proporciona tu RUT."
            request.session['step'] = 'rut'
        elif step == 'rut':
            request.session['rut_cliente'] = user_message.upper()
            bot_message = (
                "¿Ya tiene el certificado de defunción entregado por el médico de defunción para el fallecido? "
                "¿Ya inscribió el certificado de defunción en el Registro Civil? Responde 'sí' o 'no'."
            )
            request.session['step'] = 'certificado_defuncion'
        elif step == 'certificado_defuncion':
            # Aceptar varias formas de escribir "sí" y "no"
            affirmative_responses = ["sí", "si", "sí", "sì", "ye", "yes", "yup", "por supuesto", "claro"]
            if any(resp in user_message for resp in affirmative_responses):
                request.session['certificado_defuncion'] = "Sí"
                bot_message = (
                    "Ten en cuenta que las deudas de una persona fallecida pueden pasar a sus herederos legales. "
                    "Para evitarlo, puedes renunciar a la herencia o aceptarla con 'beneficio de inventario', "
                    "lo que limita tu responsabilidad a los bienes heredados. En algunos casos, las deudas pueden estar "
                    "cubiertas por un seguro de desgravamen, que cancela el saldo en caso de fallecimiento del titular. "
                    "Por favor, escribe 'ok' o 'continuar' para seguir con la siguiente pregunta."
                )
                request.session['step'] = 'esperando_confirmacion_deudas'
            elif user_message == 'no':
                request.session['certificado_defuncion'] = "No"
                bot_message = (
                    "Debes de llevar este documento impreso a la oficina del Registro Civil. "
                    "Es importante que lo hagas. Puedes ir a la sección de defunción en el siguiente enlace: "
                    "<a href='https://www.registrocivil.cl/' target='_blank'>Registro Civil</a> para obtener tu certificado."
                )
                request.session['step'] = 'finalizado'
            else:
                bot_message = "Por favor, responde únicamente con 'sí' o 'no'."
        elif step == 'esperando_confirmacion_deudas':
            if user_message in ["ok", "continuar"]:
                bot_message = (
                    "Según la Ley N° 19.451, las personas mayores de 18 años son donantes automáticos. "
                    "¿Estás de acuerdo con esto? Responde 'sí' o 'no'."
                )
                request.session['step'] = 'donacion'
            else:
                bot_message = "Por favor, escribe 'ok' o 'continuar' para seguir."
        elif step == 'donacion':
            affirmative_responses = ["sí", "si", "sí", "sì", "ye", "yes", "yup", "por supuesto", "claro"]
            if any(resp in user_message for resp in affirmative_responses):
                request.session['donacion'] = ("La persona fallecida ha sido considerada donante de órganos, según la Ley N° 19.451."
                                                " Esto significa que, en el momento de su fallecimiento, sus órganos pueden ser donados"
                                                " a pacientes que los necesiten, salvo que haya manifestado su negativa en vida."
                                                " Para proceder:"
                                                " * Consulta a la Familia: Si hay dudas sobre la voluntad del fallecido, se debe consultar"
                                                " a los familiares cercanos (cónyuge, hijos, etc.) para confirmar si existió una manifestación de voluntad."
                                                " * Autorización de Extracción: La extracción de órganos debe realizarse conforme a las"
                                                " normativas legales y éticas, asegurando el respeto por el fallecido."
                                                )
                bot_message = "Gracias por tu respuesta. ¿Deseas optar por cremación o sepultura?"
                request.session['step'] = 'opcion_cremacion_sepultura'
            elif user_message == 'no':
                request.session['donacion'] = ("La persona fallecida ha expresado su deseo de no ser donante de órganos. Para asegurar que esta voluntad sea respetada, se recomienda:"
                                                " Registro Nacional de No Donantes: Es importante que esta decisión se comunique al Registro Nacional de No Donantes, para que se tome en cuenta en el momento de su fallecimiento."
                                                )
                bot_message = (
                    "Si no estás de acuerdo con ser donante de órganos, debes informarlo en el Registro Nacional de No Donantes. "
                    "¿Deseas optar por cremación o sepultura?"
                )
                request.session['step'] = 'opcion_cremacion_sepultura'
            else:
                bot_message = "Lo siento, no entendí tu respuesta. Por favor responde con 'sí' o 'no'."
        elif step == 'opcion_cremacion_sepultura':
            cremation_responses = ["cremación", "crema", "cremar", "incineración", "cremacion"]
            burial_responses = ["sepultura", "tumba", "entierro", "inhumación", "inhumacion"]

            if any(resp in user_message for resp in burial_responses):
                request.session['opcion'] = ("Has optado por la sepultura. Considera los siguientes pasos:"
                                            " 1. Compra de Sepultura:"
                                            " Debes adquirir una sepultura en un cementerio legalmente autorizado. Investiga las opciones disponibles y el costo asociado."
                                            " 2. Asistencia Social:"
                                            " Si no puedes costear la sepultura, puedes solicitar una entrevista con el asistente social de la municipalidad donde vivía el fallecido para evaluar tu situación financiera y determinar si puedes optar a una sepultura gratuita."
                                            " 3. Documentación Requerida: Asegúrate de tener todos los documentos necesarios, como el certificado de defunción, para formalizar la compra o la solicitud de sepultura gratuita."
                                            )
                bot_message = (
                    "Okey, si no tienes dinero para la sepultura, puedes solicitar una entrevista con el asistente social de la municipalidad "
                    "para evaluar si puedes optar a una sepultura gratuita. "
                    "¿Tienes alguna nota adicional que agregar?"
                )
                request.session['step'] = 'notas'
            elif any(resp in user_message for resp in cremation_responses):
                request.session['opcion'] = ("Has optado por la cremación. Los pasos a seguir son:"
                                            " 1. Autorización Necesaria:"
                                            " Se requiere una autorización previa del Director General del Servicio Nacional de Salud o su delegado."
                                            " Además, es necesario presentar una declaración escrita que autorice la cremación, la cual puede ser firmada por el cónyuge sobreviviente o por la mayoría de los hijos."
                                            " 2. Certificado de Defunción: Asegúrate de tener el certificado de defunción emitido por el médico."
                                            " 3. Lugar de Cremación: Investiga y elige una crematoria autorizada. Muchas funerarias ofrecen este servicio y pueden ayudarte con los trámites."
                                            )
                bot_message = (
                    "Para la cremación, necesitas autorización previa del Director General del Servicio Nacional de Salud o su delegado, "
                    "y una declaración escrita autorizando la cremación. "
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
                messages=[{"role": "user", "content": prompt}]
            )
            bot_message = response['choices'][0]['message']['content']

        return JsonResponse({'message': bot_message})

    return JsonResponse({'error': 'Método no permitido'}, status=405)

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
            'rut_cliente': request.session.get('rut_cliente', 'No proporcionado'),
            'certificado_defuncion': request.session.get('certificado_defuncion', 'No proporcionado'),
            'deudas_herencia': request.session.get('deudas_herencia', 'No proporcionado'),
            'donacion': request.session.get('donacion', 'No proporcionado'),
            'opcion': request.session.get('opcion', 'No proporcionado'),
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
