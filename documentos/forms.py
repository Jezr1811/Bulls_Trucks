from django import forms

from .models import Documento


class DocumentoForm(forms.ModelForm):

    class Meta:
        model = Documento

        fields = [
            "viaje",
            "vehiculo",
            "conductor",
            "tipo",
            "numero",
            "fecha_expedicion",
            "fecha_vencimiento",
            "observaciones",
            "imagen",
            "pdf",
        ]

        widgets = {

            "viaje": forms.Select(attrs={
                "class": "form-select rounded-pill"
            }),

            "vehiculo": forms.Select(attrs={
                "class": "form-select rounded-pill"
            }),

            "conductor": forms.Select(attrs={
                "class": "form-select rounded-pill"
            }),

            "tipo": forms.Select(attrs={
                "class": "form-select rounded-pill"
            }),

            "numero": forms.TextInput(attrs={
                "class": "form-control rounded-pill",
                "placeholder": "Número del documento"
            }),

            "fecha_expedicion": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control rounded-pill"
            }),

            "fecha_vencimiento": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control rounded-pill"
            }),

            "observaciones": forms.Textarea(attrs={
                "class": "form-control rounded-4",
                "rows": 3,
                "placeholder": "Observaciones..."
            }),

            "imagen": forms.ClearableFileInput(attrs={
                "class": "d-none",
                "id": "id_imagen",
            }),

            "pdf": forms.ClearableFileInput(attrs={
                "class": "d-none",
                "id": "id_pdf",
            }),
        }