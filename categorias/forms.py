from django import forms

from .models import Categoria


class CategoriaForm(forms.ModelForm):

    class Meta:

        model = Categoria

        fields = [
            "nombre",
            "icono",
            "orden",
            "activo",
        ]

        widgets = {

            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "icono": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: bi-cup-hot"
                }
            ),

            "orden": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "activo": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }