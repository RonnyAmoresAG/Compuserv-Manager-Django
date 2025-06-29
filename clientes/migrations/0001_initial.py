# Generated by Django 5.2.2 on 2025-06-05 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('telefono', models.CharField(blank=True, max_length=20)),
                ('direccion', models.CharField(blank=True, max_length=200)),
                ('correo', models.EmailField(blank=True, max_length=254)),
                ('observaciones', models.TextField(blank=True)),
            ],
        ),
    ]
