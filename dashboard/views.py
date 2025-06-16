from django.shortcuts import render
from django.utils.timezone import now, timedelta
from servicios.models import Servicio
from ventas.models import Venta
from inventario.models import Producto
import locale

# Configurar locale en español
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.utf8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, '')

# Función para mostrar dinero con formato: 1.234,56
def format_money(valor):
    if valor is None:
        return "0,00"
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def dashboard_view(request):
    hoy = now().date()
    semana_inicio = hoy - timedelta(days=hoy.weekday())

    servicios_activos = Servicio.objects.exclude(estado='entregado')
    servicios_entregados = Servicio.objects.filter(
        estado='entregado',
        fecha_entrega__gte=semana_inicio
    )
    ventas_recientes = Venta.objects.filter(fecha=hoy)
    productos_bajo_stock = Producto.objects.filter(stock__lte=3)

    total_ventas_hoy = sum(v.total for v in ventas_recientes)
    total_ingresos_servicios = sum(s.costo_total for s in servicios_entregados if s.costo_total)

    # Ingresos del mes actual
    mes_actual = hoy.strftime('%B').capitalize()
    ingresos_mes = sum(
        s.costo_total for s in Servicio.objects.filter(
            estado__in=['entregado', 'instalado'],
            fecha_entrega__month=hoy.month,
            fecha_entrega__year=hoy.year
        ) if s.costo_total
    )

    estado_colores = {
        'recibido': 'bg-danger',
        'diagnosticado': 'bg-orange',
        'presupuestado': 'bg-warning',
        'cotizado': 'bg-warning',
        'en_reparacion': 'bg-info',
        'pendiente_instalacion': 'bg-primary',
        'listo_para_entregar': 'bg-success',
        'instalado': 'bg-success',
    }

    estados_resumen = [
        {
            'nombre': estado.replace('_', ' ').title(),
            'total': servicios_activos.filter(estado=estado).count(),
            'color': color
        }
        for estado, color in estado_colores.items()
        if servicios_activos.filter(estado=estado).exists()
    ]

    return render(request, 'dashboard/dashboard.html', {
        'servicios_activos': servicios_activos,
        'servicios_entregados': servicios_entregados,
        'ventas_recientes': ventas_recientes,
        'productos_bajo_stock': productos_bajo_stock,
        'total_ventas_hoy': format_money(total_ventas_hoy),
        'total_ingresos_servicios': format_money(total_ingresos_servicios),
        'ingresos_mes': format_money(ingresos_mes),
        'mes_actual': mes_actual,
        'estados_resumen': estados_resumen,
    })
