from django.db import models
from django.core.validators import RegexValidator

class Cliente(models.Model):
    cedula = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{10}$', message='La cédula debe tener exactamente 10 dígitos.')],
        verbose_name='Cédula'
    )
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^\d{10}$', message='El número debe tener exactamente 10 dígitos.')],
        verbose_name='Número de teléfono'
    )
    correo = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    
    # ¡eliminamos observaciones!

    def __str__(self):
        return f"{self.nombre} - {self.cedula}"
