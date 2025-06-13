from django.contrib import admin
from .models import Factura
from django.utils.html import format_html

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'cliente', 'total', 'fecha', 'tipo_origen_coloreado', 'ver_origen')
    search_fields = ('codigo', 'cliente__nombre')
    list_filter = ('fecha',)

    def tipo_origen_coloreado(self, obj):
        tipo = obj.tipo_origen()
        color = {
            "Venta": "green",
            "Servicio Técnico": "blue",
            "Desconocido": "gray"
        }.get(tipo, "black")
        return format_html(
            '<span style="padding: 4px 10px; border-radius: 5px; background-color: {}; color: white;">{}</span>',
            color, tipo
        )
    tipo_origen_coloreado.short_description = "Tipo de Origen"

    def ver_origen(self, obj):
        url = obj.enlace_origen()
        return format_html('<a href="{}">Ver {}</a>', url, obj.tipo_origen())
    ver_origen.short_description = "Origen"
