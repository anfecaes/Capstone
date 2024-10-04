# Generated by Django 5.1.1 on 2024-10-04 14:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.BooleanField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.BooleanField()),
                ('is_active', models.BooleanField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cementerio',
            fields=[
                ('id_cementerio', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('direccion', models.TextField(blank=True, null=True)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('imagen', models.BinaryField(blank=True, null=True)),
            ],
            options={
                'db_table': 'cementerio',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id_cliente', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('apellidos', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('direccion', models.TextField(blank=True, null=True)),
                ('fecha_registro', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'cliente',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id_empleado', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=255, null=True)),
                ('cargo', models.CharField(blank=True, max_length=100, null=True)),
                ('salario', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('fecha_contratacion', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'empleado',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id_factura', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_emision', models.DateField(blank=True, null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'factura',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Funerariaproveedor',
            fields=[
                ('id_funeraria', models.OneToOneField(db_column='id_funeraria', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='main.funeraria')),
                ('fecha_contrato', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'funerariaproveedor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Mascota',
            fields=[
                ('id_mascota', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('tipo', models.CharField(blank=True, max_length=50, null=True)),
                ('raza', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'mascota',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id_pago', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_pago', models.DateField(blank=True, null=True)),
                ('monto', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('metodo_pago', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'pago',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id_proveedor', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=255, null=True)),
                ('servicio', models.CharField(blank=True, max_length=255, null=True)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('direccion', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'proveedor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sepultura',
            fields=[
                ('id_sepultura', models.AutoField(primary_key=True, serialize=False)),
                ('numero_sepultura', models.CharField(blank=True, max_length=50, null=True)),
                ('disponible', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sepultura',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sepulturamascota',
            fields=[
                ('id_sepultura_mascota', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_inhumacion', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sepulturamascota',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Serviciofunerario',
            fields=[
                ('id_servicio', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_servicio', models.CharField(blank=True, max_length=100, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('precio', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('fecha_servicio', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'serviciofunerario',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Homenaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_persona', models.CharField(max_length=255)),
                ('mensaje_homenaje', models.TextField()),
                ('imagen_persona', models.ImageField(blank=True, null=True, upload_to='homenajes/')),
                ('condolencias', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ServiciosMascotas',
            fields=[
                ('id_servi_mascota', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, null=True)),
                ('direccion', models.TextField(blank=True, null=True)),
                ('telefono', models.CharField(blank=True, null=True)),
                ('email', models.CharField(blank=True, null=True)),
                ('imagen', models.BinaryField(blank=True, null=True)),
            ],
            options={
                'db_table': 'servicios_mascotas',
                'managed': True,
            },
        ),
        migrations.AlterModelOptions(
            name='funeraria',
            options={'managed': True},
        ),
        migrations.RemoveField(
            model_name='funeraria',
            name='id',
        ),
        migrations.RemoveField(
            model_name='funeraria',
            name='latitud',
        ),
        migrations.RemoveField(
            model_name='funeraria',
            name='longitud',
        ),
        migrations.AddField(
            model_name='funeraria',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='funeraria',
            name='id_funeraria',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='funeraria',
            name='imagen',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='funeraria',
            name='telefono',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='funeraria',
            name='direccion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterModelTable(
            name='funeraria',
            table='funeraria',
        ),
    ]
