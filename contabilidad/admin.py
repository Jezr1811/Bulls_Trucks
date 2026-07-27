from django.contrib import admin
from .models import Transaccion  # 🔍 Cambiamos 'Movimiento' por 'Transaccion'

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    # Esto hará que tu panel de Django Admin sea súper limpio y legible
    list_display = ('id', 'usuario', 'tipo', 'monto', 'categoria', 'fecha_hora')
    list_filter = ('tipo', 'categoria', 'fecha_hora')
    search_fields = ('descripcion', 'categoria')