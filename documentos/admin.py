from django.contrib import admin

from .models import Documento


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "viaje",
        "vehiculo",
        "conductor",
        "tipo",
        "numero",
        "fecha_expedicion",
        "fecha_vencimiento",
    )

    list_filter = (
        "tipo",
        "vehiculo",
        "fecha_expedicion",
    )

    search_fields = (
        "numero",
        "vehiculo__placa",
        "conductor__nombre",
        "viaje__cliente",
        "observaciones",
    )

    ordering = (
        "-fecha_expedicion",
    )