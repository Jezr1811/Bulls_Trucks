from django.db import models

from conductores.models import Conductor
from vehiculos.models import Vehiculo
from trailers.models import Trailer


class Viaje(models.Model):

    cliente = models.CharField(
        max_length=150
    )

    origen = models.CharField(
        max_length=150
    )

    destino = models.CharField(
        max_length=150
    )

    flete = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    anticipo = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    fecha_inicio = models.DateField()

    fecha_fin = models.DateField(
        null=True,
        blank=True
    )

    conductor = models.ForeignKey(
        Conductor,
        on_delete=models.PROTECT
    )

    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.PROTECT
    )

    trailer = models.ForeignKey(
        Trailer,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("en_curso", "En Curso"),
        ("finalizado", "Finalizado"),
        ("cancelado", "Cancelado"),
    ]

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="pendiente"
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.cliente} - {self.origen} → {self.destino}"

    @property
    def total_gastos(self):
        """
        Calcula la suma de todos los gastos asociados a este viaje.
        Usando el campo real 'valor' del modelo Gasto.
        """
        if hasattr(self, 'gasto_set'):
            return sum(gasto.valor for gasto in self.gasto_set.all())
        return 0

    @property
    def resultado(self):
        """Calcula la ganancia real: Flete menos los Gastos acumulados"""
        from decimal import Decimal
        return self.flete - Decimal(self.total_gastos)