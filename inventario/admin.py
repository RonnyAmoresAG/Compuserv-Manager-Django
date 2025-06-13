# admin.py
from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'tipo', 'stock', 'precio_venta', 'permitir_sin_stock')
    list_filter = ('categoria', 'tipo', 'permitir_sin_stock')
    search_fields = ('nombre', 'categoria', 'tipo')
    fields = ('nombre', 'categoria', 'tipo', 'descripcion', 'precio_compra', 'precio_venta', 'stock', 'permitir_sin_stock')

