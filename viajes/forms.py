from django import forms
from .models import Viaje
from vehiculos.models import Vehiculo  # Importamos Vehiculo para poder filtrar su QuerySet


class ViajeForm(forms.ModelForm):

    class Meta:
        model = Viaje
        fields = "__all__"

        widgets = {
            "fecha_inicio": forms.DateInput(
                attrs={"type": "date"}
            ),
            "fecha_fin": forms.DateInput(
                attrs={"type": "date"}
            ),
        }

    def __init__(self, *args, **kwargs):
        # 1. Extraemos el usuario que pasaremos desde la vista
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # 2. Si el usuario está autenticado y es un conductor (no administrador)
        if user and not user.is_superuser and hasattr(user, 'conductor'):
            
            # Filtramos para que en el select SOLO aparezcan sus vehículos asignados
            self.fields['vehiculo'].queryset = Vehiculo.objects.filter(conductor=user.conductor)
            
            # Quitamos el campo 'conductor' del formulario para que no sea visible ni editable,
            # ya que el backend lo asignará automáticamente usando su sesión activa
            if 'conductor' in self.fields:
                self.fields.pop('conductor')