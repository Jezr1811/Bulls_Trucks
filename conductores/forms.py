from django import forms

from .models import Conductor


class ConductorForm(forms.ModelForm):

    class Meta:
        model = Conductor
        fields = "__all__"