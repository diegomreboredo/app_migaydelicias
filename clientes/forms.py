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
            "observaciones": forms.Textarea(
                attrs={
                    "rows": 3
                }
            )
        }