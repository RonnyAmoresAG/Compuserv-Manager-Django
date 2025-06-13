from django.urls import path
from . import views

urlpatterns = [
    path('imprimir/<int:pk>/', views.imprimir_comprobante, name='imprimir_comprobante'),
]

