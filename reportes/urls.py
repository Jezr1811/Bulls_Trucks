from django.urls import path
from . import views

app_name = "reportes"

urlpatterns = [
    path("viajes/", views.reporte_viajes, name="reporte_viajes"),
    path("mantenimiento/", views.reporte_mantenimiento, name="reporte_mantenimiento"),
    path("conductores/", views.reporte_conductores, name="reporte_conductores"),
]