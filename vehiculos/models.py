from django.db import models
from conductores.models import Conductor


class Vehiculo(models.Model):

    placa = models.CharField(
        max_length=20,
        unique=True
    )

    modelo = models.CharField(
        max_length=100
    )

    kilometraje_actual = models.IntegerField(
        default=0
    )

    conductor = models.ForeignKey(
        Conductor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vehiculos"
    )

    ESTADOS = [
        ("activo", "Activo"),
        ("mantenimiento", "Mantenimiento"),
    ]

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="activo"
    )

    def __str__(self):
        return self.placa