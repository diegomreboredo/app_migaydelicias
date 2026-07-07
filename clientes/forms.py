from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente

        fields = [
            "nombre",
            "telefono",
            "direccion",
            "observaciones",
            "activo",
        ]

        widgets = {

            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej.: Juan Pérez"
                }
            ),

            "telefono": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej.: 11 5555-5555"
                }
            ),

            "direccion": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej.: Av. Siempre Viva 123"
                }
            ),

            "observaciones": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Observaciones del cliente..."
                }
            ),

            "activo": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }