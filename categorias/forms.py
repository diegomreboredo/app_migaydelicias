from django import forms
from .iconos import ICONOS_BOOTSTRAP
from .models import Categoria


class CategoriaForm(forms.ModelForm):

    class Meta:

        model = Categoria

        fields = [
            "nombre",
            "orden",
            "activo",
        ]

        widgets = {

            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control"
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