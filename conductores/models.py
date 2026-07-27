from django.db import models
from django.contrib.auth.models import User


class Conductor(models.Model):

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    ESTADOS = [
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
    ]

    nombre = models.CharField(
        max_length=100
    )

    telefono = models.CharField(
        max_length=20,
        blank=True
    )

    correo = models.EmailField(
        blank=True
    )

    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default="activo"
    )

    def __str__(self):
        return self.nombre