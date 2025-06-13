from django.shortcuts import render
from servicios.models import Servicio
from ventas.models import Venta
from inventario.models import Producto
from django.utils.timezone import now
import json

def dashboard_view(request):
    hoy = now().date()

    servicios_activos = Servicio.objects.filter(
        estado__in=[
            'recibido', 'diagnosticado', 'presupuestado',
            'cotizado', 'en_reparacion', 'pendiente_instalacion',
            'listo_para_entregar', 'entregado', 'instalado'
        ]
    )
    ventas_recientes = Venta.objects.filter(fecha=hoy)
    productos_bajo_stock = Producto.objects.filter(stock__lte=3)

    total_ventas_hoy = sum([v.total for v in ventas_recientes])

    estado_colores = {
        'recibido': 'bg-danger',
        'diagnosticado': 'bg-orange',
        'presupuestado': 'bg-warning',
        'cotizado': 'bg-warning',
        'en_reparacion': 'bg-info',
        'pendiente_instalacion': 'bg-primary',
        'listo_para_entregar': 'bg-success',
        'entregado': 'bg-secondary',
        'instalado': 'bg-success'
    }

    estados_resumen = []
    for estado, color in estado_colores.items():
        cantidad = servicios_activos.filter(estado=estado).count()
        if cantidad > 0:
            estados_resumen.append({
                'nombre': estado.replace('_', ' ').title(),
                'total': cantidad,
                'color': color
            })

    context = {
        'servicios_activos': servicios_activos,
        'ventas_recientes': ventas_recientes,
        'productos_bajo_stock': productos_bajo_stock,
        'fecha_hoy': hoy,
        'total_ventas_hoy': total_ventas_hoy,
        'estados_resumen': estados_resumen,
        'labels': json.dumps(['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']),
        'datos': json.dumps([12, 19, 3, 5, 2, 3, 8])
    }

    return render(request, 'dashboard/dashboard.html', context)
