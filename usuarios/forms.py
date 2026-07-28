from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UsuarioRegistroForm(UserCreationForm):

    TIPO_USUARIO = (
        ("conductor", "Conductor"),
        ("admin", "Administrador"),
    )

    tipo_usuario = forms.ChoiceField(
        choices=TIPO_USUARIO,
        label="Tipo de usuario",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ej: juan123",
            }
        ),
    )

    email = forms.EmailField(
        label="Correo",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "correo@empresa.com",
            }
        ),
    )

    first_name = forms.CharField(
        label="Nombres",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nombres",
            }
        ),
    )

    last_name = forms.CharField(
        label="Apellidos",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Apellidos",
            }
        ),
    )

    nombre_conductor = forms.CharField(
        label="Nombre del conductor",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nombre completo",
            }
        ),
    )

    telefono = forms.CharField(
        label="Teléfono",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "3001234567",
            }
        ),
    )

    correo_conductor = forms.EmailField(
        label="Correo del conductor",
        required=False,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "conductor@empresa.com",
            }
        ),
    )

    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Contraseña",
            }
        ),
    )

    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirmar contraseña",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Usuario",
            }
        ),
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Contraseña",
            }
        ),
    )