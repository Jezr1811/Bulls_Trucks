from django.db import models

from viajes.models import Viaje


class Gasto(models.Model):

    TIPOS = [
        ("combustible", "Combustible"),
        ("peaje", "Peaje"),
        ("alimentacion", "Alimentación"),
        ("hospedaje", "Hospedaje"),
        ("mantenimiento", "Mantenimiento"),
        ("otro", "Otro"),
    ]

    viaje = models.ForeignKey(
        Viaje,
        on_delete=models.CASCADE
    )

    tipo = models.CharField(
    max_length=20,
    choices=TIPOS,
    default="otro"
    )

    valor = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    fecha = models.DateField()

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.tipo} - ${self.valor}"