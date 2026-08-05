from django.db import models
from cloudinary.models import CloudinaryField

from viajes.models import Viaje
from vehiculos.models import Vehiculo
from conductores.models import Conductor


class Documento(models.Model):

    TIPOS = [
        ("licencia", "Licencia de conducción"),
        ("soat", "SOAT"),
        ("tecnomecanica", "Tecnomecánica"),
        ("tarjeta", "Tarjeta de propiedad"),
        ("poliza", "Póliza"),
        ("otro", "Otro"),
    ]

    viaje = models.ForeignKey(
        Viaje,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    conductor = models.ForeignKey(
        Conductor,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    tipo = models.CharField(
        max_length=30,
        choices=TIPOS
    )

    numero = models.CharField(
        max_length=80,
        blank=True
    )

    fecha_expedicion = models.DateField()

    fecha_vencimiento = models.DateField(
        blank=True,
        null=True
    )

    # Imagen almacenada en Cloudinary
    imagen = CloudinaryField(
        "imagen",
        blank=True,
        null=True
    )

    # PDF almacenado en Cloudinary
    pdf = CloudinaryField(
        "pdf",
        resource_type="raw",
        blank=True,
        null=True
    )

    observaciones = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.vehiculo}"