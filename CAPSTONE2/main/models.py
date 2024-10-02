from django.db import models

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
