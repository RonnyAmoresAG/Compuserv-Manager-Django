# models.py
from django.db import models
from django.core.exceptions import ValidationError

class Producto(models.Model):
    TIPO_CHOICES = [
        ('producto', 'Producto'),
        ('repuesto', 'Repuesto'),
        ('accesorio', 'Accesorio'),
    ]

    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='producto')
    descripcion = models.TextField(blank=True)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    permitir_sin_stock = models.BooleanField(default=False, help_text="Permitir vender sin stock (productos puntuales)")

    def __str__(self):
        return f"{self.nombre} ({self.stock} en stock)"

    def clean(self):
        if self.stock < 0:
            raise ValidationError("El stock no puede ser negativo.")
