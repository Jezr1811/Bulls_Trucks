from django.contrib import admin

from .models import Conductor


@admin.register(Conductor)
class ConductorAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nombre",
        "telefono",
        "correo",
        "estado",
    )

    list_filter = (
        "estado",
    )

    search_fields = (
        "nombre",
        "telefono",
        "correo",
    )