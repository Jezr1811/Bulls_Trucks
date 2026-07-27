# contabilidad/forms.py
from django import forms
from .models import Transaccion

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['tipo', 'monto', 'categoria', 'descripcion']
        widgets = {
            # Lo ocultamos porque tus botones de "Ingreso" y "Gasto" se encargan de cambiar este valor por JS
            'tipo': forms.HiddenInput(attrs={'id': 'id_tipo_transaccion', 'value': 'ingreso'}),
            
            # Estilos Bootstrap hermosos y redondeados para hacer match con tu interfaz
            'monto': forms.NumberInput(attrs={
                'class': 'form-control rounded-pill border-0 py-2.5 px-3 bg-white text-dark shadow-sm',
                'placeholder': 'Ej: 150000'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select rounded-pill border-0 py-2.5 px-3 bg-white text-dark shadow-sm'
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control rounded-pill border-0 py-2.5 px-3 bg-white text-dark shadow-sm',
                'placeholder': '¿En qué consistió este movimiento? (Opcional)'
            }),
        }