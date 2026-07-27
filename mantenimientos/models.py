from django.db import models
from vehiculos.models import Vehiculo
from trailers.models import Trailer


class Mantenimiento(models.Model):

    nombre_mantenimiento = models.CharField(
        max_length=100
    )

    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    trailer = models.ForeignKey(
        Trailer,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    valor = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    fecha = models.DateField()

    km_actual = models.IntegerField()

    km_duracion = models.IntegerField(
        help_text="Kilómetros para el próximo mantenimiento"
    )

    descripcion = models.TextField(
        blank=True
    )

    foto = models.FileField(
        upload_to="mantenimientos/",
        blank=True,
        null=True
    )

    def proximo_km(self):
        return self.km_actual + self.km_duracion

    def __str__(self):
        return self.nombre_mantenimiento