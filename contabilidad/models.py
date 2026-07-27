from django.db import models
from django.contrib.auth.models import User

class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
    ]
    
    CATEGORIA_CHOICES = [
        ('combustible', 'Combustible'),
        ('peajes', 'Peajes'),
        ('viaticos', 'Viáticos'),
        ('mantenimiento', 'Mantenimiento'),
        ('pago_viaje', 'Pago de Viaje'),
        ('otros', 'Otros'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transacciones")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo.upper()} - {self.monto} ({self.categoria})"