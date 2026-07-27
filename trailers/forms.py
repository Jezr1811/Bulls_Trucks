from django import forms
from .models import Trailer


class TrailerForm(forms.ModelForm):

    class Meta:
        model = Trailer
        fields = "__all__"