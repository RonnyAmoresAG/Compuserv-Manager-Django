from django.db import models
from django.core.exceptions import ValidationError
from clientes.models import Cliente
from inventario.models import Producto
from facturacion.models import Factura
from facturacion.utils import generar_codigo_factura
from facturacion.pdf_utils import generar_factura_pdf
from django.utils import timezone

class Venta(models.Model):
    FORMAS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia Bancaria'),
        ('tarjeta', 'Tarjeta Crédito/Débito'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    forma_pago = models.CharField(max_length=50, choices=FORMAS_PAGO)
    codigo_factura = models.CharField(max_length=20, unique=True, blank=True)

    def clean(self):
        if self.pk and self.detalles.count() == 0:
            raise ValidationError("La venta debe contener al menos un producto.")

    def save(self, *args, **kwargs):
        creando = self.pk is None

        if not self.codigo_factura:
            self.codigo_factura = generar_codigo_factura()

        if not self.cliente:
            self.cliente = Cliente.objects.get_or_create(nombre="Consumidor Final")[0]
        
        if not self.fecha:
            self.fecha = timezone.now().date()

        super().save(*args, **kwargs)

        if creando:
            factura = Factura.objects.create(
                cliente=self.cliente,
                codigo=self.codigo_factura,
                total=self.total,
                venta=self
            )
            generar_factura_pdf(factura)
            factura.save()

    def __str__(self):
        return f"Venta {self.codigo_factura}"

    def calcular_total(self):
        total = sum([detalle.subtotal() for detalle in self.detalles.all()])
        self.total = total
        self.save(update_fields=['total'])


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def save(self, *args, **kwargs):
        # Asignar precio_unitario por defecto desde el producto si está vacío
        if self.precio_unitario is None:
            self.precio_unitario = self.producto.precio_venta

        if self.producto.stock < self.cantidad and not self.producto.permitir_sin_stock:
            raise ValidationError(f"No hay suficiente stock para {self.producto.nombre}")

        es_nuevo = self.pk is None
        super().save(*args, **kwargs)

        if es_nuevo:
            self.producto.stock -= self.cantidad
            self.producto.save()

        if self.venta_id:
            self.venta.calcular_total()

