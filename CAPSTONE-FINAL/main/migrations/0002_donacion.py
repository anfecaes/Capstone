# Generated by Django 5.1.2 on 2024-11-04 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_donante', models.CharField(max_length=255)),
                ('email_donante', models.EmailField(max_length=254)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaccion_id', models.CharField(blank=True, max_length=255, null=True)),
                ('pagado', models.BooleanField(default=False)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
