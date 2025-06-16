from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre', 'telefono', 'correo')
    search_fields = ('cedula', 'nombre', 'telefono', 'correo')
    list_filter = ('correo',)
    list_per_page = 20
    ordering = ('nombre',)
    fields = ('cedula', 'nombre', 'telefono', 'correo', 'direccion')
