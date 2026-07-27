from django.contrib import admin

from .models import Gasto


@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "viaje",
        "tipo",
        "valor",
        "fecha",
    )

    list_filter = (
        "tipo",
        "fecha",
    )

    search_fields = (
        "viaje__cliente",
        "descripcion",
    )