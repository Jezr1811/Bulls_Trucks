from django import forms
from .models import Gasto
from viajes.models import Viaje  # Importamos viajes para poder filtrar el queryset


class GastoForm(forms.ModelForm):

    class Meta:
        model = Gasto
        # 🛠️ CORRECCIÓN 1: Excluimos 'viaje' para que Django no lo exija en el HTML
        exclude = ("viaje",)
        
        widgets = {
            "fecha": forms.DateInput(
                attrs={"type": "date"}
            ),
        }

    def __init__(self, *args, **kwargs):
        # Capturamos el usuario enviado desde la vista
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # 🛠️ CORRECCIÓN 2: Validamos si 'viaje' existe en los campos antes de filtrarlo
        # (Esto evita errores si en el futuro decides volver a usarlo o excluirlo)
        if "viaje" in self.fields and user and not user.is_superuser and hasattr(user, 'conductor'):
            # En el select del formulario SOLO aparecerán los viajes asignados a él
            self.fields['viaje'].queryset = Viaje.objects.filter(conductor=user.conductor)