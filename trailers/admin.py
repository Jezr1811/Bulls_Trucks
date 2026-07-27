from django.contrib import admin
from .models import Trailer


@admin.register(Trailer)
class TrailerAdmin(admin.ModelAdmin):

    list_display = (
        "placa",
        "tipo",
        "capacidad",
        "kilometraje",
        "estado",
    )

    search_fields = (
        "placa",
        "tipo",
    )

    list_filter = (
        "estado",
    )