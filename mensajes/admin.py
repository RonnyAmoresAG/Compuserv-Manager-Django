from django.contrib import admin
from .models import MensajeEnviado

@admin.register(MensajeEnviado)
class MensajeEnviadoAdmin(admin.ModelAdmin):
    list_display = ('servicio', 'fecha_envio', 'mensaje')
    search_fields = ('servicio__codigo', 'mensaje')
    list_filter = ('fecha_envio',)
