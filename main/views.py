from django.shortcuts import render

def homepage(request):
    return render(request, 'main/index.html')  # Se asegura de que el archivo esté en templates/main/
