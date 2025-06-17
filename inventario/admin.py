# admin.py
from django.contrib import admin
from .models import Producto, Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'tipo', 'stock', 'precio_venta', 'permitir_sin_stock')
    list_filter = ('categoria', 'tipo', 'permitir_sin_stock')
    search_fields = ('nombre',)
    fields = ('nombre', 'categoria', 'tipo', 'descripcion', 'precio_compra', 'precio_venta', 'stock', 'permitir_sin_stock')
