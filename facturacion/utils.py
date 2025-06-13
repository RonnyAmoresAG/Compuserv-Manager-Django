def generar_codigo_factura():
    from .models import Factura
    ultimo = Factura.objects.filter(codigo__startswith='F-').order_by('-id').first()
    try:
        numero = int(ultimo.codigo.split('-')[1]) + 1 if ultimo else 1
    except (IndexError, ValueError):
        numero = 1
    return f"F-{numero:06d}"
