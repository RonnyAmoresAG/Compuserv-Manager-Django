from django.db import models
from clientes.models import Cliente

class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    codigo = models.CharField(max_length=20, unique=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    ruta_archivo = models.FileField(upload_to='facturas_pdfs/', null=True, blank=True)

    # NUEVO: referencias al origen
    venta = models.OneToOneField("ventas.Venta", on_delete=models.SET_NULL, null=True, blank=True)
    servicio = models.OneToOneField("servicios.Servicio", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Factura {self.codigo}"

    def tipo_origen(self):
        if self.venta:
            return "Venta"
        elif self.servicio:
            return dict(self.servicio.TIPO_CHOICES).get(self.servicio.tipo, "Servicio")
        return "Desconocido"


    def enlace_origen(self):
        if self.venta:
            return f"/admin/ventas/venta/{self.venta.id}/change/"
        elif self.servicio:
            return f"/admin/servicios/servicio/{self.servicio.id}/change/"
        return "#"
