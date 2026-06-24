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
        ]

        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "telefono": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "direccion": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "observaciones": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Observaciones del cliente..."
                }
            ),
        }