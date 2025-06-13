from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Servicio

def dashboard_view(request):
    return HttpResponse("Dashboard funcional.")

def imprimir_comprobante(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    return render(request, 'servicios/imprimir_comprobante.html', {
        'pdf_url': servicio.ruta_comprobante.url
    })
