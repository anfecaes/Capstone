from django.db import models
from django.utils import timezone

class Funeraria(models.Model):
    nombre = models.CharField(max_length=255)  # Nombre de la funeraria
    direccion = models.CharField(max_length=255)  # Dirección de la funeraria
    latitud = models.FloatField()  # Latitud geográfica
    longitud = models.FloatField()  # Longitud geográfica

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Funeraria"
        verbose_name_plural = "Funerarias"
        ordering = ['nombre']  # Ordena las funerarias por nombre al listar

class Mascota(models.Model):
    foto = models.ImageField(upload_to='fotos/')
    descripcion = models.TextField()
    edad = models.IntegerField()
    vacunas_al_dia = models.CharField(max_length=50)
    documento_vacunas = models.ImageField(upload_to='documentos_vacunas/', blank=True, null=True)
    motivo = models.TextField()
    nombre = models.TextField()  # Asegúrate de que este campo esté presente
    contacto = models.TextField()  # Asegúrate de que este campo esté presente
    fecha = models.DateTimeField(auto_now_add=True)  # Debe estar aquí

    def __str__(self):
        return self.nombre
    
class OrdenPago(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('error', 'Error'),
    ]

    estado = models.CharField(max_length=50, choices=ESTADOS, default='pendiente')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    numero_orden = models.CharField(max_length=50, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    error = models.TextField(null=True, blank=True)  # Campo para registrar errores

    def __str__(self):
        return f'Orden {self.numero_orden} - Estado: {self.estado}'