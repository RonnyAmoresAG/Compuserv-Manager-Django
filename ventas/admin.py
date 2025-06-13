from django.contrib import admin, messages
from .models import Venta, DetalleVenta
from django.utils.html import format_html


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    inlines = [DetalleVentaInline]
    list_display = ('codigo_factura', 'cliente', 'fecha', 'total', 'forma_pago_coloreada', 'mensaje_whatsapp')
    search_fields = ('codigo_factura', 'cliente__nombre')
    list_filter = ('fecha', 'forma_pago')
    exclude = ('codigo_factura', 'total')
    readonly_fields = ('ver_factura_pdf',)

    def forma_pago_coloreada(self, obj):
        colores = {
            'efectivo': 'green',
            'transferencia': 'blue',
            'tarjeta': 'orange'
        }
        color = colores.get(obj.forma_pago, 'gray')
        return format_html(
            '<span style="padding: 4px 8px; border-radius: 4px; background-color: {}; color: white;">{}</span>',
            color,
            obj.get_forma_pago_display()
        )
    forma_pago_coloreada.short_description = "Forma de Pago"

    def mensaje_whatsapp(self, obj):
        if obj.cliente and obj.cliente.telefono:
            mensaje = f"Hola {obj.cliente.nombre}, su compra está registrada con el total de ${obj.total}."
            link = f"https://wa.me/593{obj.cliente.telefono.replace(' ', '')}?text={mensaje.replace(' ', '%20')}"
            return format_html('<a href="{}" target="_blank">WhatsApp</a>', link)
        return "-"
    mensaje_whatsapp.short_description = "Mensaje"

    def ver_factura_pdf(self, obj):
        from facturacion.models import Factura
        factura = Factura.objects.filter(codigo=obj.codigo_factura).first()
        if factura and factura.ruta_archivo:
            return format_html(
                '<a href="{}" target="_blank" style="padding: 6px 12px; background-color: #28a745; color: white; text-decoration: none; border-radius: 4px;">📄 Ver factura PDF</a>',
                factura.ruta_archivo.url
            )
        return "Factura no generada"
    ver_factura_pdf.short_description = "Comprobante generado"

    def response_add(self, request, obj, post_url_continue=None):
        if hasattr(obj, 'codigo_factura'):
            from facturacion.models import Factura
            factura = Factura.objects.filter(codigo=obj.codigo_factura).first()
            if factura and factura.ruta_archivo:
                mensaje = format_html(
                    '<a href="{}" target="_blank" style="padding: 8px 15px; background-color: #007bff; color: white; text-decoration: none; border-radius: 4px;">📄 Ver factura generada</a>',
                    factura.ruta_archivo.url
                )
                self.message_user(request, mensaje, level=messages.SUCCESS)
        return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        return self.response_add(request, obj)
