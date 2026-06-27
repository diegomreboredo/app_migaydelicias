from django import forms

from .models import Producto
from categorias.models import Categoria


class ProductoForm(forms.ModelForm):

    stock_inicial = forms.IntegerField(
        required=False,
        min_value=0,
        initial=0,
        label="Stock inicial"
    )

    class Meta:

        model = Producto

        fields = [
            "categoria",
            "nombre",
            "descripcion",
            "precio",
            "imagen",
            "stock_minimo",
            "activo",
        ]

        widgets = {

            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),

            "precio": forms.NumberInput(
                attrs={
                    "class": "form-control"
                }
            ),
            "imagen": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "stock_minimo": forms.NumberInput(
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

    def __init__(self, empresa, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["categoria"].queryset = (
            Categoria.objects.filter(
                empresa=empresa,
                activo=True
            )
        )

        self.fields["categoria"].widget.attrs.update({
            "class": "form-select"
        })

        self.fields["stock_inicial"].widget.attrs.update({
            "class": "form-control"
        })