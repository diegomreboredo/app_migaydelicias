from django import forms

from .models import Compra, DetalleCompra


class CompraForm(forms.ModelForm):

    class Meta:

        model = Compra

        fields = [
            "proveedor",
            "estado",
            "observaciones",
        ]

        widgets = {

            "proveedor": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "estado": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "observaciones": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Observaciones..."
                }
            ),

        }


class DetalleCompraForm(forms.ModelForm):

    class Meta:

        model = DetalleCompra

        fields = [
            "producto",
            "cantidad",
            "precio_unitario",
        ]

        widgets = {

            "producto": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "cantidad": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1
                }
            ),

            "precio_unitario": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),

        }