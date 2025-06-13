from django.db import models
from servicios.models import Servicio

class MensajeEnviado(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje para {self.servicio.codigo} - {self.fecha_envio.strftime('%Y-%m-%d')}"
