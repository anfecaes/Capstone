# Generated by Django 4.2.6 on 2024-09-26 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portalfunerapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cementerio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('direccion', models.TextField()),
                ('telefono', models.CharField(max_length=20)),
            ],
        ),
    ]