# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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


class Cementerio(models.Model):
    id_cementerio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cementerio'


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cliente'


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


class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_contratacion = models.DateField(blank=True, null=True)
    id_funeraria = models.ForeignKey('Funeraria', models.DO_NOTHING, db_column='id_funeraria', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'empleado'


class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente', blank=True, null=True)
    id_servicio = models.ForeignKey('Serviciofunerario', models.DO_NOTHING, db_column='id_servicio', blank=True, null=True)
    fecha_emision = models.DateField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'factura'


class Funeraria(models.Model):
    id_funeraria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'funeraria'


class Funerariaproveedor(models.Model):
    id_funeraria = models.OneToOneField(Funeraria, models.DO_NOTHING, db_column='id_funeraria', primary_key=True)  # The composite primary key (id_funeraria, id_proveedor) found, that is not supported. The first column is selected.
    id_proveedor = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='id_proveedor')
    fecha_contrato = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'funerariaproveedor'
        unique_together = (('id_funeraria', 'id_proveedor'),)


class Mascota(models.Model):
    id_mascota = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    raza = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mascota'


class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    id_factura = models.ForeignKey(Factura, models.DO_NOTHING, db_column='id_factura', blank=True, null=True)
    fecha_pago = models.DateField(blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    metodo_pago = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pago'


class PortalfunerappCementerio(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'portalfunerapp_cementerio'


class PortalfunerappFuneraria(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    servicio = models.TextField()
    descripcion = models.TextField()
    imagen = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'portalfunerapp_funeraria'


class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    servicio = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proveedor'


class Sepultura(models.Model):
    id_sepultura = models.AutoField(primary_key=True)
    numero_sepultura = models.CharField(max_length=50, blank=True, null=True)
    id_cementerio = models.ForeignKey(Cementerio, models.DO_NOTHING, db_column='id_cementerio', blank=True, null=True)
    disponible = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sepultura'


class Sepulturamascota(models.Model):
    id_sepultura_mascota = models.AutoField(primary_key=True)
    id_mascota = models.ForeignKey(Mascota, models.DO_NOTHING, db_column='id_mascota', blank=True, null=True)
    id_sepultura = models.ForeignKey(Sepultura, models.DO_NOTHING, db_column='id_sepultura', blank=True, null=True)
    fecha_inhumacion = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sepulturamascota'


class Serviciofunerario(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    tipo_servicio = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    id_funeraria = models.ForeignKey(Funeraria, models.DO_NOTHING, db_column='id_funeraria', blank=True, null=True)
    fecha_servicio = models.DateField(blank=True, null=True)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'serviciofunerario'
