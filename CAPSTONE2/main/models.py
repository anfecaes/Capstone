# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
# from uuid import uuid4
#importaciones para calificaciones
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)

# Modelo para los usuarios del portal
class Usuario(AbstractUser):
    rut = models.CharField(max_length=12, unique=True)  # RUT único para cada usuario
    telefono = models.CharField(max_length=15)
    edad = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)

    # Agregar related_name para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',  # Cambia el related_name para evitar conflicto
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_permission_set',  # Cambia el related_name para evitar conflicto
        blank=True,
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return self.username
    
class Cementerio(models.Model):
    id_cementerio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    imagen = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'cementerio'

    def __str__(self):
        return self.nombre

    def calificacion_promedio(self):
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(self)
        calificaciones = Calificacion.objects.filter(content_type=content_type, object_id=self.id_cementerio)
        if calificaciones.exists():
            promedio = sum(c.puntuacion for c in calificaciones) / calificaciones.count()
            return round(promedio, 2)
        return 0
# class Cementerio(models.Model):
#     id_cementerio = models.AutoField(primary_key=True)
#     nombre = models.CharField(max_length=255)
#     direccion = models.TextField(blank=True, null=True)
#     telefono = models.CharField(max_length=20, blank=True, null=True)
#     imagen = models.BinaryField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'cementerio'


class Calificacion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    puntuacion = models.PositiveSmallIntegerField()  # De 1 a 5 estrellas, por ejemplo
    comentario = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario} - {self.puntuacion} estrellas'

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Funeraria(models.Model):
    id_funeraria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    imagen = models.BinaryField(blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'funeraria'

    def __str__(self):
        return self.nombre

    def calificacion_promedio(self):
        calificaciones = self.calificaciones.all()  # Usar el related_name definido en el modelo Calificacion
        if calificaciones.exists():
            promedio = sum(c.puntuacion for c in calificaciones) / calificaciones.count()
            return round(promedio, 2)
        return 0  # Si no hay calificaciones, retornar 0
# class Funeraria(models.Model):
#     id_funeraria = models.AutoField(primary_key=True)
#     nombre = models.CharField(max_length=255)
#     direccion = models.TextField(blank=True, null=True)
#     telefono = models.CharField(max_length=20, blank=True, null=True)
#     email = models.CharField(unique=True, max_length=255, blank=True, null=True)
#     imagen = models.BinaryField(blank=True, null=True)
    
#     # Nuevo campo para almacenar un enlace (link)
#     link = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'funeraria'

#     def __str__(self):
#         return self.nombre

class Homenaje(models.Model):
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    mensaje = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    es_para_mascota = models.BooleanField(default=False)
    invitados = models.ManyToManyField(Usuario, related_name='invitados', blank=True)
    imagen = models.ImageField(upload_to='homenajes/imagenes/', null=True, blank=True)
    video = models.FileField(upload_to='homenajes/videos/', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    velas = models.PositiveIntegerField(default=0)  # Reacción de velas
    palomas = models.PositiveIntegerField(default=0)  # Reacción de palomas

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ver_homenaje', kwargs={'slug': self.slug})  # Devuelve la URL basada en el slug

    def __str__(self):
        return self.titulo
    class Meta:
        managed = True
        db_table = 'main_homenaje'

class Condolencia(models.Model):
    homenaje = models.ForeignKey(Homenaje, related_name='condolencias', on_delete=models.CASCADE)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.autor.username} - {self.mensaje[:30]}"

class ServiciosMascotas(models.Model):
    id_servi_mascota = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    imagen = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'servicios_mascotas'

    def __str__(self):
        return self.nombre

    def calificacion_promedio(self):
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(self)
        calificaciones = Calificacion.objects.filter(content_type=content_type, object_id=self.id_servi_mascota)
        if calificaciones.exists():
            promedio = sum(c.puntuacion for c in calificaciones) / calificaciones.count()
            return round(promedio, 2)
        return 0
# class ServiciosMascotas(models.Model):
#     id_servi_mascota = models.AutoField(primary_key=True)
#     nombre = models.CharField(blank=True, null=True)
#     direccion = models.TextField(blank=True, null=True)
#     telefono = models.CharField(blank=True, null=True)
#     email = models.CharField(blank=True, null=True)
#     imagen = models.BinaryField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'servicios_mascotas'

# implementación de la calculadora
class TipoServicio(models.Model):
    tipo = models.CharField(max_length=50)
    precio_base = models.IntegerField()

    def __str__(self):
        return self.tipo

class ServicioAdicional(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()

    def __str__(self):
        return self.nombre

class Ubicacion(models.Model):
    region = models.CharField(max_length=100)
    factor_precio = models.FloatField()

    def __str__(self):
        return self.region

class Beneficio(models.Model):
    tipo = models.CharField(max_length=100)
    monto = models.IntegerField()

    def __str__(self):
        return self.tipo

class ProductoAdicional(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()

    def __str__(self):
        return self.nombre

class ImpuestoDescuento(models.Model):
    descripcion = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=[('IVA', 'IVA'), ('descuento', 'Descuento')])
    valor = models.FloatField()

    def __str__(self):
        return self.descripcion
    
#Mascota
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
