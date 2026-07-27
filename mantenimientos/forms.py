from django import forms
from .models import Mantenimiento
from vehiculos.models import Vehiculo


class MantenimientoForm(forms.ModelForm):

    class Meta:
        model = Mantenimiento
        fields = "__all__"
        widgets = {
            "fecha": forms.DateInput(
                attrs={"type": "date"}
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Si es un conductor, limitamos el listado de camiones
        if user and not user.is_superuser and hasattr(user, 'conductor'):
            # El selector de vehículos mostrará UNICAMENTE el camión asignado a él
            self.fields['vehiculo'].queryset = Vehiculo.objects.filter(conductor=user.conductor)