from django.contrib import admin, messages
from django.utils.html import format_html
from .models import Servicio, RepuestoUsado
from mensajes.utils import generar_mensaje

class RepuestoUsadoInline(admin.TabularInline):
    model = RepuestoUsado
    extra = 1
    verbose_name = "Repuesto utilizado"
    verbose_name_plural = "Repuestos utilizados"

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.estado != 'en_reparacion':
            return [f.name for f in self.model._meta.fields if f.name != 'id']
        return []

    def has_add_permission(self, request, obj):
        return obj and obj.estado == 'en_reparacion'

    def has_change_permission(self, request, obj=None):
        return obj and obj.estado == 'en_reparacion'

    def has_delete_permission(self, request, obj=None):
        return obj and obj.estado == 'en_reparacion'

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    inlines = [RepuestoUsadoInline]
    list_display = ('codigo', 'cliente', 'estado_coloreado', 'mensaje_whatsapp')
    readonly_fields = ('codigo', 'mostrar_comprobante', 'mostrar_factura')
    list_filter = ('estado', 'tipo', 'fecha_entrega')
    search_fields = ('codigo', 'cliente__nombre', 'estado')
    actions = ['marcar_como_entregado']

    def get_fields(self, request, obj=None):
        fields = [
            'cliente', 'tipo', 'descripcion', 'accesorios',
            'observaciones', 'estado', 'fecha_entrega', 'costo_total'
        ]
        if obj:
            fields.insert(2, 'codigo')
            fields += ['mostrar_comprobante', 'mostrar_factura']
        return fields

    def mostrar_comprobante(self, obj):
        if obj.ruta_comprobante:
            return format_html('<a href="{}" target="_blank">Ver comprobante</a>', obj.ruta_comprobante.url)
        return "-"
    mostrar_comprobante.short_description = "Comprobante"

    def mostrar_factura(self, obj):
        if obj.ruta_factura:
            return format_html('<a href="{}" target="_blank">Ver factura</a>', obj.ruta_factura.url)
        return "-"
    mostrar_factura.short_description = "Factura"

    def mensaje_whatsapp(self, obj):
        if not obj.cliente or not obj.cliente.telefono:
            return "-"
        mensaje = generar_mensaje(obj)
        texto = mensaje.replace(' ', '%20')
        numero = obj.cliente.telefono.replace(' ', '')
        link = f"https://wa.me/593{numero}?text={texto}"
        return format_html('<a href="{}" target="_blank">WhatsApp</a>', link)
    mensaje_whatsapp.short_description = "Mensaje"

    def estado_coloreado(self, obj):
        colores = {
            'recibido': 'gray',
            'diagnosticado': 'orange',
            'presupuestado': 'dodgerblue',
            'en_reparacion': 'purple',
            'listo_para_entregar': 'green',
            'entregado': 'black',
            'cotizado': 'deepskyblue',
            'pendiente_instalacion': 'darkorange',
            'instalado': 'darkgreen',
        }
        color = colores.get(obj.estado, 'black')
        return format_html(
            '<span style="padding: 3px 8px; border-radius: 5px; background-color: {}; color: white;">{}</span>',
            color, obj.get_estado_display()
        )
    estado_coloreado.short_description = "Estado"

    def marcar_como_entregado(self, request, queryset):
        actualizados = queryset.update(estado='entregado')
        self.message_user(request, f"{actualizados} servicio(s) marcados como entregado.")
    marcar_como_entregado.short_description = "Marcar como entregado"

    def response_add(self, request, obj, post_url_continue=None):
        if obj.ruta_comprobante:
            self.message_user(request, format_html(
                '<a href="{}" target="_blank" style="padding: 8px 15px; background-color: #28a745; color: white; text-decoration: none; border-radius: 4px;">📄 Abrir comprobante en nueva pestaña</a>',
                obj.ruta_comprobante.url
            ), level=messages.SUCCESS)

        if obj.ruta_factura:
            self.message_user(request, format_html(
                '<a href="{}" target="_blank" style="padding: 8px 15px; background-color: #007bff; color: white; text-decoration: none; border-radius: 4px;">📄 Ver factura generada</a>',
                obj.ruta_factura.url
            ), level=messages.SUCCESS)

        return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        if obj.ruta_factura:
            self.message_user(request, format_html(
                '<a href="{}" target="_blank" style="padding: 8px 15px; background-color: #007bff; color: white; text-decoration: none; border-radius: 4px;">📄 Ver factura generada</a>',
                obj.ruta_factura.url
            ), level=messages.SUCCESS)

        if obj.ruta_comprobante:
            self.message_user(request, format_html(
                '<a href="{}" target="_blank" style="padding: 8px 15px; background-color: #28a745; color: white; text-decoration: none; border-radius: 4px;">📄 Ver comprobante</a>',
                obj.ruta_comprobante.url
            ), level=messages.SUCCESS)

        return super().response_change(request, obj)
