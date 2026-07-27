from django.contrib import admin

from .models import Viaje


@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "cliente",
        "origen",
        "destino",
        "conductor",
        "vehiculo",
        "trailer",
        "estado",
        "fecha_inicio",
    )

    list_filter = (
        "estado",
        "fecha_inicio",
    )

    search_fields = (
        "cliente",
        "origen",
        "destino",
    )