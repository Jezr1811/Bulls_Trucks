from django.contrib import admin  # type: ignore
from .models import Mantenimiento


@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nombre_mantenimiento",
        "vehiculo",
        "trailer",
        "valor",
        "fecha",
        "km_actual",
    )

    list_filter = (
        "fecha",
    )

    search_fields = (
        "nombre_mantenimiento",
        "vehiculo__placa",
        "trailer__placa",
    )