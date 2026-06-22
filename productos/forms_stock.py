from django import forms

class AgregarStockForm(forms.Form):

    cantidad = forms.IntegerField(
        min_value=1,
        label="Cantidad"
    )

    motivo = forms.CharField(
        required=False,
        label="Motivo"
    )