# Generated by Django 5.1.1 on 2024-10-02 21:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='funeraria',
            options={'ordering': ['nombre'], 'verbose_name': 'Funeraria', 'verbose_name_plural': 'Funerarias'},
        ),
    ]
