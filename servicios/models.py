from django.db import models
from django.core.exceptions import ValidationError
from clientes.models import Cliente
from facturacion.pdf_utils import generar_comprobante_pdf, generar_factura_pdf
from facturacion.models import Factura
from facturacion.utils import generar_codigo_factura
from inventario.models import Producto

class Servicio(models.Model):
    TIPO_CHOICES = [
        ('tecnico', 'Servicio Técnico'),
        ('instalacion', 'Instalación de Cámaras'),
    ]

    ESTADO_CHOICES = [
        ('recibido', 'Recibido'),
        ('diagnosticado', 'Diagnosticado'),
        ('presupuestado', 'Presupuestado'),
        ('en_reparacion', 'En reparación'),
        ('listo_para_entregar', 'Listo para entregar'),
        ('entregado', 'Entregado'),
        ('cotizado', 'Cotizado'),
        ('pendiente_instalacion', 'Pendiente instalación'),
        ('instalado', 'Instalado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    codigo = models.CharField(max_length=20, unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    accesorios = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)
    estado = models.CharField(max_length=30, choices=ESTADO_CHOICES, default='recibido')
    fecha_ingreso = models.DateField(auto_now_add=True)
    fecha_entrega = models.DateField(null=True, blank=True)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ruta_comprobante = models.FileField(upload_to='comprobantes/', null=True, blank=True)
    ruta_factura = models.FileField(upload_to='facturas_pdfs/', null=True, blank=True)

    def clean(self):
        if self.estado in ['entregado', 'instalado'] and not self.costo_total:
            raise ValidationError("Debe ingresar el costo total antes de marcar el servicio como entregado o instalado.")

    def generar_codigo_unico(self):
        prefix = 'ST' if self.tipo == 'tecnico' else 'IN'
        existentes = Servicio.objects.filter(codigo__startswith=prefix).values_list('codigo', flat=True)
        usados = set()
        for cod in existentes:
            try:
                usados.add(int(cod.split('-')[1]))
            except:
                continue
        number = 1
        while number in usados:
            number += 1
        return f"{prefix}-{str(number).zfill(6)}"

    def save(self, *args, **kwargs):
        self.clean()
        nuevo_servicio = self.pk is None

        if not self.codigo:
            self.codigo = self.generar_codigo_unico()

        super().save(*args, **kwargs)

        if nuevo_servicio and not self.ruta_comprobante:
            generar_comprobante_pdf(self)

        if self.estado in ['entregado', 'instalado'] and self.costo_total and not Factura.objects.filter(servicio=self).exists():
            factura = Factura.objects.create(
                cliente=self.cliente,
                codigo=generar_codigo_factura(),
                total=self.costo_total,
                servicio=self
            )
            generar_factura_pdf(factura)
            self.ruta_factura = factura.ruta_archivo
            super().save(update_fields=['ruta_factura'])

    def __str__(self):
        return self.codigo if self.codigo else f"{self.get_tipo_display()} sin código"

class RepuestoUsado(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='repuestos_usados')
    producto = models.ForeignKey(Producto, limit_choices_to={'tipo': 'repuesto'}, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self.pk:
            anterior = RepuestoUsado.objects.get(pk=self.pk)
            diferencia = self.cantidad - anterior.cantidad
        else:
            diferencia = self.cantidad

        super().save(*args, **kwargs)
        self.producto.stock -= diferencia
        self.producto.save()

    def delete(self, *args, **kwargs):
        self.producto.stock += self.cantidad
        self.producto.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.producto.nombre} usado en {self.servicio.codigo}"
