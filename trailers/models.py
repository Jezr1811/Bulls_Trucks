from django.db import models


class Trailer(models.Model):

    ESTADOS = [
        ('activo', 'Activo'),
        ('mantenimiento', 'Mantenimiento'),
    ]

    placa = models.CharField(
        max_length=20,
        unique=True
    )

    tipo = models.CharField(
        max_length=80
    )

    capacidad = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    kilometraje = models.PositiveIntegerField(
        default=0
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='activo'
    )

    def __str__(self):
        return self.placa